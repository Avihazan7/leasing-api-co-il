'use strict';

// מריץ ההוכחה מקצה לקצה לשלב א'. מדפיס חמישה שלבים:
// תכנון · ביצוע · הרכבת פלט סופי · היומן המלא · אימות מנגנוני הממשל.

const { SharedMemory } = require('./src/shared-memory');
const { Manager } = require('./src/manager');
const { SummarizerWorker } = require('./src/worker-summarizer');

// מקור מקומי לדוגמה — חיסיון: אפס תלות חיצונית, הכול רץ במקום.
const LEASING_CONTRACT = {
  clauses: [
    { id: 'c1', text: 'תקופת ההתקשרות 36 חודשים מיום מסירת הרכב.', gist: 'תקופת הליסינג: 36 חודשים.' },
    { id: 'c2', text: 'תשלום חודשי קבוע של 1,890 ש"ח כולל מע"מ.', gist: 'תשלום חודשי: 1,890 ש"ח כולל מע"מ.' },
    { id: 'c3', text: "מגבלת קילומטראז' שנתית 20,000 ק\"מ; חריגה 0.45 ש\"ח לק\"מ.", gist: 'תקרת ק"מ שנתית 20,000; חריגה בתשלום נוסף.' },
    { id: 'c4', text: 'בתום התקופה אופציית רכישה בשווי שייר של 28%.', gist: 'אופציית רכישה בתום התקופה (שייר 28%).' },
  ],
};

function hr(title) {
  console.log('\n' + '─'.repeat(64));
  console.log(title);
  console.log('─'.repeat(64));
}

function main() {
  const memory = new SharedMemory();
  const manager = new Manager(memory, { maxSteps: 5 });
  const summarizer = new SummarizerWorker(memory, {
    sources: { 'leasing-contract': LEASING_CONTRACT },
  });
  const workers = { summarizer };

  // ── שלב 1/5 · תכנון וניתוב (המנהל) ──
  hr('שלב 1/5 · תכנון וניתוב (המנהל)');
  const plan = manager.plan('סכם את תנאי הסכם הליסינג בסיכום מעוגן-מקור.', [
    { worker: 'summarizer', inputRef: 'source:leasing-contract' },
  ]);
  console.log(`taskId : ${plan.taskId}`);
  console.log(`goal   : ${plan.goal}`);
  console.log(`steps  : ${plan.steps.length} (תקרה: ${plan.maxSteps})`);
  plan.steps.forEach((s) =>
    console.log(`  • ${s.stepId} → worker=${s.worker} input=${s.inputRef} dependsOn=[${s.dependsOn}]`),
  );

  // ── שלב 2/5 · ביצוע דרך הזיכרון (העובד) ──
  hr('שלב 2/5 · ביצוע דרך הזיכרון (העובד)');
  let guard = 0;
  let pending = manager.nextSteps(plan);
  while (pending.length > 0) {
    if (++guard > plan.maxSteps) throw new Error('step ceiling breached at runtime');
    for (const step of pending) {
      const worker = workers[step.worker];
      const out = worker.execute(step, plan.taskId);
      console.log(
        `  ✦ ${step.stepId} בוצע ע"י "${worker.id}" → status=${out.payload.status}, evidence=${out.evidence.length}`,
      );
    }
    pending = manager.nextSteps(plan);
  }

  // ── שלב 3/5 · הרכבת פלט סופי ──
  hr('שלב 3/5 · הרכבת פלט סופי (סיכום מעוגן-מקור)');
  const result = memory.byStep('s1', plan.taskId).payload;
  result.summary.forEach((p, i) => {
    console.log(`  ${i + 1}. ${p.point}`);
    console.log(`     ↳ עוגן [${p.evidence.ref}]: "${p.evidence.quote}"`);
  });

  // ── שלב 4/5 · היומן המלא (שקיפות) ──
  hr('שלב 4/5 · היומן המלא (append-only · שקיפות מלאה)');
  memory.all().forEach((e) =>
    console.log(
      `  [${e.entryId}] ${e.ts} author=${e.author} kind=${e.kind} step=${e.stepId} evidence=${e.evidence.length}`,
    ),
  );

  // ── שלב 5/5 · אימות מנגנוני הממשל ──
  hr('שלב 5/5 · אימות מנגנוני הממשל');
  verifyGovernance(memory);
}

// כל בדיקה מַפעילה את המנגנון בפועל — אכיפה בקוד, לא רק תיעוד.
function verifyGovernance(memory) {
  const checks = [
    ['evidence[] mandatory on worker output', () => {
      let threw = false;
      try {
        memory.append({ taskId: 't', author: 'summarizer', stepId: 'x', kind: 'worker-output', payload: {}, evidence: [] });
      } catch {
        threw = true;
      }
      if (!threw) throw new Error('worker output without evidence was accepted');
    }],
    ['step ceiling halts runaway loops', () => {
      const m = new Manager(new SharedMemory(), { maxSteps: 2 });
      let threw = false;
      try {
        m.plan('g', [{ worker: 'w' }, { worker: 'w' }, { worker: 'w' }]);
      } catch {
        threw = true;
      }
      if (!threw) throw new Error('plan exceeding ceiling was accepted');
    }],
    ['worker safe-stops on missing input', () => {
      const mem = new SharedMemory();
      const w = new SummarizerWorker(mem, { sources: {} });
      const out = w.execute({ stepId: 's1', dependsOn: [], inputRef: 'source:missing' }, 'tX');
      if (out.payload.status !== 'partial' || !out.payload.flags.includes('incomplete-source')) {
        throw new Error('worker did not safe-stop on missing input');
      }
    }],
    ['memory is append-only (full audit)', () => {
      const mem = new SharedMemory();
      const e = mem.append({ taskId: 't', author: 'manager', kind: 'note', payload: { v: 1 } });
      if (!Object.isFrozen(e)) throw new Error('entry is not frozen');
      if ('delete' in mem || 'update' in mem) throw new Error('memory exposes mutation');
    }],
    ['partial output flagged for human review', () => {
      const mem = new SharedMemory();
      const w = new SummarizerWorker(mem, { sources: {} });
      const out = w.execute({ stepId: 's1', dependsOn: [], inputRef: 'source:none' }, 'tH');
      if (!out.payload.flags.includes('incomplete-source')) {
        throw new Error('partial output not flagged for review');
      }
    }],
  ];

  let allPass = true;
  for (const [name, fn] of checks) {
    let status = 'ENFORCED';
    try {
      fn();
    } catch (err) {
      status = `FAILED (${err.message})`;
      allPass = false;
    }
    console.log(`  [${status === 'ENFORCED' ? '✓' : '✗'}] ${name.padEnd(42)}: ${status}`);
  }

  console.log('');
  console.log(
    allPass
      ? "  כל מנגנוני הממשל נאכפים בקוד. שלב א' — הוכחת היתכנות הושלמה."
      : '  אזהרה: מנגנון ממשל אחד או יותר אינו נאכף.',
  );
  if (!allPass) process.exitCode = 1;
}

main();
