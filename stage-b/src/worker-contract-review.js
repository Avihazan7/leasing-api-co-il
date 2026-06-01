'use strict';

// סוכן עובד — Contract-Review. סקירת סעיפי חוזה כנגד ספר-כללים פנימי.
// אינו מודע למנהל ואינו מודע לעובדים אחרים. צורך מקור כקלט עיקרי, וקורא
// תוצרים של צעדים קודמים מהזיכרון המשותף לפי dependsOn (העשרת הקשר).
//
// כל ממצא — סיכון, אישור, או חֶסֶר — מעוגן ל-evidence. אין שיפוט ללא ביסוס.

// תמצית חוזה ה-AGENT.md: כללי הסקירה דטרמיניסטיים וניתנים לביקורת; אין
// המצאת ממצאים; אבסנציה (חֶסֶר סעיף נדרש) מסומנת בנפרד כ-missing-clause.
const AGENT_CONTRACT = Object.freeze({
  id: 'contract-review',
  role: 'סוקר חוזה ליסינג ומסמן סיכונים, אישורים וסעיפים חסרים',
  rules: Object.freeze([
    'כל ממצא מעוגן ל-evidence המפנה לשורת המקור (או לחֶסֶר מסומן).',
    'כללי הסקירה דטרמיניסטיים — ניתנים לקריאה, ביקורת ותחזוקה.',
    'אבסנציה של סעיף נדרש מסומנת כ-missing-clause; אין שתיקה.',
    'קלט חסר → תוצר partial + דגל incomplete-source (עצירה בטוחה).',
  ]),
});

