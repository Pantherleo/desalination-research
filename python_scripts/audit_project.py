"""Read-only repository and data-integrity checks using the standard library."""
from __future__ import annotations
import argparse
import ast
import csv
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HDF_SIGNATURE = b'\x89HDF\r\n\x1a\n'
PLACEHOLDERS = {'gem.ipynb', 'preprocessing.ipynb', 'process2.ipynb'}
SECRET = re.compile(r'(?:AIza[\w-]{30,}|sk-(?:proj-)?[\w-]{30,}|ghp_[\w]{30,})')


def hdf_references(path: Path, data_root: Path) -> list[Path]:
    """Resolve local XMF HDF references and reject paths outside the dataset."""
    result = []
    for node in ET.parse(path).iter('DataItem'):
        if node.attrib.get('Format', '').upper() != 'HDF':
            continue
        value = (node.text or '').strip()
        if ':' not in value:
            raise ValueError('HDF reference has no dataset separator')
        filename, key = value.rsplit(':', 1)
        if not filename or not key:
            raise ValueError('HDF reference must name a file and dataset')
        resolved = (path.parent / filename).resolve()
        if not resolved.is_relative_to(data_root.resolve()):
            raise ValueError('HDF reference escapes RO_data')
        if not resolved.is_file():
            raise ValueError('HDF companion file is missing')
        result.append(resolved)
    if not result:
        raise ValueError('No HDF references found')
    return result


def audit(root: Path, verify_originals: bool = False) -> dict:
    errors, warnings = [], []
    valid, placeholders = 0, []
    for path in sorted((root / 'notebooks').rglob('*.ipynb')):
        rel = path.relative_to(root).as_posix()
        if not path.stat().st_size and path.parent.name == 'placeholders' and path.name in PLACEHOLDERS:
            placeholders.append(rel)
            continue
        try:
            nb = json.loads(path.read_text(encoding='utf-8-sig'))
            if nb.get('nbformat') != 4 or not isinstance(nb.get('cells'), list):
                raise ValueError('Expected v4 notebook cells')
            valid += 1
            for index, cell in enumerate(nb['cells'], 1):
                if SECRET.search(''.join(cell.get('source', []))):
                    errors.append(f'{rel}: cell {index}: possible source credential')
                for output in cell.get('outputs', []):
                    if output.get('output_type') == 'error':
                        errors.append(f'{rel}: cell {index}: saved error output')
        except (ValueError, TypeError, KeyError) as exc:
            errors.append(f'{rel}: invalid notebook: {exc}')
    if not valid:
        errors.append('No valid processing notebook found')
    for path in (root / 'python_scripts').glob('*.py'):
        try:
            code = path.read_text(encoding='utf-8-sig')
            ast.parse(code)
            if SECRET.search(code):
                errors.append(f'{path.name}: possible source credential')
        except (ValueError, SyntaxError) as exc:
            errors.append(f'{path.name}: invalid Python: {exc}')
    h5s = sorted((root / 'RO_data').rglob('*.h5'))
    xmfs = sorted((root / 'RO_data').rglob('*.xmf'))
    for path in h5s:
        with path.open('rb') as handle:
            signature = handle.read(8)
        if signature != HDF_SIGNATURE:
            errors.append(f'{path.relative_to(root)}: no HDF5 signature at offset zero')
        if not path.with_suffix('.xmf').is_file():
            errors.append(f'{path.relative_to(root)}: missing XMF companion')
    checked = 0
    for path in xmfs:
        try:
            refs = hdf_references(path, root / 'RO_data')
            if path.with_suffix('.h5').resolve() not in refs:
                errors.append(f'{path.relative_to(root)}: does not reference same-stem HDF5')
            checked += 1
        except (ValueError, ET.ParseError) as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
    if not h5s and not xmfs:
        warnings.append('Local simulation files absent or excluded: dataset integrity was not checked')
    if placeholders:
        warnings.append('Three original zero-byte placeholders are retained; they are not executable notebooks')
    manifest = root / 'docs/file_manifest.csv'
    hash_count = 0
    if not manifest.is_file():
        errors.append('Missing original-file manifest')
    elif verify_originals:
        with manifest.open(encoding='utf-8', newline='') as handle:
            for record in csv.DictReader(handle):
                path = (root / record['current_path']).resolve()
                if not path.is_relative_to(root.resolve()):
                    errors.append('Manifest path escapes project')
                elif not path.is_file():
                    errors.append(f'Missing original: {record["current_path"]}')
                elif hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
                    errors.append(f'Original content changed: {record["current_path"]}')
                else:
                    hash_count += 1
    return {'valid_notebooks': valid, 'preserved_empty_notebooks': placeholders,
            'hdf5_files': len(h5s), 'xmf_files': len(xmfs), 'xmf_references_checked': checked,
            'original_hashes_verified': hash_count, 'errors': errors, 'warnings': warnings,
            'scope': 'File integrity only; not CFD physical validation or model reproduction'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-originals', action='store_true')
    args = parser.parse_args()
    result = audit(ROOT, args.verify_originals)
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['errors']))
