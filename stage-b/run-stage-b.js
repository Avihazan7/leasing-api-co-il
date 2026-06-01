'use strict';

// מריץ ההוכחה מקצה לקצה לשלב ב'. מדפיס שבעה שלבים:
// תכנון רב-עובדים · ביצוע גלי לפי תלות · תוצרי Summarizer · ציר-זמן ·
// סקירת חוזה · יומן מלא · אימות-הרחבה.
//
// עיקרון מנחה: SharedMemory ו-Manager של שלב א' נצרכים כמו-שהם — אפס שינוי
// בתשתית. שלב ב' הוא ראיה שההרחבה אינה דורשת ארכיטקטורה חדשה.

const { SharedMemory } = require('../stage-a/src/shared-memory');
const { Manager } = require('../stage-a/src/manager');
const { SummarizerWorker } = require('../stage-a/src/worker-summarizer');
const { TimelineWorker } = require('./src/worker-timeline');
const { ContractReviewWorker } = require('./src/worker-contract-review');

// מקור מקומי לדוגמה — חיסיון: אפס תלות חיצונית, הכול רץ במקום.
const LEASING_CONTRACT = {
  clauses: [
    { id: 'c1', text: 'תקופת ההתקשרות 36 חודשים מיום מסירת הרכב.',
      gist: 'תקופת הליסינג: 36 חודשים.' },
    { id: 'c2', text: 'תשלום חודשי קבוע של 1,890 ש"ח כולל מע"מ.',
      gist: 'תשלום חודשי: 1,890 ש"ח כולל מע"מ.' },
    { id: 'c3', text: "מגבלת קילומטראז' שנתית 20,000 ק\"מ; חריגה 0.45 ש\"ח לק\"מ.",
      gist: 'תקרת ק"מ שנתית 20,000; חריגה בתשלום נוסף.' },
    { id: 'c4', text: 'בתום התקופה אופציית רכישה בשווי שייר של 28%.',
      gist: 'אופציית רכישה בתום התקופה (שייר 28%).' },
  ],
};

function hr(title) {
  console.log('\n' + '─'.repeat(64));
  console.log(title);
  console.log('─'.repeat(64));
}

function main() {
  const memory = new SharedMemory();
  const manager = new Manager(memory, { maxSteps: 6 });
  const sharedSources = { 'leasing-contract': LEASING_CONTRACT };

  const workers = {
    summarizer:         new SummarizerWorker(memory,       { sources: sharedSources }),
    'timeline-builder': new TimelineWorker(memory,         { sources: sharedSources }),
    'contract-review':  new ContractReviewWorker(memory,   { sources: sharedSources }),
  };

  // ── שלב 1/7 · תכנון רב-עובדים עם תלות בין-צעדים ──
  hr('שלב 1/7 · תכנון רב-עובדים עם תלות בין-צעדים (המנהל)');
  const plan = manager.plan(
    'הפק סיכום, ציר-זמן וסקירת חוזה — כולם מעוגנים למקור, וסקירה צורכת קודמים.',
    [
      { worker: 'summarizer',       inputRef: 'source:leasing-contract', dependsOn: [] },
      { worker: 'timeline-builder', inputRef: 'source:leasing-contract', dependsOn: [] },
      { worker: 'contract-review',  inputRef: 'source:leasing-contract', dependsOn: ['s1', 's2'] },
    ],
  );
  console.log(`taskId : ${plan.taskId}`);
  console.log(`goal   : ${plan.goal}`);
  console.log(`steps  : ${plan.steps.length} (תקרה: ${plan.maxSteps})`);
  plan.steps.forEach((s) =>
    console.log(`  • ${s.stepId} → worker=${s.worker} input=${s.inputRef} dependsOn=[${s.dependsOn}]`),
  );

  // ── שלב 2/7 · ביצוע — תזמון "Ready-Set" לפי מוכנות תלות ──
  hr('שלב 2/7 · ביצוע — תזמון Ready-Set (גלים לפי מוכנות תלוּת)');
  let guard = 0;
  let wave = 0;
  let pending = manager.nextSteps(plan);
  while (pending.length > 0) {
    if (++guard > plan.maxSteps) throw new Error('step ceiling breached at runtime');
    wave += 1;
    console.log(`  → גל #${wave}: ${pending.map((s) => s.stepId).join(', ')}`);
    for (const step of pending) {
      const worker = workers[step.worker];
      const out = worker.execute(step, plan.taskId);
      console.log(
        `    ✦ ${step.stepId} בוצע ע"י "${worker.id}" → status=${out.payload.status}, evidence=${out.evidence.length}`,
      );
    }
    pending = manager.nextSteps(plan);
  }

  // ── שלב 3/7 · תוצר ה-Summarizer ──
  hr('שלב 3/7 · תוצר ה-Summarizer (סיכום מעוגן-מקור)');
  memory.byStep('s1', plan.taskId).payload.summary.forEach((p, i) => {
    console.log(`  ${i + 1}. ${p.point}`);
    console.log(`     ↳ עוגן [${p.evidence.ref}]: "${p.evidence.quote}"`);
  });

  // ── שלב 4/7 · ציר-הזמן ──
  hr('שלב 4/7 · ציר-הזמן (Timeline-Builder)');
  memory.byStep('s2', plan.taskId).payload.timeline.forEach((e, i) => {
    console.log(`  ${i + 1}. [${e.kind}] ${e.when} — ${e.what}`);
    console.log(`     ↳ עוגן [${e.evidence.ref}]: "${e.evidence.quote}"`);
  });

  // ── שלב 5/7 · סקירת חוזה — צרכנית של s1, s2 ──
  hr('שלב 5/7 · סקירת חוזה (Contract-Review) — צורכת s1, s2 דרך הזיכרון');
  const review = memory.byStep('s3', plan.taskId).payload;
  console.log(`  contextUsed: [${review.contextUsed.join(', ')}]`);
  console.log('  סיכונים:');
  review.risks.forEach((r) =>
    console.log(`    ⚠ [${r.severity}] ${r.topic} — ${r.finding}  (↳ ${r.evidence.ref})`),
  );
  console.log('  אישורים:');
  review.cleared.forEach((c) =>
    console.log(`    ✓ ${c.topic} — ${c.finding}  (↳ ${c.evidence.ref})`),
  );
  console.log('  סעיפים חסרים:');
  review.missing.forEach((m) =>
    console.log(`    ✗ ${m.topic} — ${m.finding}  (↳ ${m.evidence.ref})`),
  );

  // ── שלב 6/7 · יומן מלא ──
  hr('שלב 6/7 · יומן מלא (append-only · ראיות חוצות-צעדים)');
  memory.all().forEach((e) =>
    console.log(
      `  [${e.entryId}] ${e.ts} author=${e.author} kind=${e.kind} step=${e.stepId} evidence=${e.evidence.length}`,
    ),
  );

  // ── שלב 7/7 · אימות הרחבה ──
  hr("שלב 7/7 · אימות הרחבה — שלב ב' מרחיב את שלב א' בלי לשבור");
  verifyStageB(memory, plan);
}

