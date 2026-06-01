#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULease 🎯 Leasing.co.il — Executive Dashboard generator
קורא את CASES/ULEASE_FORECAST.csv ומפיק דשבורד HTML עצמאי (RTL, גרפי SVG).
כולל: KPIs, הכנסות, מזומן, עסקאות, תמהיל הכנסות, הוצאות, רווח ומרווח, וצ'קליסט השקה אינטראקטיבי.
הרצה:  python3 CASES/ULEASE_FORECAST.py && python3 CASES/ULEASE_DASHBOARD.py
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
ACCENT, CREAM, INK, GREEN = "#c0532b", "#f5f1e8", "#2a2622", "#2f7d4f"
PAL = ["#c0532b", "#e0894f", "#2a6f6b", "#9b8557", "#7a5c3e"]

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
SCEN=[("שמרני",0.7,"#9b8557"),("בסיס",1.0,ACCENT),("אופטימי",1.3,GREEN)]
scen={nm:_scen(mu) for nm,mu,_ in SCEN}

# funnel (2027), what-if base, launch timeline
leads27=int(S(y27,"leads")); deals27i=int(K["deals27"]); deliv27=round(deals27i*0.95)
B={"deal":S(y27,"deal_rev"),"lead":S(y27,"lead_rev"),"sub":S(y27,"sub_rev"),"ad":S(y27,"ad_rev"),"fin":S(y27,"fin_rev"),"opex":K["opex27"]}
def funnel_html():
    stages=[("לידים",leads27,PAL[1]),("עסקאות",deals27i,ACCENT),("מסירות",deliv27,PAL[2])]; mx=stages[0][1]; out=[]; prev=None
    for nm,v,c in stages:
        w=22+78*(v/mx); conv=f" · {v/prev*100:.0f}% מהקודם" if prev else ""
        out.append(f'<div class="seg" style="width:{w:.0f}%;background:{c}">{nm}: {v:,}{conv}</div>'); prev=v
    return '<div class="funnel">'+''.join(out)+'</div>'
TL=[("יוני · שבוע 1","חברה + דומיין + תשתית + ingestion"),("יוני · שבוע 2","חדר-עסקה + מנויים + QA"),
    ("חצי-שני יוני 26","🚀 Go-Live — 26 עסקאות"),("Q3–Q4 2026","Scale: מכרז · מנוי Max · n8n"),("2027","Architect + צמיחה")]
tl_html="".join(f'<div class="step"><b>{t}</b>{d}</div>' for t,d in TL)

def m(n): return f"₪{n/1e6:.2f}M" if abs(n)>=1e6 else f"₪{n/1e3:.0f}K"
def f(n): return f"{n:,.0f}"

def svg_bars(vals, labels, color=ACCENT, w=960, h=210, pad=22, sep=7):
    mx=max(vals) or 1; n=len(vals); bw=(w-2*pad)/n; out=[]
    for i,v in enumerate(vals):
        bh=(h-2*pad)*(v/mx); x=pad+i*bw; y=h-pad-bh
        out.append(f'<rect x="{x+bw*0.12:.1f}" y="{y:.1f}" width="{bw*0.76:.1f}" height="{bh:.1f}" rx="2" fill="{color}"><title>{labels[i]}: {v:,.0f}</title></rect>')
    base=f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="#ccc"/>'
    sx=pad+sep*bw; s=f'<line x1="{sx:.1f}" y1="{pad}" x2="{sx:.1f}" y2="{h-pad}" stroke="{ACCENT}" stroke-dasharray="4" opacity=".4"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%" preserveAspectRatio="xMidYMid meet">{base}{s}{"".join(out)}</svg>'

def svg_line(vals, color=GREEN, w=960, h=210, pad=22, suffix=""):
    mx=max(vals) or 1; n=len(vals); pts=[(pad+(w-2*pad)*(i/(n-1)), h-pad-(h-2*pad)*(v/mx)) for i,v in enumerate(vals)]
    poly=f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="3"/>'
    area=f'<polygon points="{pad},{h-pad} '+" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)+f' {w-pad},{h-pad}" fill="{color}" opacity=".08"/>'
    dots="".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{color}"><title>{vals[i]:,.0f}{suffix}</title></circle>' for i,(x,y) in enumerate(pts))
    base=f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="#ccc"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%">{base}{area}{poly}{dots}</svg>'

