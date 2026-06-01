#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 — אומדנים / ניתוח תרחישים (sensitivity)
קורא את ULEASE_FORECAST.csv ומריץ 3 תרחישים על נקודת הרגישות המרכזית: קצב העסקאות.
ההכנסות תלויות-העסקה (עסקה+לידים+מימון) מוכפלות במכפיל; מנויים/פרסום/הוצאות קבועים.
הרצה:  python3 CASES/ULEASE_FORECAST.py && python3 CASES/ULEASE_SCENARIOS.py
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "ULEASE_FORECAST.csv"), encoding="utf-8-sig")))
flo = lambda r,k: float(r[k])
OPENING = 150_000
SCEN = [("שמרני", 0.70), ("בסיס", 1.00), ("אופטימי", 1.30)]

def run(mult):
    cum = OPENING; a = {2026: {}, 2027: {}}
    for yr in (2026, 2027): a[yr] = dict(rev=0.0, net=0.0)
    last_total = 0.0
    for i, r in enumerate(rows):
        yr = 2026 if i < 7 else 2027
        deal_driven = flo(r,"deal_rev") + flo(r,"lead_rev") + flo(r,"fin_rev")
        indep = flo(r,"sub_rev") + flo(r,"ad_rev")
        total = mult*deal_driven + indep
        net = total - flo(r,"opex")
        cum += net; last_total = total
        a[yr]["rev"] += total; a[yr]["net"] += net
    return a, cum, last_total*12

def m(n): return f"₪{n/1e6:.2f}M"
print('| תרחיש | עסקאות | הכנסה 2026 | נטו 2026 | הכנסה 2027 | נטו 2027 | Cash סוף 27 | Run-rate |')
print('|-------|-------|-----------|---------|-----------|---------|-----------|----------|')
out = [["scenario","deals_mult","rev_2026","net_2026","rev_2027","net_2027","cash_end_2027","run_rate_dec27"]]
for name, mult in SCEN:
    a, cum, rr = run(mult)
    print(f"| {name} (×{mult:g}) | ×{mult:g} | {m(a[2026]['rev'])} | {m(a[2026]['net'])} | {m(a[2027]['rev'])} | {m(a[2027]['net'])} | {m(cum)} | {m(rr)} |")
    out.append([name, mult, round(a[2026]['rev']), round(a[2026]['net']), round(a[2027]['rev']), round(a[2027]['net']), round(cum), round(rr)])

with open(os.path.join(HERE, "ULEASE_SCENARIOS.csv"), "w", newline="", encoding="utf-8-sig") as fcsv:
    csv.writer(fcsv).writerows(out)
print("\nנכתב → ULEASE_SCENARIOS.csv · ההנחה: הוצאות קבועות (operating leverage); בפועל חלק מהשיווק יגדל עם הנפח.")