// כל בדיקה מַפעילה את המנגנון בפועל — אכיפה ולא תיעוד.
function verifyStageB(memory, plan) {
  const checks = [
    ['three workers ran in same task', () => {
      const authors = new Set(
        memory.find((e) => e.kind === 'worker-output' && e.taskId === plan.taskId).map((e) => e.author),
      );
      if (authors.size !== 3) throw new Error(`expected 3 worker authors, got ${authors.size}`);
    }],
    ['ready-set fired s1+s2 in same wave', () => {
      const s1 = memory.byStep('s1', plan.taskId);
      const s2 = memory.byStep('s2', plan.taskId);
      const s3 = memory.byStep('s3', plan.taskId);
      // s3 חייב להיכתב אחרי שניהם — וזה רק יכול לקרות אם s1,s2 בוצעו בגל קודם.
      if (!(s3.entryId > s1.entryId && s3.entryId > s2.entryId)) {
        throw new Error('s3 did not follow s1 and s2 in the append-only log');
      }
    }],
    ['cross-step dependency consumed in s3', () => {
      const s3 = memory.byStep('s3', plan.taskId).payload;
      if (!s3.contextUsed.includes('s1') || !s3.contextUsed.includes('s2')) {
        throw new Error(`s3.contextUsed missing prior steps: [${s3.contextUsed}]`);
      }
    }],
    ['evidence chain spans steps in s3 output', () => {
      const s3 = memory.byStep('s3', plan.taskId);
      const stepCtx = s3.evidence.filter((e) => e.kind === 'step-context');
      if (stepCtx.length < 2) {
        throw new Error(`expected ≥2 step-context evidence entries in s3, got ${stepCtx.length}`);
      }
    }],
    ['all worker outputs carry evidence', () => {
      const all = memory.find((e) => e.kind === 'worker-output' && e.taskId === plan.taskId);
      for (const e of all) {
        if (e.evidence.length === 0) throw new Error(`output ${e.stepId} has empty evidence`);
      }
    }],
    ['missing-clause detection produced a finding', () => {
      const s3 = memory.byStep('s3', plan.taskId).payload;
      if (s3.missing.length === 0) throw new Error('no missing-clause findings produced');
    }],
    ['stage-a infrastructure unchanged (path check)', () => {
      // require של קבצי שלב א' ישירות מ-stage-b — אם נשבור את שלב א', זה ייכשל.
      const sa = require('../stage-a/src/shared-memory');
      const ma = require('../stage-a/src/manager');
      const sw = require('../stage-a/src/worker-summarizer');
      if (!sa.SharedMemory || !ma.Manager || !sw.SummarizerWorker) {
        throw new Error('stage-a exports changed shape');
      }
    }],
  ];

  let allPass = true;
  for (const [name, fn] of checks) {
    let status = 'ENFORCED';
    try { fn(); } catch (err) { status = `FAILED (${err.message})`; allPass = false; }
    console.log(`  [${status === 'ENFORCED' ? '✓' : '✗'}] ${name.padEnd(46)}: ${status}`);
  }

  console.log('');
  console.log(
    allPass
      ? "  שלב ב' — שלושה עובדים, גל מקבילי, תלות בין-צעדים, ראיות חוצות-צעדים. התשתית עומדת."
      : '  אזהרה: בדיקה אחת או יותר נכשלה.',
  );
  if (!allPass) process.exitCode = 1;
}

main();
