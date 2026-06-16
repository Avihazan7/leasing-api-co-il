#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 Leasing.co.il — Executive Cockpit Dashboard generator
=================================================================
קורא את CASES/ULEASE_FORECAST.csv ומפיק דשבורד HTML עצמאי (RTL) בשפת עיצוב של
קוקפיט רכב-יוקרה (Hyperscreen): מצב-נהיגה (HUD), אשכול מחוונים מעגליים זוהרים
(Run-rate · הכנסה · מרווח), מד-טעינה למזומן, מסך מרכזי עם טאבים (הכנסה/עסקאות/
מזומן/תמהיל), קונסולת DRIVE-MODE (What-If קצב×מט"ח), ומסכי-עומק: Funnel,
Arbitrage, Unit-Economics חי, TAM/SAM/SOM, AI Agents, הוצאות, תרחישים,
צ'קליסט השקה, תחזית מלאה וטיימליין. כל הנתונים מחווטים מהמודל הפיננסי.
הרצה:  python3 CASES/ULEASE_FORECAST.py && python3 CASES/ULEASE_DASHBOARD.py
"""
import csv, os, math

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- לוח-צבעים: קוקפיט EV יוקרתי (שחור עמוק · זוהר ציאן/כחול · מותג ULease ענבר/זהב) ----
BG0, BG1 = "#04070c", "#0a0f17"
CYAN, BLUE, AMBER, GOLD = "#34d6ef", "#3f9be8", "#f2a85c", "#dcb56a"
GREEN, VIOLET, RED = "#41e0a3", "#9a86f2", "#f0746e"
TXT, MUTE = "#e9eff7", "rgba(233,239,247,.55)"
LINE, LINE2 = "rgba(120,180,220,.10)", "rgba(120,180,220,.28)"
COLS = [CYAN, AMBER, GREEN, VIOLET, GOLD]

# ---------------- נתונים (זהה למקור — מחווט למודל הפיננסי) ----------------
rows = list(csv.DictReader(open(os.path.join(HERE, "ULEASE_FORECAST.csv"), encoding="utf-8-sig")))
NUM = ("deals","leads","subscribers","deal_rev","lead_rev","sub_rev","ad_rev","fin_rev",
       "total_rev","opex","net_monthly","cum_cash","gmv","team","marketing","infra","gna")
for r in rows:
    for k in NUM: r[k] = float(r[k])
y26, y27 = rows[:7], rows[7:]
S = lambda rs,k: sum(r[k] for r in rs)
K = dict(gmv27=S(y27,"gmv"), rev26=S(y26,"total_rev"), rev27=S(y27,"total_rev"),
         net26=S(y26,"net_monthly"), net27=S(y27,"net_monthly"), opex27=S(y27,"opex"),
         deals26=S(y26,"deals"), deals27=S(y27,"deals"), subs_end=int(rows[-1]["subscribers"]),
         cash_end=rows[-1]["cum_cash"], runrate=rows[-1]["total_rev"]*12)
K["margin27"] = K["net27"]/K["rev27"] if K["rev27"] else 0
mix27 = {"עסקאות":S(y27,"deal_rev"),"לידים":S(y27,"lead_rev"),"מנויים":S(y27,"sub_rev"),"פרסום":S(y27,"ad_rev"),"מימון":S(y27,"fin_rev")}
exp27 = {"צוות":S(y27,"team"),"שיווק":S(y27,"marketing"),"תשתית":S(y27,"infra"),"תקורה":S(y27,"gna")}

def _scen(mult):
    cum=150000.0; r26=r27=n26=n27=last=0.0
    for i,r in enumerate(rows):
        dd=r['deal_rev']+r['lead_rev']+r['fin_rev']; ind=r['sub_rev']+r['ad_rev']
        t=mult*dd+ind; nt=t-r['opex']; cum+=nt; last=t
        if i<7: r26+=t; n26+=nt
        else: r27+=t; n27+=nt
    return dict(r27=r27,n27=n27,cash=cum,rr=last*12)
SCEN=[("שמרני",0.7,GOLD),("בסיס",1.0,AMBER),("אופטימי",1.3,GREEN)]
scen={nm:_scen(mu) for nm,mu,_ in SCEN}

leads27=int(S(y27,"leads")); deals27i=int(K["deals27"]); deliv27=round(deals27i*0.95)
B={"deal":S(y27,"deal_rev"),"lead":S(y27,"lead_rev"),"sub":S(y27,"sub_rev"),"ad":S(y27,"ad_rev"),"fin":S(y27,"fin_rev"),"opex":K["opex27"]}
take_blended=K["rev27"]/K["gmv27"] if K["gmv27"] else 0
mkt27=S(y27,"marketing"); cac=mkt27/deals27i if deals27i else 0
contrib=4995+990; cpl=mkt27/leads27 if leads27 else 0
maxdeals=int(max(r["deals"] for r in rows))
labels=[r["period"] for r in rows]

def m(n): return f"₪{n/1e6:.2f}M" if abs(n)>=1e6 else f"₪{n/1e3:.0f}K"
def f(n): return f"{n:,.0f}"

# ---------------- SVG: גיאומטריה + מחוונים ----------------
def _pol(cx,cy,r,a):
    rad=math.radians(a); return cx+r*math.cos(rad), cy+r*math.sin(rad)
def _arc(cx,cy,r,a0,a1):
    x0,y0=_pol(cx,cy,r,a0); x1,y1=_pol(cx,cy,r,a1)
    large=1 if (a1-a0)>180 else 0
    return f"M{x0:.2f} {y0:.2f} A{r:.2f} {r:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}"

def gauge(frac, big, label, col=CYAN, sub="", size=260):
    """מד מעגלי בסגנון מד-מהירות: קשת זוהרת + מחט + קריאה מרכזית."""
    frac=max(0.0,min(1.0,frac)); cx=cy=size/2; r=size/2-26; A0,SPAN=135,270; a1=A0+frac*SPAN
    ticks="".join(
        (lambda p: f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{p[2]:.1f}" y2="{p[3]:.1f}" stroke="{LINE2}" stroke-width="{3 if i%5==0 else 1.5}"/>')(
            (*_pol(cx,cy,r-3,A0+SPAN*i/20), *_pol(cx,cy,r-(15 if i%5==0 else 9),A0+SPAN*i/20)))
        for i in range(21))
    nx,ny=_pol(cx,cy,r-18,a1)
    needle=(f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{col}" stroke-width="3.5" '
            f'stroke-linecap="round" filter="url(#glow)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="{col}" filter="url(#glow)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{BG0}"/>')
    subt=f'<text x="{cx}" y="{cy+44}" text-anchor="middle" class="g-sub">{sub}</text>' if sub else ""
    return (f'<svg viewBox="0 0 {size} {size}" class="gauge">'
            f'<path d="{_arc(cx,cy,r,A0,A0+SPAN)}" fill="none" stroke="rgba(255,255,255,.06)" stroke-width="13" stroke-linecap="round"/>'
            f'<path d="{_arc(cx,cy,r,A0,a1)}" fill="none" stroke="{col}" stroke-width="13" stroke-linecap="round" filter="url(#glow)"/>'
            f'{ticks}{needle}'
            f'<text x="{cx}" y="{cy+2}" text-anchor="middle" class="g-big">{big}</text>'
            f'<text x="{cx}" y="{cy+26}" text-anchor="middle" class="g-lab">{label}</text>{subt}</svg>')

def battery(pct, n=16):
    pct=max(0.0,min(1.0,pct)); fill=round(pct*n)
    return "".join(f'<i class="bseg{" on" if i<fill else ""}"></i>' for i in range(n))

def svg_bars(vals, labels, grad="barCyan", w=960, h=210, pad=24, sep=7):
    mx=max(vals) or 1; n=len(vals); bw=(w-2*pad)/n; out=[]
    grid="".join(f'<line x1="{pad}" y1="{pad+(h-2*pad)*g/4:.1f}" x2="{w-pad}" y2="{pad+(h-2*pad)*g/4:.1f}" stroke="{LINE}"/>' for g in range(5))
    for i,v in enumerate(vals):
        bh=(h-2*pad)*(v/mx); x=pad+i*bw; y=h-pad-bh
        out.append(f'<rect x="{x+bw*0.14:.1f}" y="{y:.1f}" width="{bw*0.72:.1f}" height="{bh:.1f}" rx="3" fill="url(#{grad})" filter="url(#glowSoft)"><title>{labels[i]}: {v:,.0f}</title></rect>')
    base=f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="{LINE2}"/>'
    sx=pad+sep*bw; s=f'<line x1="{sx:.1f}" y1="{pad}" x2="{sx:.1f}" y2="{h-pad}" stroke="{AMBER}" stroke-dasharray="3 5" opacity=".55" filter="url(#glow)"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" preserveAspectRatio="xMidYMid meet">{grid}{base}{s}{"".join(out)}</svg>'

def svg_line(vals, col=GREEN, grad="areaGreen", w=960, h=210, pad=24, suffix=""):
    mx=max(vals) or 1; n=len(vals); pts=[(pad+(w-2*pad)*(i/(n-1)), h-pad-(h-2*pad)*(v/mx)) for i,v in enumerate(vals)]
    grid="".join(f'<line x1="{pad}" y1="{pad+(h-2*pad)*g/4:.1f}" x2="{w-pad}" y2="{pad+(h-2*pad)*g/4:.1f}" stroke="{LINE}"/>' for g in range(5))
    poly=f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="none" stroke="{col}" stroke-width="3" stroke-linejoin="round" filter="url(#glow)"/>'
    area=f'<polygon points="{pad},{h-pad} '+" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)+f' {w-pad},{h-pad}" fill="url(#{grad})"/>'
    dots="".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{col}" filter="url(#glow)"><title>{vals[i]:,.0f}{suffix}</title></circle>' for i,(x,y) in enumerate(pts))
    base=f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="{LINE2}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%">{grid}{base}{area}{poly}{dots}</svg>'

def svg_stacked(parts, w=960, h=46):
    tot=sum(parts.values()) or 1; x=2.0; segs=[]
    for (l,v),c in zip(parts.items(), COLS):
        ws=(w-4)*(v/tot); segs.append(f'<rect x="{x:.1f}" y="0" width="{max(0,ws-4):.1f}" height="{h}" rx="7" fill="{c}" filter="url(#glowSoft)" opacity=".92"><title>{l}: {v:,.0f} ({v/tot*100:.0f}%)</title></rect>'); x+=ws
    return f'<svg viewBox="0 0 {w} {h}" width="100%">{"".join(segs)}</svg>'

def legend(parts): return "".join(f'<span class="lg"><i style="background:{COLS[i]}"></i>{l} ({v/sum(parts.values())*100:.0f}%)</span>' for i,(l,v) in enumerate(parts.items()))

def svg_scen(w=960, h=230, pad=38):
    vals=[scen[nm]['n27'] for nm,_,_ in SCEN]; mx=max(vals) or 1; n=len(SCEN); bw=(w-2*pad)/n; out=[]
    for i,(nm,mu,c) in enumerate(SCEN):
        v=scen[nm]['n27']; bh=(h-2*pad)*(v/mx); x=pad+i*bw+bw*0.22; y=h-pad-bh
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw*0.56:.1f}" height="{bh:.1f}" rx="5" fill="{c}" filter="url(#glowSoft)"/>')
        out.append(f'<text x="{x+bw*0.28:.1f}" y="{y-9:.1f}" text-anchor="middle" class="sc-v" fill="{c}">{v/1e6:.1f}M</text>')
        out.append(f'<text x="{x+bw*0.28:.1f}" y="{h-pad+20:.1f}" text-anchor="middle" class="sc-l">{nm} ×{mu:g}</text>')
    base=f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="{LINE2}"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%">{base}{"".join(out)}</svg>'

# ---------------- בלוקים מחושבים ----------------
cards=[("GMV 2027",m(K["gmv27"]),"מצטבר"),("הכנסה 2027",m(K["rev27"]),f"2026: {m(K['rev26'])}"),
       ("נטו 2027",m(K["net27"]),f"מרווח {K['margin27']*100:.0f}%"),("הוצאות 2027",m(K["opex27"]),"opex"),
       ("Run-rate דצמ' 27",m(K["runrate"]),"שנתי"),("עסקאות 2027",f(K["deals27"]),f"2026: {f(K['deals26'])}"),
       ("מנויים",str(K["subs_end"]),"סוף 2027"),("Cash מצטבר",m(K["cash_end"]),"כולל ₪150K")]
kpi_html="".join(f'<div class="kpi"><div class="cap">{c[0]}</div><div class="big">{c[1]}</div><div class="sub">{c[2]}</div></div>' for c in cards)
table_rows="".join(f"<tr><td>{r['period']}</td><td>{f(r['deals'])}</td><td>{m(r['total_rev'])}</td><td>{m(r['opex'])}</td><td>{m(r['net_monthly'])}</td><td>{m(r['cum_cash'])}</td></tr>" for r in rows)

def funnel_html():
    stages=[("לידים",leads27,BLUE),("עסקאות",deals27i,AMBER),("מסירות",deliv27,GREEN)]; mx=stages[0][1]; out=[]; prev=None
    for nm,v,c in stages:
        w=22+78*(v/mx); conv=f" · {v/prev*100:.0f}% מהקודם" if prev else ""
        out.append(f'<div class="seg" style="width:{w:.0f}%;background:{c}">{nm}: {v:,}{conv}</div>'); prev=v
    return '<div class="funnel">'+''.join(out)+'</div>'

TL=[("יוני · שבוע 1","חברה + דומיין + תשתית + ingestion"),("יוני · שבוע 2","חדר-עסקה + מנויים + QA"),
    ("חצי-שני יוני 26","🚀 Go-Live — 26 עסקאות"),("Q3–Q4 2026","Scale: מכרז · מנוי Max · n8n"),("2027","Architect + צמיחה")]
tl_html="".join(f'<div class="step"><b>{t}</b>{d}</div>' for t,d in TL)

CHECKLIST = [("דומיין",["רכישת ULease.co.il","חיבור Leasing.co.il","DNS + SSL + מייל"]),
             ("משפטי",["הקמת חברה","תקנון + מדיניות פרטיות","ייעוץ משפטי לחיתום","עמידה בחוק ספאם"]),
             ("MVP",["אתר + אפליקציה לאוויר","Ingestion (API/CSV)","חדר-עסקה (חתימה+מקדמה)","מנויי Ultra + חיוב","Admin בסיסי"]),
             ("תוכן + Outreach",["מלאי 7 ספקים טעון","Landing + הצעת ערך","שלד n8n ב-assist"]),
             ("QA → Go-Live",["עסקה מקצה-לקצה עברה","תשלום/מקדמה נבדק","גיוס Tech Lead"])]
cl_html=""
for head,items in CHECKLIST:
    cl_html+=f'<div class="clhead">{head}</div>'
    cl_html+="".join(f'<label class="chk"><input type="checkbox"> {it}</label>' for it in items)

# ---------------- DEFS גלובליים (gradients + glow) ----------------
DEFS=(f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
      f'<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
      f'<filter id="glowSoft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
      f'<linearGradient id="barCyan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".12"/></linearGradient>'
      f'<linearGradient id="barBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".12"/></linearGradient>'
      f'<linearGradient id="barAmber" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}"/><stop offset="1" stop-color="{AMBER}" stop-opacity=".12"/></linearGradient>'
      f'<linearGradient id="barGreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{GREEN}" stop-opacity=".12"/></linearGradient>'
      f'<linearGradient id="areaGreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".34"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>'
      f'<linearGradient id="areaAmber" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity=".30"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>'
      f'</defs></svg>')

# ---------------- CSS ----------------
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--cy:#34d6ef;--am:#f2a85c;--gr:#41e0a3;--txt:#e9eff7;--mute:rgba(233,239,247,.55)}
html{scroll-behavior:smooth}
body{background:radial-gradient(120% 90% at 50% -10%,#0c1626 0%,#070b12 45%,#04070c 100%);
 font-family:'Heebo',system-ui,'Segoe UI',Arial,sans-serif;color:var(--txt);
 padding:18px;min-height:100vh;overflow-x:hidden}
.ambient{position:fixed;inset:0;z-index:-1;pointer-events:none;overflow:hidden}
.ambient::before,.ambient::after{content:'';position:absolute;border-radius:50%;filter:blur(90px);opacity:.5}
.ambient::before{width:70vw;height:42vh;left:-10vw;top:-12vh;background:radial-gradient(circle,#1f7fd1,transparent 70%);animation:drift1 14s ease-in-out infinite alternate}
.ambient::after{width:60vw;height:40vh;right:-8vw;bottom:-10vh;background:radial-gradient(circle,#c0532b,transparent 70%);opacity:.32;animation:drift2 17s ease-in-out infinite alternate}
@keyframes drift1{to{transform:translate(6vw,4vh) scale(1.1)}}
@keyframes drift2{to{transform:translate(-5vw,-3vh) scale(1.12)}}
.wrap{max-width:1180px;margin:0 auto}
.num{font-family:'Rajdhani','Heebo',sans-serif;font-weight:700;letter-spacing:.5px}

/* ---- HUD status bar ---- */
.hud{display:flex;align-items:center;justify-content:space-between;gap:14px;
 background:linear-gradient(180deg,rgba(20,30,44,.85),rgba(12,18,28,.7));
 border:1px solid rgba(120,180,220,.22);border-radius:16px;padding:12px 20px;margin-bottom:16px;
 backdrop-filter:blur(14px);box-shadow:0 1px 0 rgba(255,255,255,.06) inset,0 16px 40px rgba(0,0,0,.5),0 0 0 1px rgba(52,214,239,.05);position:relative;animation:rise .6s both}
.hud::after{content:'';position:absolute;left:18px;right:18px;bottom:-1px;height:2px;border-radius:2px;
 background:linear-gradient(90deg,transparent,var(--cy),#3f9be8,transparent);box-shadow:0 0 14px var(--cy);opacity:.8}
.brand{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.5rem;letter-spacing:1px;
 background:linear-gradient(90deg,#fff,var(--cy) 55%,var(--am));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.brand small{display:block;font-size:.62rem;letter-spacing:5px;color:var(--mute);-webkit-text-fill-color:initial;font-family:'Heebo'}
.hud .ico{display:flex;align-items:center;gap:14px;font-size:.82rem;color:var(--mute)}
.hud .chip{display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(120,180,220,.25);border-radius:20px;padding:4px 12px;color:var(--cy)}
.hud .dot{width:8px;height:8px;border-radius:50%;background:var(--gr);box-shadow:0 0 10px var(--gr);animation:pulse 2.4s infinite}
#clock{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.35rem;color:#fff;letter-spacing:2px}
@keyframes pulse{50%{opacity:.4}}

/* ---- cockpit cluster ---- */
.cockpit{background:linear-gradient(180deg,rgba(14,22,34,.7),rgba(7,11,18,.78));
 border:1px solid rgba(120,180,220,.2);border-radius:26px;padding:24px 20px 18px;margin-bottom:16px;position:relative;overflow:hidden;
 box-shadow:0 1px 0 rgba(255,255,255,.07) inset,0 24px 60px rgba(0,0,0,.55);animation:rise .7s both}
.cockpit::before{content:'';position:absolute;inset:0 0 auto 0;height:46%;background:radial-gradient(120% 100% at 50% 0,rgba(52,214,239,.1),transparent 70%);pointer-events:none}
.cluster{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap}
.gw{text-align:center;position:relative;flex:1;min-width:170px;max-width:210px}
.gw.big{max-width:300px;flex:1.3}
.gw .tag{font-family:'Rajdhani',sans-serif;letter-spacing:3px;font-size:.66rem;color:var(--mute);margin-bottom:-6px}
.gauge{width:100%;height:auto;display:block;filter:drop-shadow(0 8px 22px rgba(0,0,0,.5))}
.g-big{fill:#fff;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:30px;letter-spacing:.5px}
.gw.big .g-big{font-size:38px}
.g-lab{fill:var(--mute);font-family:'Heebo';font-size:12px}
.g-sub{fill:var(--cy);font-family:'Rajdhani';font-size:12px;letter-spacing:1px}
.battery{margin:14px auto 2px;max-width:760px;background:rgba(8,13,20,.6);border:1px solid rgba(120,180,220,.18);border-radius:16px;padding:12px 16px;display:flex;align-items:center;gap:14px}
.battery .lab{font-size:.78rem;color:var(--mute);white-space:nowrap}
.battery .lab b{display:block;font-family:'Rajdhani';font-size:1.35rem;color:#fff}
.bat{display:flex;gap:3px;flex:1;height:26px}
.bseg{flex:1;border-radius:3px;background:rgba(255,255,255,.06)}
.bseg.on{background:linear-gradient(180deg,#7af0c4,var(--gr));box-shadow:0 0 10px rgba(65,224,163,.7)}
.bolt{color:var(--gr);font-size:1.3rem;text-shadow:0 0 12px var(--gr)}

/* ---- KPI widget tiles ---- */
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}
.kpi{background:linear-gradient(180deg,rgba(18,27,40,.72),rgba(10,16,25,.72));border:1px solid rgba(120,180,220,.16);
 border-radius:16px;padding:15px 16px;backdrop-filter:blur(12px);position:relative;overflow:hidden;animation:rise .6s both;transition:.25s}
.kpi::before{content:'';position:absolute;top:0;right:0;width:34%;height:3px;background:linear-gradient(90deg,transparent,var(--cy));box-shadow:0 0 10px var(--cy)}
.kpi:hover{transform:translateY(-3px);border-color:rgba(52,214,239,.4);box-shadow:0 16px 34px rgba(0,0,0,.4)}
.kpi .cap{font-size:.76rem;color:var(--mute)}
.kpi .big{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.7rem;margin:3px 0;
 background:linear-gradient(90deg,#fff,var(--cy));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.kpi .sub{font-size:.72rem;color:var(--mute)}

/* ---- screens (glass panels) ---- */
.screen{background:linear-gradient(180deg,rgba(16,24,37,.66),rgba(8,13,21,.7));border:1px solid rgba(120,180,220,.16);
 border-radius:18px;padding:20px 22px;margin-bottom:16px;backdrop-filter:blur(14px);position:relative;
 box-shadow:0 1px 0 rgba(255,255,255,.05) inset,0 18px 40px rgba(0,0,0,.4);animation:rise .6s both}
.screen h2{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.15rem;letter-spacing:.5px;color:#fff;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.screen h2::before{content:'';width:9px;height:9px;border-radius:50%;background:var(--cy);box-shadow:0 0 12px var(--cy)}
small{color:var(--mute);font-size:.8rem}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}

/* ---- hyperscreen tabs ---- */
.hsbar{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap}
.tab{font-family:'Rajdhani',sans-serif;font-weight:500;letter-spacing:1px;cursor:pointer;color:var(--mute);
 border:1px solid rgba(120,180,220,.2);border-radius:12px;padding:7px 16px;font-size:.9rem;background:rgba(8,13,20,.5);transition:.2s}
.tab:hover{color:var(--txt)}
.tab.on{color:#04070c;background:linear-gradient(90deg,var(--cy),#3f9be8);border-color:transparent;box-shadow:0 0 18px rgba(52,214,239,.5);font-weight:700}
.view{display:none;animation:fade .4s both}.view.on{display:block}
@keyframes fade{from{opacity:0}}

/* ---- DRIVE-MODE console ---- */
.console{display:grid;grid-template-columns:1.1fr 1fr;gap:18px;align-items:center}
.dials{display:flex;justify-content:center;gap:24px;flex-wrap:wrap}
.dial{width:138px;text-align:center}
.dial .ring{width:138px;height:138px;border-radius:50%;display:grid;place-items:center;position:relative;margin:0 auto;
 background:conic-gradient(var(--cy) calc(var(--p,50)*1%),rgba(255,255,255,.07) 0);
 -webkit-mask:radial-gradient(transparent 54%,#000 55%);mask:radial-gradient(transparent 54%,#000 55%)}
.dial .ico{position:absolute;font-family:'Rajdhani';font-weight:700;font-size:1.45rem;color:#fff;-webkit-mask:none;mask:none}
.dial .nm{font-size:.78rem;color:var(--mute);margin-top:8px}
.ctrl{display:flex;flex-direction:column;gap:16px}
.ctrl label{font-size:.88rem;color:var(--mute)}.ctrl label b{color:var(--cy);font-family:'Rajdhani';font-size:1.05rem}
input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:6px;border-radius:6px;
 background:linear-gradient(90deg,var(--cy),#3f9be8);outline:none;margin-top:8px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;border-radius:50%;
 background:#0a0f17;border:2px solid var(--cy);box-shadow:0 0 12px var(--cy);cursor:pointer}
input[type=range]::-moz-range-thumb{width:22px;height:22px;border-radius:50%;background:#0a0f17;border:2px solid var(--cy);box-shadow:0 0 12px var(--cy);cursor:pointer}
.out{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.out>div{background:rgba(8,13,20,.55);border:1px solid rgba(120,180,220,.14);border-radius:12px;padding:11px;text-align:center}
.out small{color:var(--mute);font-size:.72rem}
.out b{font-family:'Rajdhani',sans-serif;color:var(--cy);font-size:1.2rem;display:block;margin-top:3px}

/* ---- shared bits ---- */
.lg{display:inline-flex;align-items:center;font-size:.82rem;margin-left:14px;color:var(--mute)}.lg i{width:12px;height:12px;border-radius:3px;display:inline-block;margin-left:6px}
.funnel{display:flex;flex-direction:column;gap:7px;align-items:center}
.funnel .seg{color:#04070c;border-radius:8px;padding:.6rem;text-align:center;font-size:.86rem;font-weight:700;font-family:'Heebo';box-shadow:0 0 18px rgba(52,214,239,.25)}
.pill{display:inline-block;background:rgba(52,214,239,.08);border:1px solid rgba(52,214,239,.35);color:var(--cy);border-radius:20px;padding:.22rem .7rem;font-size:.78rem;margin:.18rem}
.flag{background:linear-gradient(90deg,rgba(242,168,92,.12),transparent);border-right:3px solid var(--am);padding:.6rem .9rem;border-radius:8px;font-size:.84rem;margin-top:10px;color:#f3d9bf}
ul{list-style:none}li{padding:.26rem 0;padding-right:1.2rem;position:relative;font-size:.9rem}
li::before{content:'';position:absolute;right:0;top:.62em;width:.5rem;height:.5rem;background:var(--cy);border-radius:50%;box-shadow:0 0 8px var(--cy)}
.tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{width:100%;border-collapse:collapse;font-size:.88rem}
th,td{padding:.42rem .6rem;text-align:right;border-bottom:1px solid rgba(120,180,220,.12);white-space:nowrap}
th{color:var(--cy);font-family:'Rajdhani';font-weight:500;letter-spacing:.5px}
tbody tr:hover{background:rgba(52,214,239,.05)}
.sc-v{font-family:'Rajdhani';font-weight:700;font-size:16px}.sc-l{fill:var(--mute);font-family:'Heebo';font-size:12px}
.chk{display:flex;align-items:center;gap:9px;font-size:.9rem;padding:.2rem 0;cursor:pointer;color:var(--txt)}
.chk input{width:17px;height:17px;accent-color:var(--cy)}
.clhead{font-family:'Rajdhani';font-weight:700;letter-spacing:1px;color:var(--am);margin-top:12px;font-size:.86rem}
.prog{background:rgba(8,13,20,.7);border:1px solid rgba(120,180,220,.18);border-radius:20px;height:22px;overflow:hidden;margin:8px 0 4px}
.prog>div{background:linear-gradient(90deg,var(--cy),#3f9be8);height:100%;width:0;transition:width .4s;box-shadow:0 0 16px var(--cy)}
#clpct{font-family:'Rajdhani';font-weight:700;color:var(--cy)}
.tl{display:flex;gap:10px;overflow-x:auto;padding-bottom:8px}
.tl .step{flex:1;min-width:145px;background:rgba(8,13,20,.55);border:1px solid rgba(120,180,220,.16);border-top:3px solid var(--cy);border-radius:12px;padding:12px;font-size:.82rem}
.tl .step b{font-family:'Rajdhani';color:var(--cy);display:block;margin-bottom:4px;letter-spacing:.5px}
.foot{text-align:center;color:var(--mute);font-size:.76rem;padding:6px 0 20px}
@keyframes rise{from{opacity:0;transform:translateY(16px)}}
@media(max-width:780px){.kpis{grid-template-columns:repeat(2,1fr)}.two{grid-template-columns:1fr}.console{grid-template-columns:1fr}
 .gw.big{max-width:260px}table{font-size:.8rem}th,td{padding:.32rem .42rem}.brand{font-size:1.2rem}}
"""

# ---------------- JS (placeholders מוזרקים מהמודל) ----------------
JS = """
<script>
/* live clock */
(function(){var c=document.getElementById('clock');function t(){if(!c)return;
 c.textContent=new Date().toLocaleTimeString('he-IL',{hour:'2-digit',minute:'2-digit'});}t();setInterval(t,15000);})();
/* hyperscreen tabs */
(function(){var tabs=[].slice.call(document.querySelectorAll('.tab'));
 tabs.forEach(function(t){t.addEventListener('click',function(){
  tabs.forEach(function(x){x.classList.remove('on');});
  [].forEach.call(document.querySelectorAll('.view'),function(v){v.classList.remove('on');});
  t.classList.add('on');var el=document.getElementById(t.getAttribute('data-view'));if(el)el.classList.add('on');});});})();
/* launch checklist */
(function(){var boxes=[].slice.call(document.querySelectorAll('.chk input'));
 var bar=document.getElementById('clbar'),pct=document.getElementById('clpct');if(!bar)return;
 function upd(){var d=boxes.filter(function(b){return b.checked;}).length;var p=Math.round(d/boxes.length*100);
  bar.style.width=p+'%';pct.textContent=p+'% ('+d+'/'+boxes.length+')';
  try{localStorage.setItem('ulease_cl',JSON.stringify(boxes.map(function(b){return b.checked;})));}catch(e){}}
 try{var sv=JSON.parse(localStorage.getItem('ulease_cl')||'[]');boxes.forEach(function(b,i){if(sv[i])b.checked=true;});}catch(e){}
 boxes.forEach(function(b){b.addEventListener('change',upd);});upd();})();
/* DRIVE-MODE: deal rate x FX */
(function(){
 var B={deal:__DEAL__,lead:__LEAD__,sub:__SUB__,ad:__AD__,fin:__FIN__,opex:__OPEX__};
 var dm=document.getElementById('dm'),fx=document.getElementById('fx');if(!dm||!fx)return;
 function mm(n){return Math.abs(n)>=1e6?'₪'+(n/1e6).toFixed(2)+'M':'₪'+Math.round(n/1e3)+'K';}
 function calc(){var d=dm.value/100,ff=fx.value/100,dv=150000*(ff/3.6),cm=dv*0.020;
  var rev=B.deal*d*(ff/3.6)+B.lead*d+B.fin*d+B.sub+B.ad,net=rev-B.opex,mg=rev?net/rev*100:0;
  document.getElementById('dmv').textContent=Math.round(dm.value)+'%';
  document.getElementById('fxv').textContent=ff.toFixed(2);
  document.getElementById('o_dv').textContent=mm(dv);
  document.getElementById('o_cm').textContent='₪'+Math.round(cm).toLocaleString();
  document.getElementById('o_rev').textContent=mm(rev);
  document.getElementById('o_net').textContent=mm(net);
  document.getElementById('o_mg').textContent=Math.round(mg)+'%';
  var kd=document.getElementById('k_dm');if(kd){kd.style.setProperty('--p',Math.min(100,dm.value/1.5));}
  var kf=document.getElementById('k_fx');if(kf){kf.style.setProperty('--p',(fx.value-250)/1.5);}
 }
 dm.addEventListener('input',calc);fx.addEventListener('input',calc);calc();})();
/* Unit economics (live) */
(function(){var CPL=__CPL__,CONTRIB=5985,PRO=4500,PMX=7700;
 var ch=document.getElementById('ch'),cv=document.getElementById('cv'),cp=document.getElementById('cp'),cl=document.getElementById('cl');
 if(!ch||!cv||!cp||!cl)return;
 function mm(n){return Math.abs(n)>=1e6?'₪'+(n/1e6).toFixed(2)+'M':'₪'+Math.round(n/1e3)+'K';}
 function calc2(){var churn=ch.value/1000,conv=cv.value/100,cpm=+cp.value,close=cl.value/100;
  var ltvP=PRO/churn,ltvX=PMX/churn,cacD=CPL/conv,cacS=cpm/close;
  document.getElementById('chv').textContent=(ch.value/10).toFixed(1)+'%';
  document.getElementById('cvv').textContent=cv.value+'%';
  document.getElementById('cpv').textContent='₪'+cp.value;
  document.getElementById('clv').textContent=cl.value+'%';
  document.getElementById('u_lp').textContent=mm(ltvP);
  document.getElementById('u_lx').textContent=mm(ltvX);
  document.getElementById('u_cd').textContent='₪'+Math.round(cacD).toLocaleString();
  document.getElementById('u_cs').textContent='₪'+Math.round(cacS).toLocaleString();
  document.getElementById('u_rd').textContent=Math.round(CONTRIB/cacD)+'x';
  document.getElementById('u_rs').textContent=Math.round(ltvP/cacS)+'x';}
 [ch,cv,cp,cl].forEach(function(s){s.addEventListener('input',calc2);});calc2();})();
</script>
"""
JS = (JS.replace("__DEAL__", f"{B['deal']:.0f}").replace("__LEAD__", f"{B['lead']:.0f}")
        .replace("__SUB__", f"{B['sub']:.0f}").replace("__AD__", f"{B['ad']:.0f}")
        .replace("__FIN__", f"{B['fin']:.0f}").replace("__OPEX__", f"{B['opex']:.0f}")
        .replace("__CPL__", f"{cpl:.2f}"))

# ---------------- HEAD ----------------
HEAD = ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>ULease 🎯 — Executive Cockpit</title>'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;700&family=Heebo:wght@300;400;700&display=swap" rel="stylesheet">'
        f'<style>{CSS}</style></head><body><div class="ambient"></div>{DEFS}<div class="wrap">')

