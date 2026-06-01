#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 Leasing.co.il — Financial Forecast Model (Base Case v1.4)
Horizon: יוני 2026 (בסיס השקה) → דצמבר 2027.
כל הערכים ב-₪. כל ההנחות מפורשות וניתנות לכיול.
הערה (W3): "נטו" = רווח תפעולי לפני מס חברות ומע"מ.
"""
import csv, os

# ---------------- תמחור קבוע (מהמייסד — D-005, D-015) ----------------
AVG_DEAL_VALUE = 150_000      # ₪ עסקת רכב ממוצעת
# עמלות עסקה מדורגות (D-015, 1.6.2026) — התחזית מניחה את אמצע כל טווח:
B2B_TAKE   = 0.0165           # B2B מהספק:   טווח 1.1%–2.2%  → אמצע 1.65%
B2B2C_TAKE = 0.0222           # B2B2C עסקי:  טווח 1.1%–3.33% → אמצע ≈2.22%
B2C_TAKE   = 0.0555           # B2C פרטי:    טווח 3.33%–7.77% → אמצע ≈5.55% (upside — טרם בתמהיל)
B2B2C_MIX, B2B_MIX = 16/26, 10/26     # תמהיל עסקאות (D-006: בסיס יוני = 16 B2B2C + 10 B2B)
DEAL_TAKE  = B2B2C_MIX*B2B2C_TAKE + B2B_MIX*B2B_TAKE   # נתח משוקלל ≈ 2.0%
DEAL_REV   = round(AVG_DEAL_VALUE * DEAL_TAKE)          # ≈ 3,001 ₪ לעסקה (משוקלל)
LEAD_PRICE     = 150          # ₪ לליד שנמכר לספקים (מאושר ע"י המייסד)
ULTRA_PRICE    = 4_500        # ₪/חודש מנוי Ultra — B2B: מידע, ניתוחים מתקדמים וגישה למכרזים מיבואני רכב
MAX_PRICE      = 7_700        # ₪/חודש מנוי Max — פרימיום: עסקאות בכמויות און-ליין
LEADS_PER_DEAL = 5            # יחס יוני: 130 לידים / 26 עסקאות
# עמלת מימון (D-015) — חברת המימון משלמת 1% מערך העסקה על כל עסקה ממומנת; פעיל מספטמבר 26
FIN_ATTACH   = 0.50                                  # 50% מהעסקאות ממומנות
FIN_COMM     = round(AVG_DEAL_VALUE * 0.01)          # ₪1,500 = 1% מערך העסקה
FIN_PER_DEAL = round(FIN_ATTACH * FIN_COMM)          # ≈ 750 ₪/עסקה משוקלל
FIN_START    = (2026, 9)      # ניתוב המימון עולה לאוויר

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

# ---------------- מנוע מנויים (Ultra / Max — D-015) ----------------
subs_total, ultra_subs, max_subs = [], [], []
CHURN = 0.02
for i,(y,m) in enumerate(months):
    if i == 0:
        tot = 15
    else:
        net = 5 if y == 2026 else 7
        tot = subs_total[-1] + net - round(CHURN*subs_total[-1])
    subs_total.append(tot)
    share = 0.25 * i / (N-1)          # נתח Max מטפס 0% → 25%
    mx = round(tot*share)
    max_subs.append(mx)
    ultra_subs.append(tot-mx)

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
LAUNCH_PRORATE = 0.5    # W2: יוני = חצי-חודש השקה — מנויים נצברים, לא משולמים מלא מיום 1
TAX_RATE = 0.23         # W3: מס חברות (אינפורמטיבי — לא מנוכה משורת ה"נטו")
rows, cum = [], OPENING_CASH
for i,(y,m) in enumerate(months):
    leads = deals[i]*LEADS_PER_DEAL
    deal_rev = deals[i]*DEAL_REV
    lead_rev = leads*LEAD_PRICE
    sub_rev  = ultra_subs[i]*ULTRA_PRICE + max_subs[i]*MAX_PRICE
    if i == 0: sub_rev = round(sub_rev * LAUNCH_PRORATE)   # W2: פרו-רייטה לחודש ההשקה
    ad_rev   = ad_k[i]*K
    fin_rev  = deals[i]*FIN_PER_DEAL if (y, m) >= FIN_START else 0
    total_rev= deal_rev+lead_rev+sub_rev+ad_rev+fin_rev
    opex     = (team_k[i]+mkt_k[i]+infra_k[i]+gna_k[i])*K
    net      = total_rev-opex
    cum     += net
    rows.append(dict(period=f"{HEB_MON[m]} {y%100:02d}", y=y, m=m,
        deals=deals[i], leads=leads, subs=subs_total[i], ultra=ultra_subs[i], maxs=max_subs[i],
        deal_rev=deal_rev, lead_rev=lead_rev, sub_rev=sub_rev, ad_rev=ad_rev, fin_rev=fin_rev,
        total_rev=total_rev, opex=opex, team=team_k[i]*K, marketing=mkt_k[i]*K, infra=infra_k[i]*K, gna=gna_k[i]*K,
        net=net, cum=cum, gmv=deals[i]*AVG_DEAL_VALUE))

# ---------------- פלט: CSV ----------------
out_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ULEASE_FORECAST.csv")
with open(out_csv,"w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f)
    w.writerow(["period","deals","leads","subscribers","ultra","max",
                "deal_rev","lead_rev","sub_rev","ad_rev","fin_rev","total_rev","opex","net_monthly","cum_cash","gmv",
                "team","marketing","infra","gna"])
    for r in rows:
        w.writerow([r["period"],r["deals"],r["leads"],r["subs"],r["ultra"],r["maxs"],
            r["deal_rev"],r["lead_rev"],r["sub_rev"],r["ad_rev"],r["fin_rev"],r["total_rev"],r["opex"],r["net"],r["cum"],r["gmv"],
            r["team"],r["marketing"],r["infra"],r["gna"]])

# ---------------- פלט: טבלת Markdown חודשית ----------------
f = lambda n: f"{n:,.0f}"
print('| חודש | עסקאות | לידים | מנויים | הכנ׳ עסקאות | הכנ׳ לידים | הכנ׳ מנויים | פרסום | מימון | סה"כ הכנסה | הוצאות | נטו | Cash מצטבר |')
print('|------|------:|-----:|-----:|----------:|---------:|----------:|-----:|-----:|---------:|------:|----:|----------:|')
for r in rows:
    print(f"| {r['period']} | {r['deals']} | {r['leads']} | {r['subs']} | {f(r['deal_rev'])} | {f(r['lead_rev'])} | {f(r['sub_rev'])} | {f(r['ad_rev'])} | {f(r['fin_rev'])} | {f(r['total_rev'])} | {f(r['opex'])} | {f(r['net'])} | {f(r['cum'])} |")

# ---------------- סיכומים שנתיים ----------------
def agg(yr):
    sel=[r for r in rows if r["y"]==yr]
    return dict(deals=sum(r["deals"] for r in sel), rev=sum(r["total_rev"] for r in sel),
                opex=sum(r["opex"] for r in sel), net=sum(r["net"] for r in sel),
                gmv=sum(r["gmv"] for r in sel), subs=sel[-1]["subs"], fin=sum(r["fin_rev"] for r in sel))
a26, a27 = agg(2026), agg(2027)
print("\n=== סיכום שנתי ===")
print(f"2026 (יוני–דצמ'): עסקאות {a26['deals']:,} | GMV {a26['gmv']:,.0f} | הכנסה {a26['rev']:,.0f} | מזה מימון {a26['fin']:,.0f} | הוצאות {a26['opex']:,.0f} | נטו {a26['net']:,.0f} | מנויים {a26['subs']}")
print(f"2027 (ינו'–דצמ'): עסקאות {a27['deals']:,} | GMV {a27['gmv']:,.0f} | הכנסה {a27['rev']:,.0f} | מזה מימון {a27['fin']:,.0f} | הוצאות {a27['opex']:,.0f} | נטו {a27['net']:,.0f} | מנויים {a27['subs']}")
d = rows[-1]
print(f"\nRun-rate דצמ' 27: הכנסה חודשית {d['total_rev']:,.0f} → שנתי {d['total_rev']*12:,.0f}")
print(f"Cash מצטבר סוף 2027 (כולל גיוס 150K): {d['cum']:,.0f}")
print(f"DEAL_REV/עסקה (משוקלל) = {DEAL_REV:,} ₪  (B2B2C {B2B2C_TAKE:.2%} × {B2B2C_MIX:.0%} + B2B {B2B_TAKE:.2%} × {B2B_MIX:.0%})")
print(f"מרווח 2027 = {a27['net']/a27['rev']:.1%}")
print(f"\n[W3] נטו = רווח תפעולי לפני מס. אחרי מס חברות משוער ({TAX_RATE:.0%}): 2026 ≈ {a26['net']*(1-TAX_RATE):,.0f} · 2027 ≈ {a27['net']*(1-TAX_RATE):,.0f}")