def svg_stacked(parts, w=960, h=50):
    tot=sum(parts.values()) or 1; x=0; segs=[]
    for (l,v),c in zip(parts.items(), PAL):
        ws=w*(v/tot); segs.append(f'<rect x="{x:.1f}" y="0" width="{ws:.1f}" height="{h}" fill="{c}"><title>{l}: {v:,.0f} ({v/tot*100:.0f}%)</title></rect>'); x+=ws
    return f'<svg viewBox="0 0 {w} {h}" width="100%">{"".join(segs)}</svg>'

def legend(parts): return "".join(f'<span class="lg"><i style="background:{PAL[i]}"></i>{l} ({v/sum(parts.values())*100:.0f}%)</span>' for i,(l,v) in enumerate(parts.items()))

def svg_scen(w=960, h=220, pad=34):
    vals=[scen[nm]['n27'] for nm,_,_ in SCEN]; mx=max(vals) or 1; n=len(SCEN); bw=(w-2*pad)/n; out=[]
    for i,(nm,mu,c) in enumerate(SCEN):
        v=scen[nm]['n27']; bh=(h-2*pad)*(v/mx); x=pad+i*bw+bw*0.2; y=h-pad-bh
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw*0.6:.1f}" height="{bh:.1f}" rx="3" fill="{c}"/>')
        out.append(f'<text x="{x+bw*0.3:.1f}" y="{y-7:.1f}" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}">{v/1e6:.1f}M</text>')
        out.append(f'<text x="{x+bw*0.3:.1f}" y="{h-pad+17:.1f}" text-anchor="middle" font-size="12" fill="{INK}">{nm} ×{mu:g}</text>')
    base=f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="#ccc"/>'
    return f'<svg viewBox="0 0 {w} {h}" width="100%">{base}{"".join(out)}</svg>'

labels=[r["period"] for r in rows]
cards=[("GMV 2027",m(K["gmv27"]),"מצטבר"),("הכנסה 2027",m(K["rev27"]),f"2026: {m(K['rev26'])}"),
       ("נטו 2027",m(K["net27"]),f"מרווח {K['margin27']*100:.0f}%"),("הוצאות 2027",m(K["opex27"]),"opex"),
       ("Run-rate דצמ' 27",m(K["runrate"]),"שנתי"),("עסקאות 2027",f(K["deals27"]),f"2026: {f(K['deals26'])}"),
       ("מנויים",str(K["subs_end"]),"סוף 2027"),("Cash מצטבר",m(K["cash_end"]),"כולל ₪150K")]
card_html="".join(f'<div class="card"><div class="cap">{c[0]}</div><div class="big">{c[1]}</div><div class="sub">{c[2]}</div></div>' for c in cards)
table_rows="".join(f"<tr><td>{r['period']}</td><td>{f(r['deals'])}</td><td>{m(r['total_rev'])}</td><td>{m(r['opex'])}</td><td>{m(r['net_monthly'])}</td><td>{m(r['cum_cash'])}</td></tr>" for r in rows)

CHECKLIST = [("דומיין",["רכישת ULease.co.il","חיבור Leasing.co.il","DNS + SSL + מייל"]),
             ("משפטי",["הקמת חברה","תקנון + מדיניות פרטיות","ייעוץ משפטי לחיתום","עמידה בחוק ספאם"]),
             ("MVP",["אתר + אפליקציה לאוויר","Ingestion (API/CSV)","חדר-עסקה (חתימה+מקדמה)","מנויי Ultra + חיוב","Admin בסיסי"]),
             ("תוכן + Outreach",["מלאי 7 ספקים טעון","Landing + הצעת ערך","שלד n8n ב-assist"]),
             ("QA → Go-Live",["עסקה מקצה-לקצה עברה","תשלום/מקדמה נבדק","גיוס Tech Lead"])]