# ---------------- BODY ----------------
P=[]
# HUD
P.append('<div class="hud">'
 '<div class="ico"><span class="chip"><span class="dot"></span>DRIVE</span>'
 '<span>⚡ ECO</span><span>📶 LTE</span></div>'
 '<div class="brand">ULease&nbsp;🎯<small>L E A S I N G . C O . I L</small></div>'
 '<div class="ico"><span id="clock">10:10</span><span class="chip">16 · 06 · 26</span></div></div>')

# Cockpit cluster
P.append('<div class="cockpit"><div class="cluster">')
margin_pct = f"{K['margin27']*100:.0f}%"
P.append(f'<div class="gw"><div class="tag">REVENUE</div>{gauge(K["rev27"]/15e6, m(K["rev27"]), "הכנסה 2027", CYAN)}</div>')
P.append(f'<div class="gw big"><div class="tag">RUN-RATE · ARR</div>{gauge(K["runrate"]/20e6, m(K["runrate"]), "Run-rate שנתי", AMBER, sub="דצמבר 27")}</div>')
P.append(f'<div class="gw"><div class="tag">MARGIN</div>{gauge(K["margin27"], margin_pct, "מרווח נטו", GREEN)}</div>')
P.append('</div>')
P.append(f'<div class="battery"><div class="lab">Cash מצטבר<b class="num">{m(K["cash_end"])}</b></div>'
         f'<div class="bat">{battery(min(1,K["cash_end"]/14e6))}</div>'
         f'<div class="bolt">⚡</div><div class="lab">CHARGED<b class="num" style="color:#41e0a3">{min(100,K["cash_end"]/14e6*100):.0f}%</b></div></div>')
