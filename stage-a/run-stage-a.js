'use strict';

/**
 * run-stage-a.js — מריץ את הוכחת ההיתכנות של שלב א'
 *
 * מחבר את שלושת הרכיבים מקצה-לקצה ומוכיח שלושה דברים:
 *  1. מנהל מקבל מטרה, מתכנן, וכותב תוכנית לזיכרון המשותף.
 *  2. עובד קורא מהזיכרון, מבצע, וכותב תוצר מעוגן-מקור חזרה.
 *  3. כל זה תחת ממשל: תקרת צעדים, יומן append-only, ושדה evidence חובה.
 *
 * הרצה:  node run-stage-a.js
 */

const { SharedMemory } = require('./src/shared-memory');
const { Manager } = require('./src/manager');
const { SummarizerWorker } = require('./src/worker-summarizer');

// ── מסמך מקור לדוגמה (תיק משפטי קצר בעברית) ──
// מקור מקומי בלבד: אפס תלות חיצונית, הכול רץ במקום. כל סעיף הוא שורת-מקור
// מעוגנת (id) שאליה יפנה ה-evidence של העובד.
const LEGAL_CASE = {
  clauses: [
    {
      id: 'c1',
      text: 'ביום 12 במרץ 2026 הוגשה בקשת צו הרחקה לבית המשפט לענייני משפחה.',
      gist: 'הוגשה בקשת צו הרחקה (12.3.2026, ביהמ"ש לענייני משפחה).',
    },
    {
      id: 'c2',
      text: 'המבקש טען כי המשיב הפר את ההסכם שנחתם בין הצדדים ביום 1 בינואר 2026.',
      gist: 'נטענה הפרת הסכם שנחתם ביום 1.1.2026.',
    },
    {
      id: 'c3',
      text: 'ההסכם קבע כי המשיב ישלם סך של 50,000 ש"ח בתוך תשעים יום.',
      gist: 'ההסכם: תשלום 50,000 ש"ח בתוך 90 יום.',
    },
    {
      id: 'c4',
      text: 'המשיב לא שילם את הסכום במועד שנקבע בהסכם.',
      gist: 'המשיב לא שילם את הסכום במועד.',
    },
    {
      id: 'c5',
      text: 'בית המשפט קבע דיון ליום 20 באפריל 2026.',
      gist: 'נקבע דיון ליום 20.4.2026.',
    },
    {
      id: 'c6',
      text: 'הצדדים התבקשו להגיש תצהירים עד עשרה ימים לפני הדיון.',
      gist: 'הצדדים יגישו תצהירים עד 10 ימים לפני הדיון.',
    },
  ],
};

function divider(title) {
  console.log('\n' + '─'.repeat(64));
  console.log('  ' + title);
  console.log('─'.repeat(64));
}

