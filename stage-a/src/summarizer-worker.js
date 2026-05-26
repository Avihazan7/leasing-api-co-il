'use strict';

/**
 * SummarizerWorker — סוכן עובד יחיד (שלב א')
 *
 * מממש את החוזה של Summarizer.AGENT.md ברמת הוכחת-היתכנות:
 * מקבל תת-משימה מהזיכרון המשותף, מבצע סיכום אקסטרקטיבי נאמן-למקור,
 * וכותב תוצר חזרה לזיכרון — עם שדה evidence[] חובה.
 *
 * עיקרון מפתח (לפי האפיון): העובד אינו מודע למנהל ואינו מודע לעובדים אחרים.
 * הוא מכיר רק את הזיכרון המשותף. כך נשמרת מודולריות.
 *
 * גבולות שמומשו מתוך ה-AGENT.md:
 *  - קלט חסר → עוצר ומחזיר incomplete-source, אינו מסכם חלקית.
 *  - לעולם אינו מוסיף עובדה שאינה במקור (סיכום אקסטרקטיבי בלבד).
 *  - כל טענה בתקציר מעוגנת למזהה מקור (mono).
 */
class SummarizerWorker {
  constructor() {
    this.name = 'summarizer';
  }

  /**
   * מבצע את תת-המשימה.
   * @param {object} input - { sourceText, sourceId, maxSentences }
   * @returns {object} payload + evidence, או דגל עצירה.
   */
  run(input) {
    // עצירה בטוחה: קלט חסר או פגום
    if (!input || !input.sourceText || !input.sourceText.trim()) {
      return {
        stop: true,
        flag: 'incomplete-source',
        note: 'No source text provided; summarizer refuses to invent content.',
      };
    }

    const sourceId = input.sourceId || 'src:unknown';
    const text = input.sourceText.trim();

    // פיצול למשפטים (תומך בעברית ובאנגלית)
    const sentences = text
      .split(/(?<=[.!?。])\s+|\n+/)
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    // תנאי עצירה: מסמך קצר מסף משמעות
    if (sentences.length <= 1) {
      return {
        stop: true,
        flag: 'no-summary-needed',
        note: 'Source is a single sentence; returned as-is.',
        payload: { summary: text, coverage: 'full' },
        evidence: [sourceId],
      };
    }

    // דירוג אקסטרקטיבי פשוט: לפי תדירות מילים (דטרמיניסטי, ללא מודל)
    const freq = {};
    for (const w of text.toLowerCase().match(/[\p{L}]+/gu) || []) {
      if (w.length < 3) continue;
      freq[w] = (freq[w] || 0) + 1;
    }
    const score = (s) =>
      (s.toLowerCase().match(/[\p{L}]+/gu) || []).reduce(
        (sum, w) => sum + (freq[w] || 0),
        0
      ) / Math.max(1, s.split(/\s+/).length);

    const maxN = Math.max(
      1,
      Math.min(
        input.maxSentences || Math.ceil(sentences.length / 3),
        sentences.length
      )
    );

    // בחירת המשפטים המדורגים-גבוה, תוך שמירת סדר המקור
    const ranked = sentences
      .map((s, i) => ({ s, i, sc: score(s) }))
      .sort((a, b) => b.sc - a.sc)
      .slice(0, maxN)
      .sort((a, b) => a.i - b.i);

    const summary = ranked.map((r) => r.s).join(' ');

    // כל משפט בתקציר מעוגן למקור (mono) עם מספר המשפט המקורי
    const evidence = ranked.map((r) => `${sourceId}#s${r.i + 1}`);

    return {
      stop: false,
      payload: {
        summary,
        coverage: maxN < sentences.length ? 'partial' : 'full',
        source_sentences: sentences.length,
        summary_sentences: maxN,
      },
      evidence,
    };
  }
}

module.exports = { SummarizerWorker };