P.append('<div style="text-align:center;margin-top:6px"><small>כולל גיוס ₪150K · רווחי מהחודש הראשון · יוני 2026 → דצמבר 2027</small></div></div>')

# KPI tiles
P.append(f'<div class="kpis">{kpi_html}</div>')

# Central hyperscreen (tabs)
P.append('<div class="screen"><h2>🖥️ Central Display — מסך מרכזי</h2>'
 '<div class="hsbar">'
 '<div class="tab on" data-view="v_rev">📈 הכנסה</div>'
 '<div class="tab" data-view="v_deal">🚗 עסקאות</div>'
 '<div class="tab" data-view="v_cash">💰 מזומן</div>'
 '<div class="tab" data-view="v_mix">🧩 תמהיל</div></div>')
P.append(f'<div id="v_rev" class="view on">{svg_bars([r["total_rev"] for r in rows], labels, "barCyan")}'
         '<small>מסלול הכנסה חודשית (₪) · קו ענבר = מעבר 2026→2027 · יעד: Run-rate ₪17.45M · רחף לפרטים</small></div>')
P.append(f'<div id="v_deal" class="view">{svg_bars([r["deals"] for r in rows], labels, "barBlue")}'
         f'<small>עסקאות לחודש · שיא {maxdeals} עסקאות · 2027: {f(K["deals27"])} עסקאות</small></div>')
