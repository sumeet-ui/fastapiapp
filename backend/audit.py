import sys

bad_checks = [
    ('routers/job.py',     'db.query('),
    ('routers/company.py', 'db.query('),
    ('routers/auth.py',    'db.query('),
    ('app/main.py',        'create_all(bind='),
]
good_checks = [
    ('models/company.py',  'lazy='),
    ('models/job.py',      'lazy='),
]

ok = True
for f, pat in bad_checks:
    found = pat in open(f).read()
    label = "BAD" if found else "OK"
    print(f"  {label:4} {f}: should NOT contain '{pat}'")
    if found:
        ok = False

for f, pat in good_checks:
    found = pat in open(f).read()
    label = "OK" if found else "MISSING"
    print(f"  {label:7} {f}: should contain '{pat}'")
    if not found:
        ok = False

print()
print("FULLY FIXED" if ok else "STILL HAS ISSUES")
sys.exit(0 if ok else 1)
