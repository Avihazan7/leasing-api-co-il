# CLAUDE.md — OS Entry Point

נקודת הכניסה הראשית של ה-Claude Operating System עבור הריפו.

## Active Modules
- `OPERATING_SYSTEM.md` v1.0.0 — Kernel: עקרונות יסוד, ארכיטקטורת שכבות, רישום מודולים, Boot Block והיררכיית הכרעה.
- `MEMORY.md` v1.0.0 — שכבת זיכרון: schema, כרטיס זהות, Active Focus/Projects, העדפות ופרוטוקול קריאה/כתיבה.
- `COWORK_SETUP.md` v1.0.0 — מדריך אונבורדינג ל-Cowork: 7 שלבי הגדרה, Global Instructions, מפת קבצי הקשר ואינטגרציה עם ה-OS.
- `COMMAND_API.md` v1.0.0 — 89 slash commands, composition operators, drop-in system prompt loaded.
- `AI_SKILL_MAP.md` v1.0.0 — מפת מיומנויות AI: 4 שלבים (Tools → Workflows → Agentic → Architect), יישומים, ומיקום ULease על המפה.
- `INVESTOR_RELATIONS.md` v1.0.0 — IR: חברה, cap table, גיוס 150K, תחזית ומעקב משקיעים.
- `CASES/ULEASE.md` v1.0.0 — תיק ULease 🎯 Leasing.co.il: מודל Marketplace תלת-צדדי + תחזית פיננסית (יוני 26 → דצמ' 27).
- `CASES/ULEASE_SPEC.md` v1.0.0 — איפיון מוצר ומערכת מקצה-לקצה: שחקנים, ארכיטקטורה, Multi-agent (Ultra·Master·Max), מודל נתונים, אינטגרציות ו-roadmap.
- `CASES/ULEASE_DECK.md` v1.1.0 — מצגת פיץ' (13 שקפים): Marp + HTML אינטראקטיבי (הקשה/החלקה/חיצים), נוצר ע"י `CASES/ULEASE_DECK.py`.
- `CASES/ULEASE_METHODOLOGY.md` v1.1.0 — מתודולוגיה: Big Five (OCEAN) להתאמת קונה-רכב, העשרה אינסטרומנטלית, תורת המשחקים, ומו"מ מבוסס-אינטרסים.

## Module Load Order
1. `OPERATING_SYSTEM.md`
2. `MEMORY.md`
3. `COWORK_SETUP.md`          ← חיבור התיקייה וטעינת ההקשר (אונבורדינג)
4. `COMMAND_API.md`           ← לפני הקטגוריות העסקיות
5. `INVESTOR_RELATIONS.md`    ← שכבת עסק: משקיעים וגיוס
6. `CASES/*.md`               ← תיקים פעילים (ULease 🎯)

## Activation
כדי להפעיל את ה-Command API, טען את בלוק ה-System Prompt מסעיף 7 ב-[`COMMAND_API.md`](./COMMAND_API.md)
אל ההקשר (`userPreferences` / system prompt / טעינת OS). זה מה שגורם ל-Claude לזהות תחביר `/command`.