P.append(f'<div id="v_cash" class="view">{svg_line([r["cum_cash"] for r in rows], GREEN, "areaGreen")}'
         '<small>מזומן מצטבר (₪, כולל גיוס 150K) — עקומת הטעינה</small></div>')
P.append(f'<div id="v_mix" class="view">{svg_stacked(mix27)}<div style="margin-top:12px">{legend(mix27)}</div>'
         '<small style="display:block;margin-top:6px">תמהיל הכנסות 2027 — חמישה מנועי הכנסה</small></div>')
P.append('</div>')

# DRIVE-MODE console (What-If deal x FX)
P.append('<div class="screen"><h2>🎛️ DRIVE MODE — מחוון קצב עסקאות × מט"ח</h2><div class="console">'
 '<div class="dials">'
 '<div class="dial"><div id="k_dm" class="ring" style="--p:67"><span class="ico">🚗</span></div><div class="nm">קצב עסקאות</div></div>'
 '<div class="dial"><div id="k_fx" class="ring" style="--p:73"><span class="ico">$</span></div><div class="nm">USD / ILS</div></div></div>'
 '<div class="ctrl">'
 '<div><label>קצב עסקאות: <b id="dmv">100%</b></label><input id="dm" type="range" min="50" max="150" value="100"></div>'
 '<div><label>USD/ILS: <b id="fxv">3.60</b></label><input id="fx" type="range" min="250" max="400" value="360"></div></div></div>'
 '<div class="out" style="margin-top:16px">'
 '<div><small>שווי עסקה</small><b id="o_dv">₪150K</b></div>'
 '<div><small>עמלה/עסקה</small><b id="o_cm">₪3,001</b></div>'
 f'<div><small>הכנסה 2027</small><b id="o_rev">{m(K["rev27"])}</b></div>'
 f'<div><small>נטו 2027</small><b id="o_net">{m(K["net27"])}</b></div>'
 f'<div><small>מרווח</small><b id="o_mg">{K["margin27"]*100:.0f}%</b></div>'
 f'<div><small>לידים 2027</small><b>{leads27:,}</b></div></div>'
 '<div class="flag">מט"ח משפיע על <b>שווי העסקה</b> (רכב מיובא; <b>3.60 = עוגן היסטורי</b> שבו ₪150K; שער 29/05: 2.8152). שקל חזק → גם <b>יותר נפח</b> — הזז גם את "קצב עסקאות".</div></div>')

