"""Audit organized notebooks and optionally verify full recovered originals."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
from audit_project import audit, SECRET

ROOT = Path(__file__).resolve().parents[1]


def review(root: Path, full: bool = False) -> dict:
    result = audit(root, full)
    errors = result['errors']
    manifest = json.loads((root/'docs/notebook_review_manifest.json').read_text(encoding='utf-8'))
    code_positions = 0
    for record in manifest:
        path = root/record['review_path']
        if not path.is_file():
            errors.append('Missing review notebook: '+record['review_path'])
            continue
        notebook = json.loads(path.read_text(encoding='utf-8'))
        if len(notebook['cells']) != record['cell_count']:
            errors.append('Cell positions changed: '+record['review_path'])
        for cell, expected in zip(notebook['cells'], record['cells']):
            text = ''.join(cell.get('source', []))
            if hashlib.sha256(text.encode('utf-8')).hexdigest() != expected['review_source_sha256']:
                errors.append(f'{record["review_path"]}: cell {expected["cell"]}: source differs from reviewed version')
            code_positions += cell.get('cell_type') == 'code'
            for output in cell.get('outputs', []):
                values = [''.join(output.get('text', []))]
                for mime,value in output.get('data', {}).items():
                    if mime.startswith('text/'):
                        values.append(''.join(value) if isinstance(value,list) else str(value))
                if any(SECRET.search(v) for v in values):
                    errors.append(f'{record["review_path"]}: possible credential in text output')
        if full:
            recovered = root/record['recovered_path']
            if not recovered.is_file() or hashlib.sha256(recovered.read_bytes()).hexdigest() != record['recovered_sha256']:
                errors.append('Full recovered notebook changed or missing: '+record['recovered_path'])
    result['reviewed_notebooks'] = len(manifest)
    result['code_cell_positions_preserved'] = code_positions
    result['saved_error_cells_cleared_in_review_copies'] = sum(c['action']=='clear_saved_error' for r in manifest for c in r['cells'])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-originals', action='store_true')
    args = parser.parse_args()
    result = review(ROOT, args.verify_originals)
    print(json.dumps(result,indent=2))
    raise SystemExit(bool(result['errors']))
