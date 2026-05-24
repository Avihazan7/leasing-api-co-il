'use strict';

// אפיק הזיכרון המשותף — append-only, אוכף ביסוס (evidence) על תוצרי עובדים.
// זהו ה-single-source-of-truth שדרכו המנהל והעובדים מתקשרים. אין דרך
// למחוק או לשכתב רשומה: שקיפות וביקורת מלאות נאכפות במבנה עצמו.

class SharedMemory {
  constructor() {
    this._log = []; // append-only — לעולם לא נמחק ולא משוכתב
    this._seq = 0;
  }

  // כתיבת רשומה. תוצר עובד (kind === 'worker-output') חייב evidence[] לא-ריק.
  append({ taskId, author, stepId = null, kind = 'note', payload, evidence }) {
    if (!taskId) throw new Error('shared-memory: taskId required');
    if (!author) throw new Error('shared-memory: author required');

    // נקודת-אכיפה: ביסוס חובה על כל תוצר עובד.
    if (kind === 'worker-output' && (!Array.isArray(evidence) || evidence.length === 0)) {
      throw new Error(`shared-memory: evidence[] is mandatory on worker output (stepId=${stepId})`);
    }

    const entry = Object.freeze({
      entryId: `e${++this._seq}`,
      taskId,
      author,
      stepId,
      kind,
      payload,
      evidence: Object.freeze([...(evidence || [])]),
      ts: new Date().toISOString(),
    });

    this._log.push(entry);
    return entry;
  }

  // קריאה בלבד. אין כאן delete/update — append-only מעצם הממשק.
  all() {
    return this._log.slice();
  }

  find(predicate) {
    return this._log.filter(predicate);
  }

  // תוצר העובד עבור צעד נתון (בתוך משימה, אם נמסרה).
  byStep(stepId, taskId = null) {
    return (
      this._log.find(
        (e) =>
          e.kind === 'worker-output' &&
          e.stepId === stepId &&
          (taskId === null || e.taskId === taskId),
      ) || null
    );
  }

  get size() {
    return this._log.length;
  }
}

module.exports = { SharedMemory };