# Funnel
P.append(f'<div class="screen"><h2>📊 Funnel — לידים → עסקאות → מסירות (2027)</h2>{funnel_html()}'
 '<small style="display:block;margin-top:10px">המרה: לידים→עסקאות ~20% · עסקאות→מסירות ~95%</small></div>')

# Arbitrage
P.append('<div class="screen"><h2>💱 Proof of Arbitrage</h2><div class="funnel">'
 f'<div class="seg" style="width:100%;background:{GOLD}">מחירון ₪165K</div>'
 f'<div class="seg" style="width:82%;background:{BLUE}">עלות יבואן (אחרי FX) ₪135K</div>'
 f'<div class="seg" style="width:91%;background:{AMBER}">עסקה ב-ULease ₪150K</div></div>'
 '<ul style="margin-top:12px">'
 '<li><b>מט"ח:</b> USD/ILS 3.60→2.81 (~22% התחזקות שקל) → מרווח יבואן מתרחב</li>'
 '<li><b>0 ק"מ / גיולים:</b> מלאי תקוע מאמצע 2025 → לחץ למכירה בהנחה</li>'
 '<li><b>הפער</b> בין מחירון לעלות-יבואן הוא הארביטראז\' ש-ULease לוכדת דיגיטלית</li></ul>'
 '<div class="flag">נתונים להמחשה — לאמת מול עסקאות אמת.</div></div>')

