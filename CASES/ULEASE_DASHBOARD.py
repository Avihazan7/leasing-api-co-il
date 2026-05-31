#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 Leasing.co.il — Executive Dashboard generator
קורא את CASES/ULEASE_FORECAST.csv ומפיק דשבורד HTML עצמאי (RTL, גרפי SVG).
הרצה:  python3 CASES/ULEASE_FORECAST.py && python3 CASES/ULEASE_DASHBOARD.py
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
ACCENT, CREAM, INK = "#c0532b", "#f5f1e8", "#2a2622"
PAL = ["#c0532b", "#e0894f", "#2a6f6b", "#9b8557", "#7a5c3e"]  # deal, lead, sub, ad, uw

# ---------- data ----------
rows = list(csv.DictReader(open(os.path.join(HERE, "ULEASE_FORECAST.csv"), encoding="utf-8-sig")))
for r in rows:
    for k in ("deals","leads","subscribers","deal_rev","lead_rev","sub_rev","ad_rev","uw_rev","total_rev","opex","net_monthly","cum_cash","gmv"):
        r[k] = float(r[k])
y26, y27 = rows[:7], rows[7:]
def ssum(rs, k): return sum(r[k] for r in rs)
K = dict(
    gmv26=ssum(y26,"gmv"), gmv27=ssum(y27,"gmv"),
    rev26=ssum(y26,"total_rev"), rev27=ssum(y27,"total_rev"),
    net26=ssum(y26,"net_monthly"), net27=ssum(y27,"net_monthly"),
    deals26=ssum(y26,"deals"), deals27=ssum(y27,"deals"),
    subs_end=int(rows[-1]["subscribers"]), cash_end=rows[-1]["cum_cash"],
    runrate=rows[-1]["total_rev"]*12,
)
mix27 = {"עסקאות":ssum(y27,"deal_rev"),"לידים":ssum(y27,"lead_rev"),"מנויים":ssum(y27,"sub_rev"),
         "פרסום":ssum(y27,"ad_rev"),"חיתום":ssum(y27,"uw_rev")}

def m(n):  return f"₪{n/1e6:.2f}M" if abs(n)>=1e6 else f"₪{n/1e3:.0f}K"
def f(n):  return f"{n:,.0f}"

# ---------- svg helpers ----------
def svg_bars(vals, labels, color=ACCENT, w=960, h=230, pad=24, sep=7):
    mx=max(vals) or 1; n=len(vals); bw=(w-2*pad)/n; out=[]
    for i,v in enumerate(vals):
        bh=(h-2*pad)*(v/mx); x=pad+i*bw; y=h-pad-bh
        out.append(f'<rect x="{x+bw*0.12:.1f}" y="{y:.1f}" width="{bw*0.76:.1f}" height="{bh:.1f}" rx="2" fill="{color}"><title>{labels[i]}: {v:,.0f}</title></rect>')
    base=f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="#ccc"/>'
    sx=pad+sep*bw; s=f'<line x1="{sx:.1f}" y1="{pad}" x2="{sx:.1f}" y2="{h-pad}" stroke="{ACCENT}" stroke-dasharray="4" opacity=".4"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" preserveAspectRatio="xMidYMid meet">{base}{s}{"".join(out)}</svg>'

def svg_line(vals, color="#2f7d4f", w=960, h=230, pad=24):
    mx=max(vals) or 1; n=len(vals); pts=[]
    for i,v in enumerate(vals):
        x=pad+(w-2*pad)*(i/(n-1)); y=h-pad-(h-2*pad)*(v/mx); pts.append((x,y))
    poly=f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="3"/>'
    area=f'<polygon points="{pad},{h-pad} '+" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)+f' {w-pad},{h-pad}" fill="{color}" opacity=".08"/>'
    dots="".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{color}"><title>{vals[i]:,.0f}</title></circle>' for i,(x,y) in enumerate(pts))
    base=f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="#ccc"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%">{base}{area}{poly}{dots}</svg>'

