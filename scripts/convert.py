#!/usr/bin/env python3
"""แปลงไฟล์ Excel -> data/*.json สำหรับ Dashboard
ใช้: python scripts/convert.py [--redeem FILE] [--master FILE] [--out data]
ไม่ยึดชื่อไฟล์/ชื่อ Sheet: หา Sheet ที่มีคอลัมน์ STATUS_REDEEM + PARTNER_CODE (Redeem), EMP_ID (MAN LIST), SHOP CODE (SHOP LIST)"""
import argparse, csv, datetime, json, os, sys
import openpyxl

def cell(v):
    if v is None: return ''
    if isinstance(v, (datetime.datetime, datetime.date)): return v.strftime('%Y/%m/%d')
    if isinstance(v, float) and v.is_integer(): return str(int(v))
    return str(v).strip()

def sheets(path):
    if path.lower().endswith('.csv'):
        with open(path, encoding='utf-8-sig', newline='') as f:
            yield os.path.basename(path), [[cell(c) for c in r] for r in csv.reader(f)]
        return
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        yield ws.title, [[cell(c) for c in r] for r in ws.iter_rows(values_only=True)]

def find_header(rows, keys):
    for i, r in enumerate(rows[:15]):
        up = [c.upper() for c in r]
        if all(k in up for k in keys): return i
    return -1

def trim(cols, rows):
    while cols and cols[-1] == '': cols = cols[:-1]
    rows = [r[:len(cols)] + [''] * (len(cols) - len(r)) for r in rows if any(x != '' for x in r)]
    return cols, rows

def encode(cols, rows):
    dicts, idx = [], []
    for j in range(len(cols)):
        d, vals, ix = {}, [], []
        for r in rows:
            v = r[j]
            if v not in d: d[v] = len(vals); vals.append(v)
            ix.append(d[v])
        dicts.append(vals); idx.append(ix)
    return {'cols': cols, 'dict': dicts, 'idx': idx, 'n': len(rows)}

def now(): return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime('%Y-%m-%d %H:%M')

def dump(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))

def convert_redeem(path, out, by):
    for name, rows in sheets(path):
        h = find_header(rows, ['STATUS_REDEEM', 'PARTNER_CODE'])
        if h >= 0:
            cols, body = trim(rows[h], rows[h + 1:])
            enc = encode(cols, body)
            enc['meta'] = {'fileName': os.path.basename(path), 'sheet': name, 'uploadedAt': now(), 'by': by}
            dump(enc, os.path.join(out, 'redeem.json'))
            print(f'redeem: {path} [{name}] {len(body)} rows')
            return enc['meta']
    sys.exit(f'ERROR: ไม่พบ Sheet ที่มีคอลัมน์ STATUS_REDEEM ใน {path}')

def convert_master(path, out, by):
    old = {}
    p = os.path.join(out, 'master.json')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f: old = json.load(f)
    res = {'meta': {'fileName': os.path.basename(path), 'uploadedAt': now(), 'by': by}}
    for name, rows in sheets(path):
        h = find_header(rows, ['EMP_ID'])
        if h >= 0 and 'man' not in res:
            c, r = trim(rows[h], rows[h + 1:]); res['man'] = {'cols': c, 'rows': r}; continue
        h = find_header(rows, ['SHOP CODE'])
        if h >= 0 and 'shop' not in res:
            c, r = trim(rows[h], rows[h + 1:]); res['shop'] = {'cols': c, 'rows': r}
    if 'man' not in res and 'shop' not in res:
        sys.exit(f'ERROR: ไม่พบ Sheet MAN LIST (EMP_ID) หรือ SHOP LIST (SHOP CODE) ใน {path}')
    for k in ('man', 'shop'):
        if k not in res:
            if k not in old: sys.exit(f'ERROR: ไม่มี {k} ในไฟล์ใหม่และไม่มีข้อมูลเดิม')
            res[k] = old[k]; res['meta']['note'] = f'ใช้ {k} เดิม'
    dump(res, p)
    print(f"master: {path} man={len(res['man']['rows'])} shop={len(res['shop']['rows'])}")
    return res['meta']

def write_version(out):
    v = {}
    for k in ('redeem', 'master'):
        p = os.path.join(out, k + '.json')
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f: m = json.load(f).get('meta', {})
            v[k] = f"{m.get('fileName','')}|{m.get('uploadedAt','')}|{os.path.getsize(p)}"
    dump(v, os.path.join(out, 'version.json'))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--redeem'); ap.add_argument('--master'); ap.add_argument('--out', default='data')
    ap.add_argument('--by', default='github'); ap.add_argument('--version-only', action='store_true')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.redeem: convert_redeem(a.redeem, a.out, a.by)
    if a.master: convert_master(a.master, a.out, a.by)
    write_version(a.out)