# Unit economics (live)
P.append('<div class="screen"><h2>📐 Unit Economics — חי (מחובר ל-Outbound Engine)</h2><div class="ctrl">'
 '<div><label>Churn מנויים חודשי: <b id="chv">2.0%</b></label><input id="ch" type="range" min="10" max="100" value="20"></div>'
 '<div><label>המרת ליד→עסקה: <b id="cvv">20%</b></label><input id="cv" type="range" min="10" max="35" value="20"></div>'
 '<div><label>Outbound — עלות לפגישה (CPM): <b id="cpv">₪214</b></label><input id="cp" type="range" min="100" max="600" value="214"></div>'
 '<div><label>סגירת ספק מפגישה: <b id="clv">40%</b></label><input id="cl" type="range" min="20" max="60" value="40"></div></div>'
 '<div class="out" style="margin-top:14px">'
 '<div><small>Take Rate עסקה</small><b>3.33%</b></div>'
 f'<div><small>Take משוקלל</small><b>{take_blended*100:.1f}%</b></div>'
 f'<div><small>תרומה/עסקה</small><b>₪{contrib:,.0f}</b></div>'
 '<div><small>LTV מנוי Pro</small><b id="u_lp">₪225K</b></div>'
 '<div><small>LTV Pro Max</small><b id="u_lx">₪385K</b></div>'
 '<div><small>CAC / עסקה</small><b id="u_cd">₪396</b></div>'
 '<div><small>CAC / ספק</small><b id="u_cs">₪535</b></div>'
 '<div><small>יחס עסקה</small><b id="u_rd">15x</b></div>'
 '<div><small>יחס מנוי</small><b id="u_rs">420x</b></div></div>'
 f'<div class="flag">עלות-ליד ₪{cpl:.0f} (שיווק 2027 ÷ לידים) · LTV = ARPU ÷ churn · CAC ספק = CPM ÷ סגירה. הזז את המחוונים וראה את הכלכלה חיה.</div></div>')

