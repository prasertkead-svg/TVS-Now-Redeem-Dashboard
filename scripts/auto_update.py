#!/usr/bin/env python3
"""GitHub Actions: หาไฟล์ Excel/CSV ที่อัปโหลดเข้ามา (ที่ไหนก็ได้ใน repo, ชื่ออะไรก็ได้)
ดูจากหัวคอลัมน์ว่าเป็นไฟล์ Redeem หรือ MAN&SHOPLIST แล้วแปลงเป็น data/*.json
ใช้: python scripts/auto_update.py <before_sha> <after_sha>   (ไม่ใส่ = สแกนทุกไฟล์)"""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import convert

EXT = ('.xlsx', '.xlsm', '.csv')

def git(*a): return subprocess.run(['git', *a], capture_output=True, text=True).stdout.strip()

def candidates(before, after):
    files = []
    if before and after and set(before) != {'0'}:
        files = git('diff', '--name-only', '--diff-filter=AM', before, after).splitlines()
    if not files:
        files = git('ls-files').splitlines()
    return [f for f in files if f.lower().endswith(EXT) and os.path.isfile(f) and not f.startswith('data/')]

def kind(path):
    try:
        for _, rows in convert.sheets(path):
            if convert.find_header(rows, ['STATUS_REDEEM', 'PARTNER_CODE']) >= 0: return 'redeem'
        for _, rows in convert.sheets(path):
            if convert.find_header(rows, ['EMP_ID']) >= 0 or convert.find_header(rows, ['SHOP CODE']) >= 0: return 'master'
    except Exception as e:
        print('skip', path, e)
    return None

def ctime(f):
    t = git('log', '-1', '--format=%ct', '--', f)
    return int(t) if t else 0

if __name__ == '__main__':
    before, after = (sys.argv[1:3] + [None, None])[:2]
    newest = {}
    for f in candidates(before, after):
        k = kind(f)
        print(f, '->', k)
        if k and (k not in newest or ctime(f) >= ctime(newest[k])): newest[k] = f
    os.makedirs('data', exist_ok=True)
    if 'redeem' in newest: convert.convert_redeem(newest['redeem'], 'data', 'github')
    if 'master' in newest: convert.convert_master(newest['master'], 'data', 'github')
    if newest: convert.write_version('data')
    print('updated:', newest or 'none')
