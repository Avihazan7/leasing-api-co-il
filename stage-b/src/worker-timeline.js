'use strict';

// סוכן עובד — Timeline-Builder. בניית ציר-זמן מעוגן-מקור.
// אינו מודע למנהל ואינו מודע לעובדים אחרים: מקבל תת-משימה + זיכרון משותף,
// פותר קלט, ומחזיר ציר-זמן מסודר שכל פריט בו מעוגן לסעיף מקור (mono).

// תמצית חוזה ה-AGENT.md: כל פריט בציר-הזמן מעוגן לשורת מקור; סדר דטרמיניסטי;
// אין המצאת אירועים; קלט חסר → תוצר partial עם דגל incomplete-source.
const AGENT_CONTRACT = Object.freeze({
  id: 'timeline-builder',
  role: 'בונה ציר-זמן מאבני-דרך וחלוֹנות-זמן שכבר קיימים במקור',
  rules: Object.freeze([
    'כל פריט בציר-הזמן מצרף evidence המפנה לשורת המקור.',
    'אין להמציא אירועים, תאריכים או מועדים שאינם במקור.',
    'סדר הפריטים בציר-הזמן יציב ודטרמיניסטי (לא תלוי-מודל).',
    'קלט חסר → תוצר partial + דגל incomplete-source (עצירה בטוחה).',
  ]),
});

// תבניות זיהוי דטרמיניסטיות — נסרקות לכל סעיף.
// kind מציין את שכבת ציר-הזמן: milestone (אבן-דרך), duration (משך),
// recurring (חיוב חוזר). הסדר ביציאה נקבע לפי השכבה ואז לפי מזהה הסעיף.
const PATTERNS = [
  { kind: 'milestone', re: /מיום\s+מסירת/u,       label: () => 'מסירת הרכב (T0)' },
  { kind: 'milestone', re: /בתום\s+התקופה/u,      label: () => 'בתום התקופה' },
  { kind: 'duration',  re: /(\d+)\s*חודשים/u,     label: (m) => `${m[1]} חודשים` },
  { kind: 'duration',  re: /(\d+)\s*שנים/u,       label: (m) => `${m[1]} שנים` },
  { kind: 'recurring', re: /תשלום\s+חודשי/u,      label: () => 'חיוב חודשי שוטף' },
  { kind: 'recurring', re: /(\d[\d,]*)\s*ק"מ/u,   label: (m) => `מכסת ק"מ שנתית: ${m[1]}` },
];

const LAYER_ORDER = { milestone: 0, duration: 1, recurring: 2 };

class TimelineWorker {
  constructor(memory, { sources = {} } = {}) {
    this.memory = memory;
    this.sources = sources;
    this.id = AGENT_CONTRACT.id;
  }

  // inputRef מצביע על מקור ('source:<id>') או על תוצר צעד קודם ('step:<id>').
  // במצב step: נקודות הסיכום נצרכות כ"סעיפים" כדי לאפשר הרכבה רב-שלבית.
  _resolveInput(step, taskId) {
    const ref = step.inputRef || '';
    if (ref.startsWith('source:')) {
      return this.sources[ref.slice('source:'.length)] || null;
    }
    if (ref.startsWith('step:')) {
      const prev = this.memory.byStep(ref.slice('step:'.length), taskId);
      if (!prev) return null;
      return {
        clauses: prev.payload.summary.map((p) => ({
          id: p.evidence.ref,
          text: p.evidence.quote,
          gist: p.point,
        })),
      };
    }
    return null;
  }

  execute(step, taskId) {
    const input = this._resolveInput(step, taskId);

    // נקודת-אכיפה: עצירה בטוחה — קלט חסר אינו מפיל את המערכת.
    if (!input) {
      return this.memory.append({
        taskId,
        author: this.id,
        stepId: step.stepId,
        kind: 'worker-output',
        payload: {
          status: 'partial',
          flags: ['incomplete-source'],
          timeline: [],
          note: `inputRef "${step.inputRef}" לא נפתר — נדרשת סקירת אדם.`,
        },
        // גם תוצר partial מעוגן: העדות היא עצם החֶסֶר.
        evidence: [{ kind: 'missing-input', ref: step.inputRef }],
      });
    }

    const timeline = this._buildTimeline(input);

    return this.memory.append({
      taskId,
      author: this.id,
      stepId: step.stepId,
      kind: 'worker-output',
      payload: { status: 'complete', flags: [], timeline },
      evidence: timeline.map((e) => e.evidence), // ביסוס חובה לכל פריט
    });
  }

  // בנייה דטרמיניסטית: לכל סעיף, התאמת תבניות → פריטי ציר-זמן עם עוגן.
  _buildTimeline(input) {
    const items = [];
    for (const clause of input.clauses) {
      for (const p of PATTERNS) {
        const m = clause.text.match(p.re);
        if (m) {
          items.push({
            kind: p.kind,
            when: p.label(m),
            what: clause.gist,
            evidence: { kind: 'source-line', ref: clause.id, quote: clause.text },
          });
        }
      }
    }
    // מיון יציב: שכבה (milestone → duration → recurring), ואז מזהה מקור.
    items.sort(
      (a, b) =>
        LAYER_ORDER[a.kind] - LAYER_ORDER[b.kind] ||
        a.evidence.ref.localeCompare(b.evidence.ref),
    );
    return items;
  }
}

module.exports = { TimelineWorker, AGENT_CONTRACT };