# TAM/SAM/SOM + Marketplace health
P.append('<div class="two">'
 '<div class="screen"><h2>🌍 TAM / SAM / SOM</h2><div class="funnel">'
 f'<div class="seg" style="width:100%;background:{BLUE}">TAM · רכב חדש ~₪38B/שנה</div>'
 f'<div class="seg" style="width:58%;background:{AMBER}">SAM · פלח דיגיטלי ~₪11B</div>'
 f'<div class="seg" style="width:26%;background:{GREEN}">SOM · בר-השגה 18ח\' ~₪300M</div></div>'
 '<div class="flag">~250K רכב/שנה × ₪150K = TAM · SAM ~30% · SOM ≈ תחזית GMV. לאמת.</div></div>'
 '<div class="screen"><h2>❤️ Marketplace Health</h2><div class="out">'
 '<div><small>המרת ליד→עסקה</small><b>20%</b></div>'
 f'<div><small>Take משוקלל</small><b>{take_blended*100:.1f}%</b></div>'
 '<div><small>ספקים פעילים</small><b>7+</b></div>'
 f'<div><small>עסקאות/חודש (שיא)</small><b>{maxdeals}</b></div>'
 '<div><small>זמן-לעסקה</small><b>דקות</b></div>'
 '<div><small>נזילות</small><b style="color:#41e0a3">🟢</b></div></div></div></div>')

