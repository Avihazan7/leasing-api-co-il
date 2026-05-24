'use strict';

// סוכן המנהל — מתכנן ומנתב בלבד. אינו מבצע תת-משימות בעצמו.
// מפרק מטרה לתוכנית מובנית, אוכף תקרת צעדים, וכותב את התוכנית לזיכרון המשותף.

let _taskCounter = 0;

class Manager {
  constructor(memory, { maxSteps = 5 } = {}) {
    this.memory = memory;
    this.maxSteps = maxSteps;
  }

  // מטרה → תוכנית. כותב את התוכנית לזיכרון המשותף ומחזיר אותה.
  plan(goal, steps) {
    const taskId = `task-${++_taskCounter}`;

    // נקודת-אכיפה: תקרת צעדים עוצרת לולאות בורחות לפני שהן מתחילות.
    if (steps.length > this.maxSteps) {
      throw new Error(`manager: plan exceeds step ceiling (${steps.length} > ${this.maxSteps})`);
    }

    const normalized = steps.map((s, i) => ({
      stepId: s.stepId || `s${i + 1}`,
      worker: s.worker,
      dependsOn: s.dependsOn || [],
      inputRef: s.inputRef || null,
    }));

    const plan = { taskId, goal, steps: normalized, maxSteps: this.maxSteps };

    // למנהל אין חובת evidence — הוא מנתב, אינו מבסס טענות.
    this.memory.append({ taskId, author: 'manager', kind: 'plan', payload: plan });

    return plan;
  }

  // ניתוב: הצעדים שתלותם כבר הושלמה בזיכרון וטרם בוצעו, לפי סדר הביצוע.
  nextSteps(plan) {
    const done = new Set(
      this.memory
        .find((e) => e.kind === 'worker-output' && e.taskId === plan.taskId)
        .map((e) => e.stepId),
    );
    return plan.steps.filter(
      (s) => !done.has(s.stepId) && s.dependsOn.every((d) => done.has(d)),
    );
  }
}

module.exports = { Manager };