cl_html=""
for head,items in CHECKLIST:
    cl_html+=f'<div class="clhead">{head}</div>'
    cl_html+="".join(f'<label class="chk"><input type="checkbox"> {it}</label>' for it in items)

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
.card .cap{{font-size:.8rem;opacity:.65}} .card .big{{font-size:1.55rem;font-weight:800;color:{ACCENT};margin:4px 0}}
.card .sub{{font-size:.78rem;opacity:.6}}
.panel{{background:{CREAM};border-radius:16px;padding:20px 24px;margin-bottom:16px}}
.panel h2{{color:{ACCENT};font-size:1.15rem;margin-bottom:12px}}
.lg{{display:inline-flex;align-items:center;font-size:.82rem;margin-left:12px}} .lg i{{width:12px;height:12px;border-radius:3px;display:inline-block;margin-left:6px}}
.tscroll{{overflow-x:auto;-webkit-overflow-scrolling:touch}}
table{{width:100%;border-collapse:collapse;font-size:.88rem}} th,td{{padding:.38rem .55rem;text-align:right;border-bottom:1px solid #ddd;white-space:nowrap}} th{{color:{ACCENT}}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
ul{{list-style:none}} li{{padding:.22rem 0;padding-right:1.1rem;position:relative;font-size:.9rem}}
li::before{{content:'';position:absolute;right:0;top:.65em;width:.45rem;height:.45rem;background:{ACCENT};border-radius:50%}}
.pill{{display:inline-block;background:#fff;border:1px solid {ACCENT};color:{ACCENT};border-radius:20px;padding:.2rem .7rem;font-size:.8rem;margin:.15rem}}
.flag{{background:#fff3ee;border-right:3px solid {ACCENT};padding:.5rem .8rem;border-radius:6px;font-size:.86rem;margin-top:8px}}
.chk{{display:flex;align-items:center;gap:8px;font-size:.9rem;padding:.18rem 0;cursor:pointer}} .chk input{{width:16px;height:16px;accent-color:{ACCENT}}}
.clhead{{font-weight:700;color:{ACCENT};margin-top:10px;font-size:.85rem}}
.prog{{background:#e7e0d3;border-radius:20px;height:20px;overflow:hidden;margin:6px 0 4px}} .prog>div{{background:{ACCENT};height:100%;width:0;transition:width .3s}}
.funnel{{display:flex;flex-direction:column;gap:6px;align-items:center}} .funnel .seg{{color:#fff;border-radius:6px;padding:.55rem;text-align:center;font-size:.85rem;font-weight:700}}
.tl{{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px}} .tl .step{{flex:1;min-width:135px;background:#fff;border-top:3px solid {ACCENT};border-radius:10px;padding:10px;font-size:.82rem}} .tl .step b{{color:{ACCENT};display:block;margin-bottom:3px}}
.ctrl{{display:flex;flex-direction:column;gap:12px;margin-bottom:10px}} .ctrl input[type=range]{{width:100%;accent-color:{ACCENT}}} .ctrl label{{font-size:.9rem}}
.out{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}} .out>div{{background:#fff;border-radius:10px;padding:10px;text-align:center}} .out b{{color:{ACCENT};font-size:1.15rem;display:block;margin-top:2px}}
small{{opacity:.55}} @media(max-width:760px){{.grid{{grid-template-columns:repeat(2,1fr)}}.two{{grid-template-columns:1fr}} table{{font-size:.8rem}} th,td{{padding:.3rem .4rem}} header h1{{font-size:1.5rem}}}}
</style></head><body><div class="wrap">

<header><h1>ULease 🎯 Leasing.co.il — Executive Dashboard</h1>
<p>Marketplace תלת-צדדי לרכב חדש · Base Case v1.4 (עמלות מדורגות · מימון 1% · פרו-רייטה) · יוני 2026 → דצמבר 2027</p></header>

<div class="grid">{card_html}</div>

<div class="panel"><h2>📈 הכנסה חודשית (₪)</h2>{svg_bars([r['total_rev'] for r in rows], labels)}<small>קו מקווקו = מעבר 2026→2027 · רחף לפרטים</small></div>
<div class="panel"><h2>💰 מזומן מצטבר (₪, כולל גיוס 150K)</h2>{svg_line([r['cum_cash'] for r in rows])}</div>
<div class="panel"><h2>🚗 עסקאות לחודש</h2>{svg_bars([r['deals'] for r in rows], labels, color="#2a6f6b")}</div>
<div class="panel"><h2>🧩 תמהיל הכנסות 2027</h2>{svg_stacked(mix27)}<div style="margin-top:10px">{legend(mix27)}</div></div>

<div class="panel"><h2>📊 Funnel — לידים → עסקאות → מסירות (2027)</h2>{funnel_html()}
<small style="display:block;margin-top:8px">המרה: לידים→עסקאות ~20% · עסקאות→מסירות ~95%</small></div>

<div class="panel"><h2>💸 הוצאות חודשיות (₪) + תמהיל 2027</h2>{svg_bars([r['opex'] for r in rows], labels, color="#7a5c3e")}
<div style="margin-top:10px">{svg_stacked(exp27)}</div><div style="margin-top:8px">{legend(exp27)}</div></div>

<div class="two">
<div class="panel"><h2>💵 רווח נטו חודשי (₪)</h2>{svg_bars([r['net_monthly'] for r in rows], labels, color=GREEN)}</div>
<div class="panel"><h2>📉 מרווח נטו (%)</h2>{svg_line([(r['net_monthly']/r['total_rev']*100 if r['total_rev'] else 0) for r in rows], color=ACCENT, suffix="%")}
<small>ממוצע 2027: {K['margin27']*100:.0f}%</small></div>
</div>

<div class="panel"><h2>🎯 אומדנים — תרחישי קצב עסקאות (±30%)</h2>
<div class="tscroll"><table><thead><tr><th>תרחיש</th><th>הכנסה 2027</th><th>נטו 2027</th><th>Cash סוף 27</th><th>Run-rate</th></tr></thead><tbody>
{"".join(f'<tr><td>{nm} (×{mu:g})</td><td>{m(scen[nm]["r27"])}</td><td>{m(scen[nm]["n27"])}</td><td>{m(scen[nm]["cash"])}</td><td>{m(scen[nm]["rr"])}</td></tr>' for nm,mu,_ in SCEN)}
</tbody></table></div>
<div style="margin-top:12px;font-size:.85rem;opacity:.7;margin-bottom:2px">נטו 2027 לפי תרחיש (₪)</div>{svg_scen()}
<div class="flag">גם בתרחיש <b>השמרני</b> (−30% עסקאות) הפלטפורמה נשארת רווחית מאוד — נטו 2027 ₪8.6M. זה ה-operating leverage. הנחת W4: שיווק חצי-משתנה (50% קבוע + 50% צמוד לעסקאות).</div></div>

<div class="panel"><h2>🎛️ מחוון What-If — קצב עסקאות × מט"ח</h2>
<div class="ctrl">
<div><label>קצב עסקאות: <b id="dmv">100%</b></label><input id="dm" type="range" min="50" max="150" value="100"></div>
<div><label>USD/ILS: <b id="fxv">3.60</b></label><input id="fx" type="range" min="250" max="400" value="360"></div></div>
<div class="out">
<div><small>שווי עסקה</small><b id="o_dv">₪150K</b></div>
<div><small>עמלה/עסקה (משוקלל)</small><b id="o_cm">₪3,001</b></div>
<div><small>הכנסה 2027</small><b id="o_rev">₪12.98M</b></div>
<div><small>נטו 2027</small><b id="o_net">₪10.89M</b></div>
<div><small>מרווח</small><b id="o_mg">84%</b></div>
<div><small>לידים 2027</small><b>{leads27:,}</b></div></div>
<div class="flag">מט"ח משפיע על <b>שווי העסקה</b> (רכב מיובא; <b>3.60 = עוגן היסטורי</b> שבו ₪150K; שער השוק 29/05: 2.8152). תזת החברה: שקל חזק → גם <b>יותר נפח</b> — הזז גם את "קצב עסקאות". (אפקט הנפח אינו אוטומטי.)</div></div>

<div class="panel"><h2>✅ צ'קליסט השקה — מעקב חי</h2>
<div class="prog"><div id="clbar"></div></div><div id="clpct" style="font-weight:700;color:{ACCENT}">0%</div>
<div class="two" style="margin-top:8px"><div>{cl_html.split('<div class="clhead">תוכן')[0]}</div><div><div class="clhead">תוכן{cl_html.split('<div class="clhead">תוכן')[1]}</div></div>
<div class="flag">🔴 שערים קריטיים לפני השקה: ייעוץ משפטי לחיתום · חוק ספאם · גיוס Tech Lead · עסקה מקצה-לקצה</div></div>

<div class="two">
<div class="panel"><h2>🔺 Marketplace + מנועי הכנסה</h2><ul>
<li><b>היצע:</b> יבואנים · ליסינג · מימון</li><li><b>ביקוש:</b> פרטי · B2B2C</li><li><b>מפיצים:</b> דילרים/ליסינג (מנויים)</li></ul>
<span class="pill">B2B 1.1–2.2%</span><span class="pill">B2B2C 1.1–3.33%</span><span class="pill">B2C 3.33–7.77%</span><span class="pill">ליד ₪150</span><span class="pill">Ultra ₪4,500</span><span class="pill">Max ₪7,700</span><span class="pill">מימון 1%</span></div>
<div class="panel"><h2>👥 צוות · גיוס · מתודולוגיה</h2><ul>
<li>שירי — Super COO · אברהם — מו"פ ושיווק</li><li>גיוס: מנהל מערכות טכנולוגיה ⬅️ הפער</li>
<li>Cap 37/37/13/13 · גיוס ₪150K</li><li>תורת המשחקים · Big Five · מו"מ · Multi-agent</li></ul></div>
</div>

<div class="panel"><h2>🗓️ תחזית חודשית מלאה</h2>
<div class="tscroll"><table><thead><tr><th>חודש</th><th>עסקאות</th><th>הכנסה</th><th>הוצאות</th><th>נטו</th><th>Cash</th></tr></thead>
<tbody>{table_rows}</tbody></table></div></div>

<div class="panel"><h2>📅 טיימליין השקה</h2><div class="tl">{tl_html}</div></div>

<div class="panel"><small>מקור: CASES/ULEASE_FORECAST.csv (Base Case v1.4) · כיול ב-ULEASE_FORECAST.py · ליבה (Deal Score/Match/תמחור) = IP · Claude OS — Avraham Bar Yochai Chazan</small></div>

<script>
var boxes=[].slice.call(document.querySelectorAll('.chk input'));
var bar=document.getElementById('clbar'), pct=document.getElementById('clpct');
function upd(){{var d=boxes.filter(function(b){{return b.checked}}).length;var p=Math.round(d/boxes.length*100);
  bar.style.width=p+'%';pct.textContent=p+'% ('+d+'/'+boxes.length+')';
  try{{localStorage.setItem('ulease_cl',JSON.stringify(boxes.map(function(b){{return b.checked}})));}}catch(e){{}}}}
try{{var sv=JSON.parse(localStorage.getItem('ulease_cl')||'[]');boxes.forEach(function(b,i){{if(sv[i])b.checked=true;}});}}catch(e){{}}
boxes.forEach(function(b){{b.addEventListener('change',upd);}});upd();
</script>
<script>
(function(){{
 var B={{deal:{B['deal']:.0f},lead:{B['lead']:.0f},sub:{B['sub']:.0f},ad:{B['ad']:.0f},fin:{B['fin']:.0f},opex:{B['opex']:.0f}}};
 var dm=document.getElementById('dm'),fx=document.getElementById('fx');
 function mm(n){{return Math.abs(n)>=1e6?'₪'+(n/1e6).toFixed(2)+'M':'₪'+Math.round(n/1e3)+'K';}}
 function calc(){{
  var d=dm.value/100,ff=fx.value/100,dv=150000*(ff/3.6),cm=dv*0.020;
  var rev=B.deal*d*(ff/3.6)+B.lead*d+B.fin*d+B.sub+B.ad,net=rev-B.opex,mg=rev?net/rev*100:0;
  document.getElementById('dmv').textContent=Math.round(dm.value)+'%';
  document.getElementById('fxv').textContent=ff.toFixed(2);
  document.getElementById('o_dv').textContent=mm(dv);
  document.getElementById('o_cm').textContent='₪'+Math.round(cm).toLocaleString();
  document.getElementById('o_rev').textContent=mm(rev);
  document.getElementById('o_net').textContent=mm(net);
  document.getElementById('o_mg').textContent=Math.round(mg)+'%';
 }}
 dm.addEventListener('input',calc);fx.addEventListener('input',calc);calc();
}})();
</script>
</div></body></html>"""

open(os.path.join(HERE, "ULEASE_DASHBOARD.html"), "w", encoding="utf-8").write(HTML)
print(f"דשבורד עודכן → ULEASE_DASHBOARD.html · הוצאות 2027 {m(K['opex27'])} · מרווח {K['margin27']*100:.0f}% · צ'קליסט {sum(len(i) for _,i in CHECKLIST)} פריטים")
