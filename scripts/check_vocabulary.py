#!/usr/bin/env python3
"""Check working Markdown entries; no third-party dependencies required."""
from pathlib import Path
import re
import sys
import unicodedata
ROOT = Path(__file__).resolve().parents[1]
TYPES = {'noun','verb','adjective','adverb','pronoun','determiner','preposition','conjunction','subjunction','interjection','expression','numeral'}
REQUIRED = ['English','Topics','Form status','Notes','Sources']
def main():
    errors = []
    keys = {}
    ids = {}
    files = [p for p in (ROOT/'vocabulary').rglob('*.md') if p.name != 'INDEX.md']
    rows = 0
    for p in files:
        text = p.read_text(encoding='utf-8')
        label = str(p.relative_to(ROOT))
        match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not match:
            errors.append(f'{label}: missing metadata block')
            continue
        meta = dict(re.findall(r'^([a-z_]+):\s*(.*?)\s*$', match.group(1), re.M))
        for field in ['id','lemma','word_type','sense','checked_on']:
            if not meta.get(field): errors.append(f'{label}: missing {field}')
        if meta.get('word_type') not in TYPES: errors.append(f'{label}: unsupported word_type')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',meta.get('checked_on','')): errors.append(f'{label}: checked_on must be YYYY-MM-DD')
        for field in REQUIRED:
            if f'**{field}:**' not in text: errors.append(f'{label}: missing {field}')
        key = (unicodedata.normalize('NFC',meta.get('lemma','')).casefold(),meta.get('word_type'),meta.get('sense'))
        if key in keys: errors.append(f'{label}: duplicate lemma/type/sense with {keys[key]}')
        keys[key] = label
        if meta.get('id') in ids: errors.append(f'{label}: duplicate id with {ids[meta.get("id")]}')
        ids[meta.get('id')] = label
        table_rows = 0
        for no,line in enumerate(text.splitlines(),1):
            if not line.startswith('|'): continue
            cells = [c.strip() for c in re.split(r'(?<!\\)\|',line)[1:-1]]
            if len(cells) != 4:
                errors.append(f'{label}:{no}: expected four table cells')
                continue
            if cells[0] == 'Form / feature' or all(re.fullmatch(r':?-+:?',c) for c in cells): continue
            table_rows += 1
            if not all(cells): errors.append(f'{label}:{no}: incomplete form/example row')
            if any('[Form or feature]' in c or '[One sentence' in c or '[English translation]' in c for c in cells): errors.append(f'{label}:{no}: unreplaced template placeholder')
        if not table_rows: errors.append(f'{label}: missing form/example table')
        rows += table_rows
    if errors:
        print('\n'.join(errors)); return 1
    print(f'Checked {len(files)} entries and {rows} form/feature rows. No structural or duplicate-key errors.')
    print('Grammar, meanings and natural example usage require language review.')
    return 0
if __name__ == '__main__':
    sys.exit(main())