# AI agent layer
P.append('<div class="screen"><h2>🤖 AI Agent Layer — Ultra · Master · Max</h2><ul>'
 '<li><b>🛰️ Ultra</b> — Orchestrator: ניתוב event + ניהול state עסקה</li>'
 '<li><b>🧠 Master</b> — <span class="pill">Match</span><span class="pill">Pricing</span><span class="pill">Negotiation</span><span class="pill">Financing</span><span class="pill">Compliance</span></li>'
 '<li><b>⚙️ Max</b> — <span class="pill">Offer</span><span class="pill">Contract/e-Sign</span><span class="pill">Financing</span><span class="pill">Billing</span></li>'
 '<li><b>🛡️ Guardian</b> — אבטחה · IP · אתיקה</li></ul>'
 '<div class="flag">סטטוס: MVP ב-assist (אדם מאשר) → V1 אוטומציה מלאה. פירוט: ULEASE_SPEC.md §7.</div></div>')

# Expenses
P.append(f'<div class="screen"><h2>💸 הוצאות חודשיות (₪) + תמהיל 2027</h2>{svg_bars([r["opex"] for r in rows], labels, "barAmber")}'
         f'<div style="margin-top:12px">{svg_stacked(exp27)}</div><div style="margin-top:8px">{legend(exp27)}</div></div>')

# Net + margin
P.append('<div class="two">'
 f'<div class="screen"><h2>💵 רווח נטו חודשי (₪)</h2>{svg_bars([r["net_monthly"] for r in rows], labels, "barGreen")}</div>'
 f'<div class="screen"><h2>📉 מרווח נטו (%)</h2>{svg_line([(r["net_monthly"]/r["total_rev"]*100 if r["total_rev"] else 0) for r in rows], AMBER, "areaAmber", suffix="%")}'
 f'<small>ממוצע 2027: {K["margin27"]*100:.0f}%</small></div></div>')

# Scenarios
P.append('<div class="screen"><h2>🎯 תרחישי קצב עסקאות (±30%)</h2>'
 '<div class="tscroll"><table><thead><tr><th>תרחיש</th><th>הכנסה 2027</th><th>נטו 2027</th><th>Cash סוף 27</th><th>Run-rate</th></tr></thead><tbody>'
 + "".join(f'<tr><td>{nm} (×{mu:g})</td><td>{m(scen[nm]["r27"])}</td><td>{m(scen[nm]["n27"])}</td><td>{m(scen[nm]["cash"])}</td><td>{m(scen[nm]["rr"])}</td></tr>' for nm,mu,_ in SCEN)
 + '</tbody></table></div>'
 f'<div style="margin-top:14px"><small>נטו 2027 לפי תרחיש (₪)</small></div>{svg_scen()}'
 '<div class="flag">גם בתרחיש <b>השמרני</b> (−30%) הפלטפורמה רווחית מאוד — נטו 2027 ₪8.6M. זה ה-operating leverage.</div></div>')

# Launch checklist
P.append('<div class="screen"><h2>✅ צ\'קליסט השקה — מעקב חי</h2>'
 '<div class="prog"><div id="clbar"></div></div><div id="clpct">0%</div>'
 + f'<div class="two" style="margin-top:10px"><div>{cl_html.split(chr(60)+"div class="+chr(34)+"clhead"+chr(34)+">תוכן")[0]}</div>'
 + f'<div><div class="clhead">תוכן{cl_html.split(chr(60)+"div class="+chr(34)+"clhead"+chr(34)+">תוכן")[1]}</div></div>'
 '<div class="flag">🔴 שערים קריטיים: ייעוץ משפטי לחיתום · חוק ספאם · גיוס Tech Lead · עסקה מקצה-לקצה</div></div>')

# Marketplace + team
P.append('<div class="two">'
 '<div class="screen"><h2>🔺 Marketplace + מנועי הכנסה</h2><ul>'
 '<li><b>היצע:</b> יבואנים · ליסינג · מימון</li><li><b>ביקוש:</b> פרטי · B2B2C</li><li><b>מפיצים:</b> דילרים/ליסינג (מנויים)</li></ul>'
 '<span class="pill">B2B 1.1–2.2%</span><span class="pill">B2B2C 1.1–3.33%</span><span class="pill">B2C 3.33–7.77%</span><span class="pill">ליד ₪150</span><span class="pill">Ultra ₪4,500</span><span class="pill">Max ₪7,700</span><span class="pill">מימון 1%</span></div>'
 '<div class="screen"><h2>👥 צוות · גיוס · מתודולוגיה</h2><ul>'
 '<li>שירי — Super COO · אברהם — מו"פ ושיווק</li><li>גיוס: מנהל מערכות טכנולוגיה ⬅️ הפער</li>'
 '<li>Cap 37/37/13/13 · גיוס ₪150K</li><li>תורת המשחקים · Big Five · מו"מ · Multi-agent</li></ul></div></div>')

# Full forecast table
P.append(f'<div class="screen"><h2>🗓️ תחזית חודשית מלאה</h2><div class="tscroll"><table>'
 '<thead><tr><th>חודש</th><th>עסקאות</th><th>הכנסה</th><th>הוצאות</th><th>נטו</th><th>Cash</th></tr></thead>'
 f'<tbody>{table_rows}</tbody></table></div></div>')

# Timeline
P.append(f'<div class="screen"><h2>📅 טיימליין השקה</h2><div class="tl">{tl_html}</div></div>')

# Footer
P.append('<div class="foot">מקור: CASES/ULEASE_FORECAST.csv (Base Case v1.4) · כיול ב-ULEASE_FORECAST.py · '
 'ליבה (Deal Score/Match/תמחור) = IP · Claude OS — Avraham Bar Yochai Chazan</div>')

HTML = HEAD + "".join(P) + JS + "</div></body></html>"

open(os.path.join(HERE, "ULEASE_DASHBOARD.html"), "w", encoding="utf-8").write(HTML)
print(f"🏎️  Cockpit dashboard עודכן → ULEASE_DASHBOARD.html · Run-rate {m(K['runrate'])} · מרווח {K['margin27']*100:.0f}% · צ'קליסט {sum(len(i) for _,i in CHECKLIST)} פריטים")