function main() {
  divider("שלב א' · הוכחת היתכנות רב-סוכנית");

  // 1) אתחול הזיכרון המשותף — single-source-of-truth, append-only
  const memory = new SharedMemory();
  console.log('\n[init] shared memory created (append-only)');

  // 2) רישום העובד (יחיד בשלב א'). העובד מקבל את הזיכרון + מאגר מקורות מקומי.
  const summarizer = new SummarizerWorker(memory, {
    sources: { 'legal-case': LEGAL_CASE },
  });
  const workers = { summarizer };
  console.log(`[init] registered workers: ${Object.keys(workers).join(', ')}`);

  // 3) אתחול המנהל עם תקרת ממשל
  const manager = new Manager(memory, { maxSteps: 10 });
  console.log(`[init] manager ready · step ceiling = ${manager.maxSteps}`);

  // ── תכנון ──
  divider('1 · תכנון (Manager → Shared Memory)');
  const plan = manager.plan('סכם את מסמך התיק לקראת הדיון בסיכום מעוגן-מקור.', [
    { worker: 'summarizer', inputRef: 'source:legal-case' },
  ]);
  console.log(`taskId : ${plan.taskId}`);
  console.log(`goal   : ${plan.goal}`);
  console.log(`steps  : ${plan.steps.length} (תקרה: ${plan.maxSteps})`);
  plan.steps.forEach((s) =>
    console.log(`  • ${s.stepId} → worker=${s.worker} input=${s.inputRef} dependsOn=[${s.dependsOn}]`),
  );

  // ── ביצוע ──
  // המנהל מנתב; העובד מבצע. המנהל אינו מבצע תת-משימות בעצמו.
  divider('2 · ביצוע (Worker ← Shared Memory → Worker)');
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

  // ── הרכבה ──
  // הרכבת הפלט הסופי מתוצרי העובדים שבזיכרון. כל נקודה נושאת עוגן-מקור,
  // והשרשרת המאוחדת היא רצף העוגנים שמאחורי הסיכום כולו.
  divider('3 · הרכבת פלט סופי (סיכום מעוגן-מקור)');
  const points = memory
    .find((e) => e.kind === 'worker-output' && e.taskId === plan.taskId)
    .flatMap((e) => e.payload.summary);

  points.forEach((p, i) => {
    console.log(`  ${i + 1}. ${p.point}`);
    console.log(`     ↳ עוגן [${p.evidence.ref}]: "${p.evidence.quote}"`);
  });

  const evidenceChain = points.map((p) => p.evidence.ref);
  console.log('\nunified evidence chain:', JSON.stringify(evidenceChain));

  // ── יומן מלא (שקיפות) ──
  divider('4 · יומן מלא (append-only · שקיפות וממשל)');
  const log = memory.all();
  console.log(`total memory entries (append-only): ${log.length}`);
  log.forEach((e) =>
    console.log(
      `  [${e.entryId}] ${e.ts} author=${e.author.padEnd(11)} kind=${e.kind.padEnd(14)} step=${e.stepId} evidence=${e.evidence.length}`,
    ),
  );

  // ── אימות הממשל ──
  divider('5 · אימות מנגנוני הממשל');
  verifyGovernance(memory);

  divider('הוכחת ההיתכנות הושלמה ✓');
}

/**
 * כל בדיקה מַפעילה את המנגנון בפועל — אכיפה בקוד, לא רק תיעוד.
 */
function verifyGovernance(memory) {
  const checks = [
    // בדיקה א': כתיבת תוצר עובד ללא evidence נדחית
    ['evidence[] mandatory on worker output', () => {
      let threw = false;
      try {
        memory.append({ taskId: 't', author: 'rogue', stepId: 'x', kind: 'worker-output', payload: {}, evidence: [] });
      } catch (err) {
        threw = /evidence/.test(err.message);
      }
      if (!threw) throw new Error('worker output without evidence was accepted');
    }],

    // בדיקה ב': תוכנית החורגת מתקרת הצעדים נדחית
    ['step ceiling halts runaway loops', () => {
      const m = new Manager(new SharedMemory(), { maxSteps: 2 });
      let threw = false;
      try {
        m.plan('g', [{ worker: 'w' }, { worker: 'w' }, { worker: 'w' }]);
      } catch (err) {
        threw = /step ceiling/.test(err.message);
      }
      if (!threw) throw new Error('plan exceeding ceiling was accepted');
    }],

    // בדיקה ג': עצירה בטוחה על קלט חסר — תוצר partial לסקירת אדם
    ['worker safe-stops on missing input', () => {
      const mem = new SharedMemory();
      const w = new SummarizerWorker(mem, { sources: {} });
      const out = w.execute({ stepId: 's1', dependsOn: [], inputRef: 'source:missing' }, 'tX');
      if (out.payload.status !== 'partial' || !out.payload.flags.includes('incomplete-source')) {
        throw new Error('worker did not safe-stop on missing input');
      }
    }],

    // בדיקה ד': append-only — היומן רק גדל, רשומות קפואות, אין מוטציה
    ['memory is append-only (full audit)', () => {
      const mem = new SharedMemory();
      const e1 = mem.append({ taskId: 't', author: 'a', kind: 'note', payload: { message: 'one' } });
      const len1 = mem.size;
      mem.append({ taskId: 't', author: 'a', kind: 'note', payload: { message: 'two' } });
      if (mem.size !== len1 + 1) throw new Error('log did not grow by exactly one');
      if (!Object.isFrozen(e1)) throw new Error('entry is not frozen');
      if ('delete' in mem || 'update' in mem) throw new Error('memory exposes mutation');
    }],

    // בדיקה ה': תוצר חלקי מסומן לסקירת אדם
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

try {
  main();
} catch (err) {
  console.error('\n[FATAL]', err.message);
  process.exit(1);
}
