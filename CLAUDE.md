# CLAUDE.md — OS Entry Point

נקודת הכניסה הראשית של ה-Claude Operating System עבור הריפו.

## Active Modules
- `OPERATING_SYSTEM.md` v1.8.0 — Kernel: עקרונות יסוד, ארכיטקטורת שכבות, רישום מודולים (§3 + §3.1 תשתית תפעולית), Boot Block והיררכיית הכרעה.
- `MEMORY.md` v1.1.0 — שכבת זיכרון: schema, כרטיס זהות **מלא**, Active Focus/Projects, העדפות ופרוטוקול קריאה/כתיבה.
- `DECISION_LOG.md` v1.28.0 — יומן החלטות append-only: 41 החלטות (OS + ULease), רציונל וסטטוס.
- `COWORK_SETUP.md` v1.2.0 — מדריך אונבורדינג ל-Cowork: 7 שלבי הגדרה, Global Instructions, מפת קבצי הקשר, אינטגרציה עם ה-OS + ראש המטה (5 תפקידים מתוזמנים) — מיושם בפועל ב-`COWORK/`.
- `PROJECTS_SETUP.md` v1.0.0 — Claude Projects: 3 פרויקטים (השקה 🎯 · גיוס ₪150K · Claude OS) — תוצר אחד לכל פרויקט, הוראות drop-in, רשימות העלאה ובדיקות קבלה.
- `COMMAND_API.md` v1.2.0 — 89 slash commands, composition operators, prompting-frameworks library (כולל Opus 4.8 deltas §7.7), drop-in system prompt loaded.
- `COMMAND_API_TASKS.md` v1.0.0 — ספריית פקודות משימה: 98 פקודות ב-9 קטגוריות (99 Claude Commands) — אימייל, כתיבה, החלטות, למידה, תכנון, brainstorm, קריירה, תוכן, פגישות — ממופות לתרחישי ULease.
- `marketing-strategy-framework.md` v1.0.0 — Business: מסגרת 10 פרומפטים לבניית אסטרטגיית שיווק מלאה (פסיכולוגיה → תוכנית עמוד).
- `AI_SKILL_MAP.md` v1.0.0 — מפת מיומנויות AI: 4 שלבים (Tools → Workflows → Agentic → Architect), יישומים, ומיקום ULease על המפה.
- `AI_PROGRESSION_PLAN.md` v1.0.0 — תוכנית התקדמות אישית על המפה: Learn-vs-Delegate, ציר זמן צמוד ל-ULease, תוכנית 90 יום ושערי-מעבר.
- `AI_LEARNING_RESOURCES.md` v1.0.0 — קוריקולום AI לפי המפה: משאבים לכל שלב, עוגן IBM Agentic AI & RAG (Coursera), ומסלול אישי.
- `AI_7_SKILLS.md` v1.0.0 — 7 מיומנויות לשליטה ב-AI (2026) + מיפוי ל-OS הקיים (5 מ-7 כבר מיושמים).
- `AI_SKILLS_ACQUISITION.md` v1.0.0 — תוכנית רכישת מיומנויות hands-on (8 שבועות, Build-to-Learn): פרויקט אמיתי ב-ULease לכל מיומנות, שערי-שליטה.
- `AI_TYPES.md` v1.1.0 — טקסונומיית סוגי AI (Traditional·Generative·Agentic, 3×9 יכולות) + מיפוי מלא ל-ULease ולמפת המיומנויות + ההסבר הפשוט (צ'אטבוט מול סוכן).
- `AI_CLAUDE_TOOL_SELECTOR.md` v1.2.0 — "איזה Claude לבחור?": עץ החלטה ל-15 כלי Claude (Chat · Code · Cowork · Skills · Excel · Artifacts…), מודלים מומלצים + מנוף Effort, ומיפוי למשימות ה-OS ו-ULease.
- `AI_CLAUDE_STACK_2026.md` v1.4.0 — Claude Stack 2026: 4 עמודי ה-cheat sheet (Cowork · Projects · Skills · Code), כלל הזהב, מיפוי ה-build התפעולי בריפו, סולם 7 הרמות (אתה ברמה 6/7), Agent Teams כמסלול prototype ל-Ultra·Master·Max, ה-Agent Extension Stack (Skills·MCP·Subagents·Hooks·Plugins) + סיכוני סוכנים (Prompt Injection → Guardian).
- `AI_CLAUDE_GLOSSARY.md` v1.0.0 — מילון Claude: 30 מונחים בחמש קבוצות + מיפוי "איפה אצלך" (21/30 כבר מיושמים ב-OS) — האחות השלישית של Selector ו-Stack.
- `AI_RAG_DESIGN.md` v1.0.0 — תכנון RAG: 15 הטעויות ששוברות מערכות RAG ב-Retrieval + פתרונות, ב-4 שכבות, ממופות לרכיבי ULease (Deal Score, Q&A Bot) עם צ'קליסט design review ל-Tech Lead — משלים את שכבת ה-RAG באיפיון (§7.1).
- `AI_PROJECT_STRUCTURE.md` v1.0.0 — מבנה פרויקט AI: תקן 4 התיקיות (prompts · data · agents · evals) + מיפוי מלא לרכיבי האיפיון — השלד שריפו הפלטפורמה של ULease יקום עליו ביום 1 של ה-Tech Lead.
- `AI_ROLES_2026.md` v1.0.0 — תפקידי ה-AI של 2026: 21 תפקידים ממופים — המייסד (3), ה-Tech Lead (5 בכובע אחד), Guardian (2) — מאמת את הגדרת התפקיד ב-ULEASE_HIRING והופך אותה להצעת ערך לגיוס.
- `AI_CLAUDE_ENGINEER_ROADMAP.md` v1.0.0 — רודמאפ Claude AI Engineer: 15 שלבים ממופים מול ה-OS — 11/15 כבר בנויים; הפער (12–14) = הגדרת ה-Tech Lead; שלב 15 = השקת ULease.
- `AI_DATA_BI.md` v1.4.0 — יסודות BI ומידול נתונים (Power BI כמקרה לימוד, 20 נושאים): צינור BI, ETL, ה-star schema של ULease, DAX + Time Intelligence + 16 הפונקציות הפיננסיות (PMT · IRR · פחת/ערך שייר — המתמטיקה של הליסינג), ויזואליזציה, אינטראקטיביות, **RLS**, תפעול כשירות (התראות · מנויי דוחות · הרשאות) + מבחנים סטטיסטיים להחלטות — ממופה ל-M9 + הכרעת כלי ל-Tech Lead.
- `AI_SYSTEM_DESIGN.md` v1.2.0 — יסודות System Design: שער כניסה (Gateway·Proxy·LB), 8 סגנונות API (כולל Webhook ל-MVP), תורים (Idempotency·DLQ), JWT + מפת 24 הרכיבים (MVP/V1/V2) — ממופים לארכיטקטורת הפלטפורמה + צ'קליסט design review ל-Tech Lead.
- `AI_PROCESS_INTELLIGENCE.md` v1.0.0 — מודיעין תהליכים ובקרת הטמעת AI: GenIQ (HatchWorks×Bloomfilter) — איפה להחיל Gen AI + מדידת ROI (מלכודת ה-56%), אנטומיית סוכן n8n + דפוס Human-in-the-Loop (sendAndWait) ושער בגרות — ממופה לשקיפות SDLC מול ה-Tech Lead, מפת האוטומציות ומנוע ה-outbound.
- `INVESTOR_RELATIONS.md` v1.2.0 — IR: חברה, cap table, גיוס 150K, תחזית ומעקב משקיעים.
- `CASES/ULEASE.md` v1.5.0 — תיק ULease 🎯 Leasing.co.il: מודל Marketplace תלת-צדדי + תחזית פיננסית (יוני 26 → דצמ' 27) + Lean Canvas בעמוד אחד.
- `CASES/ULEASE_SPEC.md` v1.5.0 — איפיון מוצר ומערכת מקצה-לקצה: שחקנים, ארכיטקטורה, Multi-agent (Ultra·Master·Max), שכבת ידע RAG (§7.1), Guardrails & Evals (§7.2), מודל נתונים, אינטגרציות ו-roadmap.
- `CASES/ULEASE_DECK.md` v1.2.0 — מצגת פיץ' (13 שקפים): Marp + HTML אינטראקטיבי (הקשה/החלקה/חיצים), נוצר ע"י `CASES/ULEASE_DECK.py`.
- `CASES/ULEASE_METHODOLOGY.md` v1.1.0 — מתודולוגיה: Big Five (OCEAN) להתאמת קונה-רכב, העשרה אינסטרומנטלית, תורת המשחקים, ומו"מ מבוסס-אינטרסים.
- `CASES/ULEASE_HIRING.md` v1.0.0 — ערכת גיוס: מנהל מערכות טכנולוגיה (תיאור תפקיד, מודעת דרושים, שאלות ראיון, תהליך).
- `CASES/ULEASE_IMPORTER_PLAYBOOK.md` v1.1.0 — Playbook מו"מ מול יבואני רכב: כאב, יתרונות, "שירות שלא היה כמותו", סקריפט, התנגדויות ופיילוט.
- `CASES/ULEASE_LEASING_PLAYBOOK.md` v1.1.0 — Playbook מו"מ ליבואנים מקבילים (reach/מט"ח/אמון) וחברות ליסינג (disposal דו-כיווני + sourcing במכרז מחיר-שני).
- `CASES/ULEASE_DEMAND_PLAYBOOK.md` v1.1.0 — Playbook צד-הביקוש: יחידת כלכלה (CPL ₪103, ROI ×4.9), 3 פרסונות Big Five, 7 ערוצי רכישה (כולל GEO — ציטוט בתשובות AI), משפך, ציות ו-KPIs — סוגר את ממצא C4.
- `CASES/ULEASE_PRICING_SLA.md` v1.1.0 — מחירון רשמי + SLA ספקים: עמלות מדורגות, השוואת Ultra/Max, ו-11 התחייבויות שירות (ingestion, uptime, התחשבנות) — סוגר את ממצא W11.
- `CASES/ULEASE_LEGAL_BRIEF.md` v1.0.0 — תדריך משפטי לעו"ד: 2 שאלות Go-Live (רישוי ניתוב מימון, הסכם ספק/SLA) + 6 נושאים, תוצרים מבוקשים ולוח זמנים — לשליחה לפני הפגישה.
- `CASES/ULEASE_FINANCE_INSURANCE.md` v1.1.0 — מימון/ביטוח + חיתום דיגיטלי מקצה-לקצה: שותפים, זרימת חיתום, ניתוב רב-מלווה, התאמת Big Five, ודגלי רגולציה.
- `CASES/ULEASE_OUTREACH_SCRIPTS.md` v1.2.0 — סקריפטים לפנייה (שיחה/מייל/וואטסאפ) ל-4 סגמנטי היצע + follow-up.
- `CASES/ULEASE_OUTBOUND_ENGINE.md` v1.2.0 — בלופרינט מנוע outbound (n8n + Claude): 8 שכבות לאקווזיציית צד-היצע, מודלי Haiku/Sonnet, KPIs + שער הבגרות (§6.1): שלושה שלבי HITL מ-assist לאוטונומיה מנוטרת.
- `CASES/ULEASE_TECH_ONBOARDING.md` v1.2.0 — Onboarding ל-Tech Lead: יום 0/1, רשימת קריאה ב-OS, תוכנית 30·60·90 + שקיפות SDLC (Jira/GitHub מיום 0, דוח תהליך שבועי, cycle time).
- `CASES/ULEASE_LAUNCH_CHECKLIST.md` v1.3.0 — צ'קליסט השקה (שבועיים): דומיין, משפטי, MVP, תוכן, outreach, GEO, QA ולוח שבועי.
- `CASES/ULEASE_DASHBOARD.html` v1.2.0 — דשבורד מנהלים אינטראקטיבי (RTL): KPIs, גרפים (הכנסה/מזומן/עסקאות/הוצאות/רווחיות), תמהילי הכנסה והוצאה, וצ'קליסט השקה חי; נוצר ע"י `CASES/ULEASE_DASHBOARD.py`.
- `CASES/ULEASE_AUTOMATION_MAP.md` v1.2.0 — מפת אוטומציות AI לפי 10 פונקציות עסקיות: 40 אוטומציות מסוננות ל-ULease, סטטוס (18 כבר בנויות), עדיפות MVP/V1/V2 + 31 ה-Skills המוכנים של Anthropic כשכבת מימוש מדף + שכבת המדידה (§12): baseline, ROI וכלל 90 הימים.
- `CASES/ULEASE_AUDIT.md` v1.4.0 — דוח ביקורת מקצה-לקצה (1.6.2026): 4 סוכני ביקורת מקבילים, 41 ממצאים (9🔴/21🟡/11🔵) — **כולם נסגרו** ב-3 גלי תיקון + מחירון/SLA.

## Module Load Order
1. `OPERATING_SYSTEM.md`
2. `MEMORY.md`
3. `DECISION_LOG.md`          ← יומן החלטות (Memory)
4. `COWORK_SETUP.md`          ← חיבור התיקייה וטעינת ההקשר (אונבורדינג)
5. `PROJECTS_SETUP.md`        ← Claude Projects — workspace קבוע לכל תוצר (Context)
6. `COMMAND_API.md`           ← לפני הקטגוריות העסקיות
7. `COMMAND_API_TASKS.md`     ← ספריית פקודות המשימה (Interface)
8. `marketing-strategy-framework.md`  ← Business: אסטרטגיית שיווק
9. `AI_*` (SKILL_MAP · PROGRESSION_PLAN · LEARNING_RESOURCES · 7_SKILLS · SKILLS_ACQUISITION · TYPES · CLAUDE_TOOL_SELECTOR · CLAUDE_STACK_2026 · CLAUDE_GLOSSARY · RAG_DESIGN · PROJECT_STRUCTURE · ROLES_2026 · CLAUDE_ENGINEER_ROADMAP · DATA_BI · SYSTEM_DESIGN · PROCESS_INTELLIGENCE)  ← Knowledge (on-demand)
10. `INVESTOR_RELATIONS.md`   ← שכבת עסק: משקיעים וגיוס
11. `CASES/*.md`              ← תיקים פעילים (ULease 🎯)

## Working Sets (תשתית תפעולית — לא נטענת בצ'אט)
- `COWORK/` — סביבת העבודה של Claude Cowork: ABOUT-ME (3 קבצי זהות) · TEMPLATES (4 תבניות) · OUTPUTS. נטען ע"י אפליקציית Cowork.
- `.claude/skills/` — 4 Claude Code skills: os-module · os-decision · ulease-refresh · investor-update. נטען אוטומטית ע"י Claude Code לפי טריגר.
- `.claude/agents/os-auditor.md` — סוכן ביקורת עקביות (קריאה-בלבד). רישום קנוני: `OPERATING_SYSTEM.md` §3.1.
- `.github/workflows/` + `scripts/` — CI: בדיקות עקביות מכניות + שחזור ארטיפקטים bit-exact, רץ אוטומטית על כל PR (D-023).

## Activation
כדי להפעיל את ה-Command API, טען את בלוק ה-System Prompt מסעיף 8 ב-[`COMMAND_API.md`](./COMMAND_API.md)
אל ההקשר (`userPreferences` / system prompt / טעינת OS). זה מה שגורם ל-Claude לזהות תחביר `/command`.
ב-Claude Code התשתית נטענת אוטומטית: `CLAUDE.md` בתחילת session, skills לפי טריגר, ו-`os-auditor` כ-sub-agent.
