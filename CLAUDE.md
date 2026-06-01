# CLAUDE.md — OS Entry Point

נקודת הכניסה הראשית של ה-Claude Operating System עבור הריפו.

## Active Modules
- `OPERATING_SYSTEM.md` v1.0.1 — Kernel: עקרונות יסוד, ארכיטקטורת שכבות, רישום מודולים, Boot Block והיררכיית הכרעה.
- `MEMORY.md` v1.0.0 — שכבת זיכרון: schema, כרטיס זהות, Active Focus/Projects, העדפות ופרוטוקול קריאה/כתיבה.
- `DECISION_LOG.md` v1.5.0 — יומן החלטות append-only: 16 החלטות (OS + ULease), רציונל וסטטוס.
- `COWORK_SETUP.md` v1.0.0 — מדריך אונבורדינג ל-Cowork: 7 שלבי הגדרה, Global Instructions, מפת קבצי הקשר ואינטגרציה עם ה-OS.
- `COMMAND_API.md` v1.1.0 — 89 slash commands, composition operators, prompting-frameworks library, drop-in system prompt loaded.
- `marketing-strategy-framework.md` v1.0.0 — Business: מסגרת 10 פרומפטים לבניית אסטרטגיית שיווק מלאה (פסיכולוגיה → תוכנית עמוד).
- `AI_SKILL_MAP.md` v1.0.0 — מפת מיומנויות AI: 4 שלבים (Tools → Workflows → Agentic → Architect), יישומים, ומיקום ULease על המפה.
- `AI_PROGRESSION_PLAN.md` v1.0.0 — תוכנית התקדמות אישית על המפה: Learn-vs-Delegate, ציר זמן צמוד ל-ULease, תוכנית 90 יום ושערי-מעבר.
- `AI_LEARNING_RESOURCES.md` v1.0.0 — קוריקולום AI לפי המפה: משאבים לכל שלב, עוגן IBM Agentic AI & RAG (Coursera), ומסלול אישי.
- `AI_7_SKILLS.md` v1.0.0 — 7 מיומנויות לשליטה ב-AI (2026) + מיפוי ל-OS הקיים (5 מ-7 כבר מיושמים).
- `AI_SKILLS_ACQUISITION.md` v1.0.0 — תוכנית רכישת מיומנויות hands-on (8 שבועות, Build-to-Learn): פרויקט אמיתי ב-ULease לכל מיומנות, שערי-שליטה.
- `AI_CLAUDE_TOOL_SELECTOR.md` v1.0.0 — "איזה Claude לבחור?": עץ החלטה ל-12 כלי Claude (Chat · Code · Cowork · Skills · Routines…), מודלים מומלצים, ומיפוי למשימות ה-OS ו-ULease.
- `INVESTOR_RELATIONS.md` v1.2.0 — IR: חברה, cap table, גיוס 150K, תחזית ומעקב משקיעים.
- `CASES/ULEASE.md` v1.4.0 — תיק ULease 🎯 Leasing.co.il: מודל Marketplace תלת-צדדי + תחזית פיננסית (יוני 26 → דצמ' 27).
- `CASES/ULEASE_SPEC.md` v1.3.0 — איפיון מוצר ומערכת מקצה-לקצה: שחקנים, ארכיטקטורה, Multi-agent (Ultra·Master·Max), מודל נתונים, אינטגרציות ו-roadmap.
- `CASES/ULEASE_DECK.md` v1.2.0 — מצגת פיץ' (13 שקפים): Marp + HTML אינטראקטיבי (הקשה/החלקה/חיצים), נוצר ע"י `CASES/ULEASE_DECK.py`.
- `CASES/ULEASE_METHODOLOGY.md` v1.1.0 — מתודולוגיה: Big Five (OCEAN) להתאמת קונה-רכב, העשרה אינסטרומנטלית, תורת המשחקים, ומו"מ מבוסס-אינטרסים.
- `CASES/ULEASE_HIRING.md` v1.0.0 — ערכת גיוס: מנהל מערכות טכנולוגיה (תיאור תפקיד, מודעת דרושים, שאלות ראיון, תהליך).
- `CASES/ULEASE_IMPORTER_PLAYBOOK.md` v1.1.0 — Playbook מו"מ מול יבואני רכב: כאב, יתרונות, "שירות שלא היה כמותו", סקריפט, התנגדויות ופיילוט.
- `CASES/ULEASE_LEASING_PLAYBOOK.md` v1.1.0 — Playbook מו"מ ליבואנים מקבילים (reach/מט"ח/אמון) וחברות ליסינג (disposal דו-כיווני + sourcing במכרז מחיר-שני).
- `CASES/ULEASE_DEMAND_PLAYBOOK.md` v1.0.0 — Playbook צד-הביקוש: יחידת כלכלה (CPL ₪103, ROI ×4.9), 3 פרסונות Big Five, 6 ערוצי רכישה, משפך, ציות ו-KPIs — סוגר את ממצא C4.
- `CASES/ULEASE_FINANCE_INSURANCE.md` v1.1.0 — מימון/ביטוח + חיתום דיגיטלי מקצה-לקצה: שותפים, זרימת חיתום, ניתוב רב-מלווה, התאמת Big Five, ודגלי רגולציה.
- `CASES/ULEASE_OUTREACH_SCRIPTS.md` v1.2.0 — סקריפטים לפנייה (שיחה/מייל/וואטסאפ) ל-4 סגמנטי היצע + follow-up.
- `CASES/ULEASE_OUTBOUND_ENGINE.md` v1.1.0 — בלופרינט מנוע outbound (n8n + Claude): 8 שכבות לאקווזיציית צד-היצע, מודלי Haiku/Sonnet, KPIs.
- `CASES/ULEASE_TECH_ONBOARDING.md` v1.0.0 — Onboarding ל-Tech Lead: יום 0/1, רשימת קריאה ב-OS, ותוכנית 30·60·90.
- `CASES/ULEASE_LAUNCH_CHECKLIST.md` v1.1.0 — צ'קליסט השקה (שבועיים): דומיין, משפטי, MVP, תוכן, outreach, QA ולוח שבועי.
- `CASES/ULEASE_DASHBOARD.html` v1.2.0 — דשבורד מנהלים אינטראקטיבי (RTL): KPIs, גרפים (הכנסה/מזומן/עסקאות/הוצאות/רווחיות), תמהילי הכנסה והוצאה, וצ'קליסט השקה חי; נוצר ע"י `ULEASE_DASHBOARD.py`.
- `CASES/ULEASE_AUDIT.md` v1.3.0 — דוח ביקורת מקצה-לקצה (1.6.2026): 4 סוכני ביקורת מקבילים, 41 ממצאים (9🔴/21🟡/11🔵) ותוכנית תיקון ב-3 גלים לקראת השקה וגיוס.

## Module Load Order
1. `OPERATING_SYSTEM.md`
2. `MEMORY.md`
3. `DECISION_LOG.md`          ← יומן החלטות (Memory)
4. `COWORK_SETUP.md`          ← חיבור התיקייה וטעינת ההקשר (אונבורדינג)
5. `COMMAND_API.md`           ← לפני הקטגוריות העסקיות
6. `marketing-strategy-framework.md`  ← Business: אסטרטגיית שיווק
7. `AI_*` (SKILL_MAP · PROGRESSION_PLAN · LEARNING_RESOURCES · 7_SKILLS · SKILLS_ACQUISITION · CLAUDE_TOOL_SELECTOR)  ← Knowledge (on-demand)
8. `INVESTOR_RELATIONS.md`    ← שכבת עסק: משקיעים וגיוס
9. `CASES/*.md`               ← תיקים פעילים (ULease 🎯)

## Activation
כדי להפעיל את ה-Command API, טען את בלוק ה-System Prompt מסעיף 8 ב-[`COMMAND_API.md`](./COMMAND_API.md)
אל ההקשר (`userPreferences` / system prompt / טעינת OS). זה מה שגורם ל-Claude לזהות תחביר `/command`.
