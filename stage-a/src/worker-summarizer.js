'use strict';

// סוכן עובד — Summarizer. סיכום מעוגן-מקור.
// אינו מודע למנהל ואינו מודע לעובדים אחרים: מקבל תת-משימה + זיכרון משותף,
// פותר קלט, מבצע לפי חוזה ה-AGENT.md שלו, וכותב תוצר מעוגן חזרה לזיכרון.

// תמצית חוזה ה-AGENT.md: כל טענה בסיכום מעוגנת בשורת מקור; אין להמציא תוכן;
// קלט חסר → עצירה בטוחה (תוצר partial עם דגל incomplete-source לסקירת אדם).
const AGENT_CONTRACT = Object.freeze({
  id: 'summarizer',
  role: 'מסכם מסמכים בסיכום מעוגן-מקור',
  rules: Object.freeze([
    'כל נקודת סיכום מצרפת evidence המפנה לשורת המקור.',
    'אין להמציא תוכן שאינו קיים במקור.',
    'קלט חסר → תוצר partial + דגל incomplete-source (עצירה בטוחה).',
  ]),
});

class SummarizerWorker {
  constructor(memory, { sources = {} } = {}) {
    this.memory = memory;
    this.sources = sources; // מאגר מקורות מקומי — חיסיון, אפס תלות חיצונית
    this.id = AGENT_CONTRACT.id;
  }

  // inputRef מצביע על מקור ('source:<id>') או על תוצר צעד קודם ('step:<id>').
  _resolveInput(step) {
    const ref = step.inputRef || '';
    if (ref.startsWith('source:')) {
      return this.sources[ref.slice('source:'.length)] || null;
    }
    if (ref.startsWith('step:')) {
      const prev = this.memory.byStep(ref.slice('step:'.length));
      return prev ? { clauses: prev.payload.summary.map((p) => ({ id: p.evidence.ref, text: p.evidence.quote, gist: p.point })) } : null;
    }
    return null;
  }

  execute(step, taskId) {
    const input = this._resolveInput(step);

    // נקודת-אכיפה: עצירה בטוחה. קלט חסר אינו מפיל את המערכת — מסומן partial לסקירת אדם.
    if (!input) {
      return this.memory.append({
        taskId,
        author: this.id,
        stepId: step.stepId,
        kind: 'worker-output',
        payload: {
          status: 'partial',
          flags: ['incomplete-source'],
          summary: [],
          note: `inputRef "${step.inputRef}" לא נפתר — נדרשת סקירת אדם.`,
        },
        // גם תוצר partial מעוגן: העדות היא עצם החֶסֶר.
        evidence: [{ kind: 'missing-input', ref: step.inputRef }],
      });
    }

    const summary = this._summarize(input);

    return this.memory.append({
      taskId,
      author: this.id,
      stepId: step.stepId,
      kind: 'worker-output',
      payload: { status: 'complete', flags: [], summary },
      evidence: summary.map((p) => p.evidence), // ביסוס חובה לכל נקודה
    });
  }

  // סיכום דטרמיניסטי ומעוגן: כל סעיף מקור הופך לנקודה עם ציטוט-עוגן.
  _summarize(input) {
    return input.clauses.map((clause) => ({
      point: clause.gist,
      evidence: { kind: 'source-line', ref: clause.id, quote: clause.text },
    }));
  }
}

module.exports = { SummarizerWorker, AGENT_CONTRACT };