def svg_stacked(parts, w=960, h=54):
    tot=sum(parts.values()) or 1; x=0; segs=[]
    for (l,v),c in zip(parts.items(), PAL):
        ws=w*(v/tot); segs.append(f'<rect x="{x:.1f}" y="0" width="{ws:.1f}" height="{h}" fill="{c}"><title>{l}: {v:,.0f} ({v/tot*100:.0f}%)</title></rect>'); x+=ws
    return f'<svg viewBox="0 0 {w} {h}" width="100%">{"".join(segs)}</svg>'

# ---------- html parts ----------
labels=[r["period"] for r in rows]
cards=[("GMV 2027",m(K["gmv27"]),"₪260.5M מצטבר"),("הכנסה 2027",m(K["rev27"]),f"2026: {m(K['rev26'])}"),
       ("נטו 2027",m(K["net27"]),f"2026: {m(K['net26'])}"),("Run-rate דצמ' 27",m(K["runrate"]),"שנתי"),
       ("עסקאות 2027",f(K["deals27"]),f"2026: {f(K['deals26'])}"),("מנויים",str(K["subs_end"]),"סוף 2027"),
       ("Cash מצטבר",m(K["cash_end"]),"כולל גיוס ₪150K"),("עמלת עסקה",m(4995),"3.33% × ₪150K")]
card_html="".join(f'<div class="card"><div class="cap">{c[0]}</div><div class="big">{c[1]}</div><div class="sub">{c[2]}</div></div>' for c in cards)
legend="".join(f'<span class="lg"><i style="background:{PAL[i]}"></i>{l}</span>' for i,l in enumerate(mix27))
table_rows="".join(
    f"<tr><td>{r['period']}</td><td>{f(r['deals'])}</td><td>{f(r['total_rev'])}</td><td>{f(r['net_monthly'])}</td><td>{f(r['cum_cash'])}</td></tr>"
    for r in rows)

