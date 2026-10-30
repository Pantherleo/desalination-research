"""Training-only constant baselines for an exactly held-out spacer geometry.

Reads cached XLSX values using the standard library. Does not train or alter
the historical notebook models. All row-level outputs remain local.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import posixpath
from statistics import fmean, median
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
TARGETS = ('Output_CP_Modulus_Factor', 'Output_Channel_Velocity_Mean')
HOLDOUT = 'configuration6_interspacer3mm'


def read_table(path: Path) -> list[dict]:
    """Read the named simulation sheet without recalculating any workbook cells."""
    with zipfile.ZipFile(path) as package:
        workbook = ET.fromstring(package.read('xl/workbook.xml'))
        sheets = workbook.findall('s:sheets/s:sheet', NS)
        sheet = next((s for s in sheets if s.attrib['name'] == 'RO_Simulation_Dataset'), None)
        if sheet is None:
            raise ValueError('Missing RO_Simulation_Dataset sheet')
        rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
        relationships = ET.fromstring(package.read('xl/_rels/workbook.xml.rels'))
        target = next(r.attrib['Target'] for r in relationships if r.attrib['Id'] == rid)
        member = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
        if not member.startswith('xl/worksheets/'):
            raise ValueError('Unexpected worksheet relationship path')
        strings = []
        if 'xl/sharedStrings.xml' in package.namelist():
            strings = [''.join(n.itertext()) for n in ET.fromstring(package.read('xl/sharedStrings.xml'))]
        rows = []
        for row in ET.fromstring(package.read(member)).findall('s:sheetData/s:row', NS):
            values = {}
            for cell in row:
                column = ''.join(c for c in cell.attrib['r'] if c.isalpha())
                value_node = cell.find('s:v', NS)
                value = value_node.text if value_node is not None else ''.join(cell.itertext())
                if cell.attrib.get('t') == 's':
                    value = strings[int(value)]
                values[column] = value
            rows.append(values)
    if len(rows) < 2:
        raise ValueError('Workbook has no data rows')
    headers = rows[0]
    if len(set(headers.values())) != len(headers):
        raise ValueError('Duplicate column labels')
    return [{label: row.get(column, '') for column, label in headers.items()} for row in rows[1:]]


def partition(records: list[dict], holdout: str) -> tuple[list, list]:
    train = [r for r in records if r.get('Spacer_Design_Label') != holdout]
    test = [r for r in records if r.get('Spacer_Design_Label') == holdout]
    if not train or not test:
        raise ValueError('Exact geometry holdout must leave nonempty training and test sets')
    if any(not r.get('Spacer_Design_Label') for r in records):
        raise ValueError('Missing geometry label')
    return train, test


def score(actual: list[float], predicted: list[float]) -> dict:
    if not actual or len(actual) != len(predicted):
        raise ValueError('Actual and predicted lengths must match and be nonzero')
    if not all(math.isfinite(v) for v in actual + predicted):
        raise ValueError('Nonfinite metric input')
    errors = [a-p for a,p in zip(actual,predicted)]
    sse = sum(e*e for e in errors)
    center = fmean(actual)
    sst = sum((a-center)**2 for a in actual)
    return {'mae': fmean(abs(e) for e in errors), 'rmse': math.sqrt(sse/len(errors)),
            'r2': 1-sse/sst if sst else None}


def evaluate(records: list[dict], holdout: str = HOLDOUT) -> tuple[dict, list]:
    train, test = partition(records, holdout)
    result = {'holdout_label': holdout, 'train_rows': len(train), 'test_rows': len(test),
              'geometry_counts': dict(Counter(r['Spacer_Design_Label'] for r in records)),
              'protocol': 'Exact geometry holdout; fixed constants fitted on training targets only',
              'targets': {}}
    predictions = []
    for index, row in enumerate(test, 1):
        predictions.append({'test_row': index, 'case_uid': row.get('Case_UID', ''),
                            'geometry': holdout})
    for target in TARGETS:
        training = [float(r[target]) for r in train]
        actual = [float(r[target]) for r in test]
        if not all(math.isfinite(v) for v in training+actual):
            raise ValueError(f'Nonfinite target: {target}')
        constants = {'train_mean': fmean(training), 'train_median': median(training)}
        result['targets'][target] = {name: {'constant': value, **score(actual, [value]*len(actual))}
                                     for name,value in constants.items()}
        for row, observed in zip(predictions, actual):
            row[target+'_actual'] = observed
            for name,value in constants.items():
                row[target+'_'+name] = value
    return result, predictions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=ROOT/'data/tables/Perfect_RO_Plant_Dataset2.xlsx')
    parser.add_argument('--holdout', default=HOLDOUT)
    parser.add_argument('--output', type=Path, default=ROOT/'reports/runs/geometry_baseline')
    args = parser.parse_args()
    if not args.data.is_file():
        parser.error('Dataset missing; obtain the approved local workbook described in docs/DATA_CATALOG.md')
    records = read_table(args.data)
    result, predictions = evaluate(records, args.holdout)
    result.update({'dataset': args.data.name, 'dataset_sha256': hashlib.sha256(args.data.read_bytes()).hexdigest(),
                   'units': {'Output_CP_Modulus_Factor': 'ratio as defined by notebook; physical interpretation unverified',
                             'Output_Channel_Velocity_Mean': 'source units not verified'},
                   'limitations': ['No confidence interval; independence between image indices not established',
                                   'Constant reference only; historical model scores were not rerun']})
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'metrics.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    with (args.output/'predictions.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(predictions[0]))
        writer.writeheader()
        writer.writerows(predictions)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
