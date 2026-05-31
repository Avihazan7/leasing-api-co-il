#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 Leasing.co.il — Financial Forecast Model (Base Case v0.1)
Horizon: יוני 2026 (בסיס השקה) → דצמבר 2027.
כל הערכים ב-₪. כל ההנחות מפורשות וניתנות לכיול.
"""
import csv, os

# ---------------- תמחור קבוע (מהמייסד) ----------------
AVG_DEAL_VALUE = 150_000      # ₪ עסקת רכב ממוצעת
DEAL_TAKE      = 0.0333       # נתח פלטפורמה משוקלל לעסקה (כולל 1% ספק + מימון/ליסינג)
DEAL_REV       = round(AVG_DEAL_VALUE * DEAL_TAKE)   # ≈ 4,995 ₪ לעסקה
LEAD_PRICE     = 150          # ₪ לליד שנמכר לספקים (מאושר ע"י המייסד)
PRO_PRICE      = 4_500        # ₪/חודש מנוי Pro
PROMAX_PRICE   = 7_700        # ₪/חודש מנוי Pro Max
LEADS_PER_DEAL = 5            # יחס יוני: 130 לידים / 26 עסקאות
# חיתום דיגיטלי (מימון+ביטוח) — עמלה ממוצעת לעסקה אחרי attach rates; פעיל מספטמבר 26
FIN_ATTACH, FIN_COMM = 0.50, 1500   # 50% מהעסקאות ממומנות · ₪1,500 origination
INS_ATTACH, INS_COMM = 0.40, 600    # 40% מבטחות · ₪600 עמלת סוכן
UW_PER_DEAL = round(FIN_ATTACH*FIN_COMM + INS_ATTACH*INS_COMM)  # ≈ 990 ₪/עסקה
UW_START = (2026, 9)                 # החיתום הדיגיטלי עולה לאוויר

# ---------------- ציר זמן ----------------
months = [(2026, m) for m in range(6, 13)] + [(2027, m) for m in range(1, 13)]
N = len(months)  # 19
HEB_MON = {1:"ינואר",2:"פברואר",3:"מרץ",4:"אפריל",5:"מאי",6:"יוני",
           7:"יולי",8:"אוגוסט",9:"ספטמבר",10:"אוקטובר",11:"נובמבר",12:"דצמבר"}

# ---------------- מנוע עסקאות: טרנד חלק × עונתיות ----------------
BASE_DEALS = 26   # יוני 2026 השקה: 16 B2B2C + 10 B2B
def growth_for(y, m):
    if y == 2026:            return 0.18   # ראמפ H2-2026 (בסיס קטן)
    if y == 2027 and m <= 6: return 0.12   # H1-2027
    return 0.07                            # H2-2027
SEAS = {1:1.30,2:1.05,3:1.10,4:0.95,5:1.00,6:1.00,
        7:1.05,8:0.95,9:1.10,10:1.00,11:1.05,12:0.90}

trend, deals = [], []
for i,(y,m) in enumerate(months):
    t = BASE_DEALS if i == 0 else trend[-1]*(1+growth_for(y,m))
    trend.append(t)
    deals.append(round(t*SEAS[m]))

# ---------------- מנוע מנויים ----------------
subs_total, pro_subs, promax_subs = [], [], []
CHURN = 0.02
for i,(y,m) in enumerate(months):
    if i == 0:
        tot = 15
    else:
        net = 5 if y == 2026 else 7
        tot = subs_total[-1] + net - round(CHURN*subs_total[-1])
    subs_total.append(tot)
    share = 0.25 * i / (N-1)          # נתח Pro Max מטפס 0% → 25%
    pmx = round(tot*share)
    promax_subs.append(pmx)
    pro_subs.append(tot-pmx)

# ---------------- לוחות עלויות והכנסות נלוות (₪ אלפים) ----------------
K = 1000
team_k = [30,30,30,50,50,50,50] + [75]*6 + [100]*6
mkt_k  = [15,20,22,25,28,32,30] + [45,42,45,45,50,55,60,60,70,70,75,70]
infra_k= [4,4,5,6,7,7,8]        + [10,10,11,11,12,12,14,15,16,17,18,18]
gna_k  = [5,6,6,8,9,10,10]      + [12,12,13,13,14,15,16,17,18,19,20,20]
ad_k   = [0,0,0,0,8,10,12]      + [15,15,18,20,22,25,28,28,32,35,38,40]
assert all(len(x)==N for x in [team_k,mkt_k,infra_k,gna_k,ad_k])

# ---------------- חישוב P&L ----------------
OPENING_CASH = 150_000  # גיוס יעד
rows, cum = [], OPENING_CASH
for i,(y,m) in enumerate(months):
    leads = deals[i]*LEADS_PER_DEAL
    deal_rev = deals[i]*DEAL_REV
    lead_rev = leads*LEAD_PRICE
    sub_rev  = pro_subs[i]*PRO_PRICE + promax_subs[i]*PROMAX_PRICE
    ad_rev   = ad_k[i]*K
    uw_rev   = deals[i]*UW_PER_DEAL if (y, m) >= UW_START else 0
    total_rev= deal_rev+lead_rev+sub_rev+ad_rev+uw_rev
    opex     = (team_k[i]+mkt_k[i]+infra_k[i]+gna_k[i])*K
    net      = total_rev-opex
    cum     += net
    rows.append(dict(period=f"{HEB_MON[m]} {y%100:02d}", y=y, m=m,
        deals=deals[i], leads=leads, subs=subs_total[i], pro=pro_subs[i], promax=promax_subs[i],
        deal_rev=deal_rev, lead_rev=lead_rev, sub_rev=sub_rev, ad_rev=ad_rev, uw_rev=uw_rev,
        total_rev=total_rev, opex=opex, net=net, cum=cum, gmv=deals[i]*AVG_DEAL_VALUE))

# ---------------- פלט: CSV ----------------
out_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ULEASE_FORECAST.csv")
with open(out_csv,"w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f)
    w.writerow(["period","deals","leads","subscribers","pro","pro_max",
                "deal_rev","lead_rev","sub_rev","ad_rev","uw_rev","total_rev","opex","net_monthly","cum_cash","gmv"])
    for r in rows:
        w.writerow([r["period"],r["deals"],r["leads"],r["subs"],r["pro"],r["promax"],
            r["deal_rev"],r["lead_rev"],r["sub_rev"],r["ad_rev"],r["uw_rev"],r["total_rev"],r["opex"],r["net"],r["cum"],r["gmv"]])

# ---------------- פלט: טבלת Markdown חודשית ----------------
f = lambda n: f"{n:,.0f}"
print('| חודש | עסקאות | לידים | מנויים | הכנ׳ עסקאות | הכנ׳ לידים | הכנ׳ מנויים | פרסום | חיתום | סה"כ הכנסה | הוצאות | נטו | Cash מצטבר |')
print('|------|------:|-----:|-----:|----------:|---------:|----------:|-----:|-----:|---------:|------:|----:|----------:|')
for r in rows:
    print(f"| {r['period']} | {r['deals']} | {r['leads']} | {r['subs']} | {f(r['deal_rev'])} | {f(r['lead_rev'])} | {f(r['sub_rev'])} | {f(r['ad_rev'])} | {f(r['uw_rev'])} | {f(r['total_rev'])} | {f(r['opex'])} | {f(r['net'])} | {f(r['cum'])} |")

# ---------------- סיכומים שנתיים ----------------
def agg(yr):
    sel=[r for r in rows if r["y"]==yr]
    return dict(deals=sum(r["deals"] for r in sel), rev=sum(r["total_rev"] for r in sel),
                opex=sum(r["opex"] for r in sel), net=sum(r["net"] for r in sel),
                gmv=sum(r["gmv"] for r in sel), subs=sel[-1]["subs"], uw=sum(r["uw_rev"] for r in sel))
a26, a27 = agg(2026), agg(2027)
print("\n=== סיכום שנתי ===")
print(f"2026 (יוני–דצמ'): עסקאות {a26['deals']:,} | GMV {a26['gmv']:,.0f} | הכנסה {a26['rev']:,.0f} | מזה חיתום {a26['uw']:,.0f} | הוצאות {a26['opex']:,.0f} | נטו {a26['net']:,.0f} | מנויים {a26['subs']}")
print(f"2027 (ינו'–דצמ'): עסקאות {a27['deals']:,} | GMV {a27['gmv']:,.0f} | הכנסה {a27['rev']:,.0f} | מזה חיתום {a27['uw']:,.0f} | הוצאות {a27['opex']:,.0f} | נטו {a27['net']:,.0f} | מנויים {a27['subs']}")
d = rows[-1]
print(f"\nRun-rate דצמ' 27: הכנסה חודשית {d['total_rev']:,.0f} → שנתי {d['total_rev']*12:,.0f}")
print(f"Cash מצטבר סוף 2027 (כולל גיוס 150K): {d['cum']:,.0f}")
print(f"DEAL_REV/עסקה = {DEAL_REV:,} ₪  (3.33% × 150,000)")