HTML = f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>ULease 🎯 — Dashboard</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:{INK};font-family:Arial,'Helvetica Neue',sans-serif;color:{INK};padding:20px}}
.wrap{{max-width:1100px;margin:0 auto}}
header{{background:{CREAM};border-radius:16px;padding:24px 28px;margin-bottom:16px}}
header h1{{color:{ACCENT};font-size:2rem}} header p{{opacity:.7;margin-top:4px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}}
.card{{background:{CREAM};border-radius:14px;padding:16px;border-top:3px solid {ACCENT}}}
.card .cap{{font-size:.8rem;opacity:.65}} .card .big{{font-size:1.6rem;font-weight:800;color:{ACCENT};margin:4px 0}}
.card .sub{{font-size:.8rem;opacity:.6}}
.panel{{background:{CREAM};border-radius:16px;padding:20px 24px;margin-bottom:16px}}
.panel h2{{color:{ACCENT};font-size:1.15rem;margin-bottom:12px}}
.lg{{display:inline-flex;align-items:center;font-size:.85rem;margin-left:14px}} .lg i{{width:12px;height:12px;border-radius:3px;display:inline-block;margin-left:6px}}
table{{width:100%;border-collapse:collapse;font-size:.9rem}} th,td{{padding:.4rem .6rem;text-align:right;border-bottom:1px solid #ddd}} th{{color:{ACCENT}}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
ul{{list-style:none}} li{{padding:.25rem 0;padding-right:1.1rem;position:relative;font-size:.92rem}}
li::before{{content:'';position:absolute;right:0;top:.7em;width:.45rem;height:.45rem;background:{ACCENT};border-radius:50%}}
.pill{{display:inline-block;background:#fff;border:1px solid {ACCENT};color:{ACCENT};border-radius:20px;padding:.2rem .7rem;font-size:.8rem;margin:.15rem}}
.flag{{background:#fff3ee;border-right:3px solid {ACCENT};padding:.5rem .8rem;border-radius:6px;font-size:.88rem;margin-top:8px}}
small{{opacity:.55}} @media(max-width:760px){{.grid{{grid-template-columns:repeat(2,1fr)}}.two{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">

<header><h1>ULease 🎯 Leasing.co.il — Executive Dashboard</h1>
<p>Marketplace תלת-צדדי לרכב חדש · Base Case v1.2 (כולל חיתום) · יוני 2026 → דצמבר 2027</p></header>

<div class="grid">{card_html}</div>

<div class="panel"><h2>📈 הכנסה חודשית (₪)</h2>{svg_bars([r['total_rev'] for r in rows], labels)}
<small>הקו המקווקו = מעבר 2026→2027 · רחף לפרטים</small></div>

<div class="panel"><h2>💰 מזומן מצטבר (₪, כולל גיוס 150K)</h2>{svg_line([r['cum_cash'] for r in rows])}</div>

<div class="panel"><h2>🚗 עסקאות לחודש</h2>{svg_bars([r['deals'] for r in rows], labels, color="#2a6f6b")}</div>

<div class="panel"><h2>🧩 תמהיל הכנסות 2027</h2>{svg_stacked(mix27)}<div style="margin-top:10px">{legend}</div></div>

<div class="two">
<div class="panel"><h2>🔺 מבנה ה-Marketplace</h2><ul>
<li><b>היצע:</b> יבואנים · ליסינג · מימון → API</li>
<li><b>ביקוש:</b> פרטי · B2B2C</li>
<li><b>מפיצים:</b> דילרים/ליסינג קטנים (מנויים)</li></ul>
<h2 style="margin-top:14px">💵 מנועי הכנסה</h2>
<span class="pill">עסקה 3.33% ≈ ₪4,995</span><span class="pill">ליד ₪150</span>
<span class="pill">Pro ₪4,500</span><span class="pill">Pro Max ₪7,700</span>
<span class="pill">חיתום ~₪990/עסקה</span><span class="pill">פרסום</span></div>

<div class="panel"><h2>🧠 ארכיטקטורה מתודולוגית</h2><ul>
<li>תורת המשחקים — מכרז מחיר-שני</li>
<li>העשרה אינסטרומנטלית (Feuerstein)</li>
<li>Big Five — התאמת קונה</li>
<li>מו"מ מבוסס-אינטרסים (BATNA/Win-Win)</li>
<li>Multi-agent: Ultra · Master · Max</li></ul></div>
</div>

<div class="two">
<div class="panel"><h2>⚙️ Outbound Engine (יעדי KPI)</h2><ul>
<li>Reply Rate: 15–25% · Meeting Rate: 30–45%</li>
<li>8 שכבות · Haiku (ניקוד/סיווג) · Sonnet (כתיבה)</li>
<li>שלד n8n מוכן לייבוא</li></ul></div>

<div class="panel"><h2>👥 צוות · גיוס</h2><ul>
<li>שירי הלפישטיין — Super COO (מחזיקת מניות)</li>
<li>אברהם בר יוחאי חזן — מו"פ ושיווק</li>
<li>גיוס: מנהל מערכות טכנולוגיה ⬅️ הפער</li>
<li>Cap: 37/37/13/13 · גיוס <b>₪150K</b></li></ul></div>
</div>

<div class="panel"><h2>🗓️ תחזית חודשית מלאה</h2>
<table><thead><tr><th>חודש</th><th>עסקאות</th><th>הכנסה ₪</th><th>נטו ₪</th><th>Cash ₪</th></tr></thead>
<tbody>{table_rows}</tbody></table></div>

<div class="panel"><h2>🚀 סטטוס השקה</h2><ul>
<li>יעד: לאוויר חצי-שני יוני 2026 · MVP תוך שבועיים</li>
<li>בסיס: 26 עסקאות · 130 לידים · 15 מנויים · 7 ספקים</li></ul>
<div class="flag">🔴 לפני השקה: ייעוץ משפטי לחיתום מימון/ביטוח · חוק ספאם ל-outreach · גיוס Tech Lead</div></div>

<div class="panel"><small>מקור: CASES/ULEASE_FORECAST.csv (Base Case v1.2) · הנחות ניתנות לכיול ב-ULEASE_FORECAST.py · מנגנוני ליבה (Deal Score/Match/תמחור) = IP · Claude Operating System — Avraham Bar Yochai Chazan</small></div>

</div></body></html>"""

out = os.path.join(HERE, "ULEASE_DASHBOARD.html")
open(out, "w", encoding="utf-8").write(HTML)
print(f"דשבורד נוצר → ULEASE_DASHBOARD.html · {len(rows)} חודשים · הכנסה 2027 {m(K['rev27'])} · run-rate {m(K['runrate'])}")