// ספר-כללים — כל כלל בודק תבנית קונקרטית בסעיפי המקור.
// severity: info (סעיף תקין), medium / high (סיכון לנטל-תזרים או לכושר התקשרות).
const RULES = Object.freeze([
  {
    id: 'R1',
    topic: 'תקופת התקשרות מוגדרת',
    severity: 'info',
    detect: (c) => /\d+\s*חודשים/u.test(c.text),
    finding: 'תקופת ההתקשרות מצוינת במפורש.',
  },
  {
    id: 'R2',
    topic: 'תשלום חודשי גבוה',
    severity: 'high',
    detect: (c) => {
      const m = c.text.match(/(\d[\d,]*)\s*ש"ח/u);
      if (!m) return false;
      const v = Number(m[1].replace(/,/g, ''));
      return v >= 1800;
    },
    finding: 'תשלום חודשי ≥ 1,800 ש"ח — סיכון נטל-תזרים, יש לאמת יחס PTI.',
  },
  {
    id: 'R3',
    topic: 'מכסת ק"מ הדוקה',
    severity: 'medium',
    detect: (c) => {
      const m = c.text.match(/(\d[\d,]*)\s*ק"מ/u);
      if (!m) return false;
      const v = Number(m[1].replace(/,/g, ''));
      return v <= 20000;
    },
    finding: 'מכסת ק"מ שנתית ≤ 20,000 — חריגה צפויה תוסיף עלות שולית.',
  },
  {
    id: 'R4',
    topic: 'שווי שייר גבוה',
    severity: 'high',
    detect: (c) => {
      const m = c.text.match(/(\d+)\s*%/u);
      if (!m) return false;
      return Number(m[1]) >= 25;
    },
    finding: 'שווי שייר ≥ 25% — אופציית רכישה יקרה בתום התקופה.',
  },
]);

// סעיפים שחובה לכלול. אם לא נמצאו במקור — מסומנים כ-missing-clause.
const REQUIRED_TOPICS = Object.freeze([
  {
    topic: 'יציאה מוקדמת',
    cue: /יציאה|ביטול|הפסקה\s+מוקדמת/u,
    severity: 'high',
    finding: 'חוזה ללא סעיף יציאה מוקדמת — סיכון התחייבות בלתי-הפיכה.',
  },
]);

class ContractReviewWorker {
  constructor(memory, { sources = {} } = {}) {
    this.memory = memory;
    this.sources = sources;
    this.id = AGENT_CONTRACT.id;
  }

  // קלט עיקרי: מקור או תוצר צעד קודם. הקשר נוסף: תוצרי dependsOn מהזיכרון.
  _resolveInput(step, taskId) {
    const ref = step.inputRef || '';
    let source = null;

    if (ref.startsWith('source:')) {
      source = this.sources[ref.slice('source:'.length)] || null;
    } else if (ref.startsWith('step:')) {
      const prev = this.memory.byStep(ref.slice('step:'.length), taskId);
      if (prev) {
        source = {
          clauses: prev.payload.summary.map((p) => ({
            id: p.evidence.ref,
            text: p.evidence.quote,
            gist: p.point,
          })),
        };
      }
    }

    // קונטקסט תלוי-צעדים: כל צעד שצוין ב-dependsOn נקרא מהזיכרון המשותף.
    // זוהי הוכחת התלות בין-צעדים — העובד אינו מקבל את ההקשר מהמנהל, אלא
    // ניגש ישירות לזיכרון לפי המזהים שכבר נכתבו לתוכנית.
    const context = (step.dependsOn || [])
      .map((d) => {
        const e = this.memory.byStep(d, taskId);
        return e ? { stepId: d, author: e.author, payload: e.payload } : null;
      })
      .filter(Boolean);

    return source ? { source, context } : null;
  }

  execute(step, taskId) {
    const input = this._resolveInput(step, taskId);

    if (!input) {
      return this.memory.append({
        taskId,
        author: this.id,
        stepId: step.stepId,
        kind: 'worker-output',
        payload: {
          status: 'partial',
          flags: ['incomplete-source'],
          risks: [],
          cleared: [],
          missing: [],
          contextUsed: [],
          note: `inputRef "${step.inputRef}" לא נפתר — נדרשת סקירת אדם.`,
        },
        evidence: [{ kind: 'missing-input', ref: step.inputRef }],
      });
    }

    const { risks, cleared, missing } = this._review(input.source);

    // עוגנים לתוצרי הצעדים שצרכנו — חוצים גבולות-צעדים בתוך אותה משימה.
    const contextRefs = input.context.map((c) => ({
      kind: 'step-context',
      ref: c.stepId,
      quote: `${c.author}:${c.payload.status}`,
    }));

    return this.memory.append({
      taskId,
      author: this.id,
      stepId: step.stepId,
      kind: 'worker-output',
      payload: {
        status: 'complete',
        flags: [],
        risks,
        cleared,
        missing,
        contextUsed: input.context.map((c) => c.stepId),
      },
      // ביסוס מאוחד: ממצאי-תוכן + עוגני-הקשר חוצי-צעדים.
      evidence: [
        ...risks.map((r) => r.evidence),
        ...cleared.map((c) => c.evidence),
        ...missing.map((m) => m.evidence),
        ...contextRefs,
      ],
    });
  }

  // הפעלת הכללים על המקור. אין שיפוט מעבר למה שהמקור אומר במפורש.
  _review(source) {
    const risks = [];
    const cleared = [];

    for (const clause of source.clauses) {
      for (const rule of RULES) {
        if (rule.detect(clause)) {
          const item = {
            ruleId: rule.id,
            topic: rule.topic,
            severity: rule.severity,
            finding: rule.finding,
            evidence: { kind: 'source-line', ref: clause.id, quote: clause.text },
          };
          if (rule.severity === 'info') cleared.push(item);
          else risks.push(item);
        }
      }
    }

    // בדיקת חֶסֶר — סעיפים נדרשים שלא נמצאו במקור.
    const missing = [];
    for (const req of REQUIRED_TOPICS) {
      const found = source.clauses.some((c) => req.cue.test(c.text));
      if (!found) {
        missing.push({
          topic: req.topic,
          severity: req.severity,
          finding: req.finding,
          // העדות היא עצם החֶסֶר — דרך אחידה ל-append לאכוף ביסוס.
          evidence: {
            kind: 'missing-clause',
            ref: `req:${req.topic}`,
            quote: '(לא נמצא במקור — חסר סעיף נדרש)',
          },
        });
      }
    }

    return { risks, cleared, missing };
  }
}

module.exports = { ContractReviewWorker, AGENT_CONTRACT };
