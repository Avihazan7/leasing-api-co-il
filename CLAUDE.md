# CLAUDE.md — OS Entry Point

נקודת הכניסה הראשית של ה-Claude Operating System עבור הריפו.

## Active Modules
- `COMMAND_API.md` v1.0.0 — 89 slash commands, composition operators, drop-in system prompt loaded.
- `COWORK_SETUP.md` v1.0.0 — מדריך אונבורדינג ל-Cowork: 7 שלבי הגדרה, Global Instructions, מפת קבצי הקשר ואינטגרציה עם ה-OS.

## Module Load Order
1. `OPERATING_SYSTEM.md`
2. `MEMORY.md`
3. `COWORK_SETUP.md`          ← חיבור התיקייה וטעינת ההקשר (אונבורדינג)
4. `COMMAND_API.md`           ← לפני הקטגוריות העסקיות
5. `INVESTOR_RELATIONS.md`
6. `CASES/*.md`

## Activation
כדי להפעיל את ה-Command API, טען את בלוק ה-System Prompt מסעיף 7 ב-[`COMMAND_API.md`](./COMMAND_API.md)
אל ההקשר (`userPreferences` / system prompt / טעינת OS). זה מה שגורם ל-Claude לזהות תחביר `/command`.
