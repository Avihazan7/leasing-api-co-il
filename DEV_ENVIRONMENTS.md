# DEV_ENVIRONMENTS.md — סביבות פיתוח של Claude, מקצה לקצה

**Module:** `DEV_ENVIRONMENTS.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Production-ready. Developer-facing companion to `WINDOWS_DEPLOYMENT.md`.
**Integrates with:** `CLAUDE.md`, `COMMAND_API.md`, `MEMORY.md`, `WINDOWS_DEPLOYMENT.md`
**Target:** צוות הפיתוח של Leasing.co.il / ULease — מ-Junior עד Staff.

---

## 0. תוכן עניינים

1. [סקירה ועקרון מנחה](#1-סקירה-ועקרון-מנחה)
2. [Decision Matrix — איזו סביבה לאיזה Developer](#2-decision-matrix)
3. [Prerequisites — דרישות מקדימות לכולן](#3-prerequisites)
4. [Track A · Claude Desktop](#4-track-a--claude-desktop)
5. [Track B · VS Code + Claude Extension](#5-track-b--vs-code--claude-extension)
6. [Track C · JetBrains + Claude Plugin](#6-track-c--jetbrains--claude-plugin)
7. [Track D · Cursor](#7-track-d--cursor)
8. [Track E · Windsurf](#8-track-e--windsurf)
9. [Track F · Claude Code (CLI)](#9-track-f--claude-code-cli)
10. [Layer X · MCP — הקישוריות לכלים](#10-layer-x--mcp)
11. [Layer Y · Computer Use — האוטונומיה](#11-layer-y--computer-use)
12. [Integration — חיבור ל-COMMAND_API](#12-integration--חיבור-ל-command_api)
13. [Secrets & Security](#13-secrets--security)
14. [Team Rollout — מ-1 ל-N מפתחים](#14-team-rollout)
15. [Verification & Troubleshooting](#15-verification--troubleshooting)
16. [Checklist סופי](#16-checklist-סופי)

---

## 1. סקירה ועקרון מנחה

האינפוגרפיקה אומרת את האמת: **לא צריך את הכל. בוחרים לפי רמת הנוחות וסגנון העבודה.**

המסמך הזה הוא לא "בחרו אחד" — הוא "בנו stack מודולרי לפי תפקיד". מפתח backend, מפתח frontend, DevOps ו-Data Engineer לא יעבדו אותו דבר. כל track עומד בפני עצמו, אבל כולם מדברים לאותו `COMMAND_API.md`.

**עיקרון אחד שעובר רוחבית:**
> Claude הוא pair-programmer, לא code-monkey. המפתח מחליט מה נכון, Claude מקצר את הזמן שלוקח להגיע לשם. Code review אנושי לפני merge — תמיד.

| Track | קהל יעד | Time-to-value | רמת אוטונומיה |
|-------|----------|---------------|------------------|
| A · Claude Desktop | מפתח חדש / non-coder | 2 דקות | נמוכה (chat) |
| B · VS Code Ext | רוב הצוות | 10 דקות | בינונית (inline) |
| C · JetBrains Plugin | Backend / Kotlin / Java | 10 דקות | בינונית (inline) |
| D · Cursor | מי שרוצה AI-native IDE | 15 דקות | גבוהה |
| E · Windsurf | מי שרוצה agent-flow מובנה | 15 דקות | גבוהה |
| F · Claude Code CLI | Power-users, DevOps, CI/CD | 5 דקות | מקסימלית |

---

## 2. Decision Matrix

### 2.1 לפי תפקיד ב-ULease

| תפקיד | Primary | Secondary | Why |
|--------|---------|-----------|-----|
| Backend (Node/Python) | **VS Code Ext** | Claude Code CLI | inline edits + CLI ל-refactor רוחביים |
| Backend Java/Kotlin | **JetBrains Plugin** | Claude Code CLI | אי-אפשר לוותר על ה-IDE; CLI ל-batch |
| Frontend (React/Next) | **Cursor** | VS Code Ext | יותר מהירות, פחות הקשר אבוד |
| Mobile (iOS/Android) | **JetBrains/Xcode + Claude Code** | Desktop | CLI עוטף את ה-toolchain |
| DevOps / SRE | **Claude Code CLI** | Desktop | scripts, IaC, runbooks — terminal-first |
| Data Eng / Analytics | **VS Code Ext** | Desktop | notebooks + SQL |
| Tech Lead / Architect | **Desktop + Claude Code** | — | תכנון ב-Desktop, ביצוע ב-CLI |
| QA / Test Eng | **Claude Code CLI** | VS Code Ext | יצירת test suites batch |
| Product / PM (non-coder) | **Desktop** | — | drafting, אפיון, סיכומים |

### 2.2 לפי משימה

| משימה | הכלי הנכון |
|--------|-------------|
| "תסביר לי את הקוד הזה" | VS Code/JetBrains — Selection → Explain |
| "צור endpoint חדש לפי תבנית" | Cursor / Windsurf (יותר אוטונומיה) |
| "תרץ migration ותתקן את ה-tests" | Claude Code CLI |
| "תעבור על כל הריפו ותעדכן API version" | Claude Code CLI |
| "תכין לי מסמך אפיון" | Desktop |
| "תקרא לי PR ותגיד אם יש בעיות" | Claude Code CLI (`/code-review`) |
| "תבדוק קובץ שאני לא יודע מה הוא עושה" | Desktop |

### 2.3 כלל אצבע

- צריך **רק חלון צ'אט נפרד** → Desktop.
- צריך **לערוך קוד שאני רואה** → VS Code / JetBrains.
- צריך **לבנות פיצ'ר מאפס במהירות** → Cursor / Windsurf.
- צריך **לעשות 50 דברים על הריפו בלי GUI** → Claude Code.

---

## 3. Prerequisites

### 3.1 חשבון

- חשבון Anthropic ב-`leasing.co.il` (Team / Enterprise plan).
- 2FA פעיל (חובה — תחת רגולציה).
- API key נפרד למשתמש (לא משותף!) — נוצר ב-`console.anthropic.com`.

### 3.2 מערכת הפעלה

| OS | תמיכה ב-Tracks |
|----|----------------|
| macOS 13+ | A, B, C, D, E, F (כולם) |
| Windows 11 | A, B, C, D, E, F |
| Windows 10 22H2 | A, B, C, D, E, F (עם WSL2 ל-F) |
| Ubuntu 22.04+ | B, C, D, E, F (אין Desktop רשמי על Linux בזמן הכתיבה) |

### 3.3 כלים בסיסיים

```bash
# כל מפתח חייב את אלה לפני שמתחילים
git --version           # >= 2.40
node --version          # >= 20 LTS (אם עובדים JS/TS)
python --version        # >= 3.11 (אם עובדים Python)
docker --version        # >= 24
gh --version            # GitHub CLI (אופציונלי אבל מומלץ)
```

### 3.4 גישה לריפו

```bash
gh auth login            # התחבר ל-GitHub
git clone git@github.com:Avihazan7/leasing-api-co-il.git
cd leasing-api-co-il
```

---

## 4. Track A · Claude Desktop

### 4.1 למי

מפתחים חדשים, PMs, אנשי תוכן, או כל מי שצריך חלון צ'אט נפרד שיכול לקרוא קבצים מקומיים.

### 4.2 התקנה

1. הורד מ-`claude.ai/download`.
2. macOS: גרור ל-Applications. Windows: הרץ את ה-`.exe`.
3. Sign in עם חשבון `leasing.co.il`.

### 4.3 הגדרות מומלצות

`Settings → Appearance`:
- Theme: System.
- Font size: 14-16.

`Settings → Features`:
- **Projects**: On (מאפשר knowledge base לפרויקט).
- **Artifacts**: On.
- **Analysis tool**: On (להרצת JS בצד הלקוח).

`Settings → Developer`:
- **MCP servers**: כאן מחברים את שרתי ה-MCP (ראה פרק 10).

### 4.4 Use cases ב-ULease

| תרחיש | flow |
|--------|------|
| הבנת קוד legacy | גרור קובץ לחלון → "תסביר לי מה זה עושה ולמה זה כתוב ככה" |
| Brainstorm ארכיטקטורה | פתח Project "ULease Architecture" → דבר חופשי |
| ניסוח PR description | הדבק `git diff` → "ניסוח PR לפי הפורמט שלנו" |
| דיבאג שגיאה | הדבק stack trace → "מה השורש?" |

### 4.5 Projects — knowledge base לפרויקט

יצירת Project אחד מרכזי:
- **Name:** `ULease — Leasing.co.il`
- **Custom instructions:** "אתה pair-programmer של צוות ULease. הריפו ב-Node.js + PostgreSQL. ענה בקצרה, code-first, בעברית כשנשאלים בעברית."
- **Knowledge:** העלה את `CLAUDE.md`, `COMMAND_API.md`, `WINDOWS_DEPLOYMENT.md`, `DEV_ENVIRONMENTS.md` (הקובץ הזה), ו-`README.md`.

---

## 5. Track B · VS Code + Claude Extension

### 5.1 למי

הברירת מחדל לרוב הצוות. אם אין לך העדפה חזקה אחרת — זה הטראק.

### 5.2 התקנה

```
VS Code → Extensions (Ctrl+Shift+X)
חפש: "Claude"
מפרסם: Anthropic
לחץ Install
```

לאחר ההתקנה: `Cmd/Ctrl + Shift + P` → `Claude: Sign in`.

### 5.3 הגדרות `settings.json` מומלצות

```json
{
  "claude.defaultModel": "claude-opus-4-7",
  "claude.autoSave": true,
  "claude.inlineEdit.enabled": true,
  "claude.contextWindow": "workspace",
  "claude.excludePatterns": [
    "**/node_modules/**",
    "**/.git/**",
    "**/dist/**",
    "**/.env*"
  ],
  "claude.telemetry": "minimal"
}
```

### 5.4 קיצורי מקלדת

| פעולה | macOS | Windows / Linux |
|--------|-------|------------------|
| פתיחת Claude pane | `⌘ ⇧ L` | `Ctrl Shift L` |
| Inline edit על selection | `⌘ K` | `Ctrl K` |
| Explain selection | `⌘ ⇧ E` | `Ctrl Shift E` |
| Send to Claude | `⌘ Enter` | `Ctrl Enter` |

### 5.5 Workflow יומיומי

```
1. בחר טווח קוד (פונקציה, בלוק)
2. ⌘K → "תכתוב tests ל-vitest"
3. Claude מציג diff → Accept / Reject / Iterate
4. בדוק שה-tests עוברים
5. Commit
```

### 5.6 Custom commands ל-Workspace

צור `.vscode/claude.commands.json`:

```json
{
  "commands": [
    {
      "name": "ulease-endpoint",
      "description": "צור endpoint חדש לפי תבנית ULease",
      "prompt": "צור endpoint Express בנתיב /api/v1/<resource> עם validation (zod), שכבת service נפרדת, ו-tests ל-vitest. עקוב אחר הסגנון של src/routes/deals.ts."
    },
    {
      "name": "ulease-migration",
      "description": "Migration לפי תבנית Knex",
      "prompt": "צור migration לפי תבנית של migrations/ הקיים. up/down שניהם reversible. אל תיגע ב-FKs קיימים."
    }
  ]
}
```

---

## 6. Track C · JetBrains + Claude Plugin

### 6.1 למי

צוות backend על Kotlin/Java/Scala (IntelliJ IDEA), Python (PyCharm), או mobile (Android Studio).

### 6.2 התקנה

```
File → Settings → Plugins → Marketplace
חפש: "Claude"
מפרסם: Anthropic
Install → Restart IDE
```

לאחר restart: `Tools → Claude → Sign in`.

### 6.3 הגדרות מומלצות

`Settings → Tools → Claude`:
- Model: `claude-opus-4-7`
- Auto-include open file: On
- Auto-include project structure: On
- Max context tokens: 200k (default)

`Settings → Keymap` — חפש "Claude" ובנה לעצמך shortcut לפעולות הנפוצות.

### 6.4 שילוב עם הכלים של JetBrains

| כלי JetBrains | מה Claude מוסיף |
|---------------|------------------|
| Database tool | "תכתוב לי את ה-query הזה כ-JPA Specification" |
| Run/Debug | "תסביר למה ה-test נכשל" — Claude קורא את ה-stacktrace |
| Refactoring | Inline edit על מתודה שלמה לפני שאתה רץ Rename |
| Git integration | "סכם את ה-diff של הענף הזה" |

### 6.5 Use case — Spring Boot ב-ULease

```
1. פתח DealController.java
2. Selection על המתודה createDeal()
3. ⌥ Enter → Claude → "תוסיף rate limiting + audit log"
4. Apply → Commit
```

---

## 7. Track D · Cursor

### 7.1 למי

מי שמוכן להחליף IDE לטובת חוויית AI-native אגרסיבית יותר. בעיקר frontend / full-stack.

### 7.2 התקנה

1. הורד מ-`cursor.com`.
2. בעת הפעלה ראשונה — אפשר לייבא הגדרות מ-VS Code (extensions, themes, keybindings).
3. `Settings → Models` → הוסף Anthropic API key (או השתמש ב-Cursor's own routing).

### 7.3 הפיצ'רים שצריך להכיר

| פיצ'ר | קיצור | מתי להשתמש |
|---------|--------|-------------|
| Chat | `⌘ L` | שאלות, סיכומים |
| Inline edit | `⌘ K` | שינוי ממוקד בקובץ |
| Composer / Agent | `⌘ I` | פיצ'ר שלם על פני מספר קבצים |
| `@codebase` | בתוך chat | לתת context של הריפו כולו |
| `@docs` | בתוך chat | לטעון תיעוד חיצוני (Stripe, Twilio...) |

### 7.4 `.cursorrules` לפרויקט ULease

צור בשורש הריפו:

```
# Cursor rules — ULease / Leasing.co.il

## Stack
- Backend: Node.js 20, Express, TypeScript, Knex + PostgreSQL
- Frontend: Next.js 15, React 19, Tailwind, shadcn/ui
- Tests: Vitest (unit), Playwright (e2e)

## Conventions
- כל endpoint עובר דרך validation עם zod
- ENV vars: גישה רק דרך src/config/env.ts (אל תיגע ב-process.env ישירות)
- שגיאות: זרוק AppError, אל תחזיר 500 גנרי
- Migrations: rever­sible תמיד (up + down)

## Don't
- אל תוסיף תלויות חדשות בלי לבקש
- אל תיגע ב-secrets / .env*
- אל תייצר Mock data בייצור — רק ב-tests
- אל תכתוב comments שמסבירים WHAT — רק WHY

## Domain glossary
- Deal = עסקת ליסינג
- Fleet = צי רכבים
- IR = Investor Relations
```

### 7.5 Composer flow — פיצ'ר חדש

```
⌘ I → "הוסף endpoint POST /api/v1/deals/:id/extend שמאריך עסקה ב-N חודשים.
       - Validation לתאריך סיום חדש
       - Update ב-deals + יצירת רשומה ב-deal_history
       - Tests
       - Update OpenAPI spec"

Composer בונה plan → אתה מאשר → מבצע על כל הקבצים → review diff → Accept.
```

---

## 8. Track E · Windsurf

### 8.1 למי

מי שאהב את הרעיון של Cursor אבל רוצה agent-flow יותר מובנה ופחות chat-driven.

### 8.2 התקנה

1. הורד מ-`windsurf.com` (לשעבר Codeium).
2. ייבא הגדרות מ-VS Code אם רוצים.
3. Sign in → בחר workspace.

### 8.3 ההבדל המרכזי מ-Cursor

Windsurf מבוסס יותר על **Cascade** — סוכן שמתכנן ומבצע ברצף. מתאים יותר ל-:
- בנייה של פיצ'ר שלם מ-spec.
- Refactor רוחבי על פני 10+ קבצים.
- מי שמעדיף "תגיד לי מה לעשות" על פני "תתקן את זה".

### 8.4 הגדרות ל-ULease

צור `.windsurfrules` (תוכן דומה ל-`.cursorrules` למעלה — אותה domain knowledge).

### 8.5 מתי לבחור Windsurf על פני Cursor

- אתה רוצה approval gate בין כל שלב.
- העבודה שלך יותר greenfield ופחות bugfix-ים נקודתיים.
- אתה לבד על feature ולא צריך לעקוב צמוד.

---

## 9. Track F · Claude Code (CLI)

### 9.1 למי

Power-users, DevOps, anyone שמרגיש בנוח עם terminal. **הטראק החזק ביותר** — גם הכי בלתי-סלחני אם לא יודעים מה עושים.

### 9.2 התקנה

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | sh

# Windows (PowerShell)
iwr -useb https://claude.ai/install.ps1 | iex

# בדיקה
claude --version
```

Sign in:
```bash
claude login
# פותח דפדפן, מאשר, חוזר ל-terminal
```

### 9.3 שני מצבי הפעלה

| Mode | פקודה | מתי |
|------|--------|------|
| Interactive | `claude` (בתוך תיקיית הריפו) | פיתוח רגיל, יום-יום |
| One-shot | `claude -p "<prompt>"` | סקריפטים, CI, automation |

### 9.4 הגדרת הפרויקט

צור `.claude/settings.json` בריפו (כבר קיים `CLAUDE.md` — Claude קורא אותו אוטומטית):

```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(git:*)",
      "Bash(gh:*)",
      "Read(./**)",
      "Edit(./src/**)",
      "Edit(./tests/**)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Read(./.env*)",
      "Edit(./.env*)"
    ]
  },
  "model": "claude-opus-4-7"
}
```

### 9.5 Skills ו-Slash commands ב-CLI

צור `.claude/skills/` בריפו לסקילים ספציפיים לפרויקט:

```
.claude/
├── settings.json
└── skills/
    ├── verify-migration.md      ← /verify-migration
    ├── deploy-staging.md        ← /deploy-staging
    ├── bump-api-version.md      ← /bump-api-version
    └── audit-fleet-data.md      ← /audit-fleet-data
```

דוגמה ל-`verify-migration.md`:

```markdown
---
name: verify-migration
description: בדיקה שה-migration הכי חדש reversible ולא שובר tests
---

# Verify Migration

1. הרץ `npm run migrate:latest` על DB מקומי
2. הרץ `npm test`
3. אם עבר — הרץ `npm run migrate:rollback`
4. ודא שה-rollback הצליח (הסכמה זהה ל-pre-migrate)
5. דווח: ✅/❌ לכל שלב
```

### 9.6 use cases משמעותיים

```bash
# refactor רוחבי
claude -p "החלף את כל השימושים ב-axios ל-fetch עם wrapper שלנו ב-src/lib/http.ts"

# code review לפני push
claude -p "/code-review"

# CI integration — failing test triage
claude -p "תקרא את output הזה ותגיד אם זו רגרסיה אמיתית או flaky test:
$(cat ci-output.log)"

# יצירת PR מ-CLI
claude -p "סכם את ה-diff מול main, צור PR title + body, ופתח PR ב-GitHub"
```

### 9.7 Claude Code on the Web

מעבר ל-CLI המקומי, אפשר להריץ סשנים בענן דרך `claude.ai/code` (זה בדיוק הסביבה שבה ה-OS הזה רץ עכשיו). הענן מתאים ל-:
- משימות ארוכות שלא תלויות בלפטופ פתוח.
- עבודה מהטלפון/iPad.
- אינטגרציה עם PR webhooks (`subscribe_pr_activity`).

תיעוד מלא: `code.claude.com/docs/en/claude-code-on-the-web`.

---

## 10. Layer X · MCP — הקישוריות לכלים

### 10.1 מה זה

**MCP (Model Context Protocol)** הוא הפרוטוקול שמחבר את Claude לכלים חיצוניים — DB, GitHub, Slack, file systems, custom APIs. זו לא "סביבת עבודה" — זו השכבה שמאפשרת לכל אחת מ-Tracks A-F לעשות יותר.

### 10.2 שרתים שכדאי לחבר לארגון Leasing

| MCP server | מה זה נותן | track יעד |
|-------------|-------------|-----------|
| `mcp-postgres` | שאילתות ישירות ל-DB | Backend, Data |
| `mcp-github` | קריאת PRs, commits, issues | כולם |
| `mcp-filesystem` | גישה לקבצים מחוץ לריפו | Desktop |
| `mcp-slack` | שליחת notifications | DevOps |
| `mcp-google-drive` | קישור לתבניות של IR | PM, IR team |
| `mcp-sentry` | error tracking context | Backend, SRE |
| `mcp-stripe` | בדיקת חיובים | Backend, Finance |

### 10.3 הגדרה ל-Claude Desktop

`Settings → Developer → Edit Config` → `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ulease-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres",
               "postgresql://readonly:***@localhost:5432/ulease"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..." }
    }
  }
}
```

⚠️ **כלל ברזל:** ל-MCP על DB ייצור — read-only credentials בלבד. תמיד.

### 10.4 הגדרה ל-Claude Code

ב-`.claude/settings.json`:

```json
{
  "mcpServers": {
    "ulease-db": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-postgres", "$DATABASE_URL_READONLY"] }
  }
}
```

או דרך CLI:
```bash
claude mcp add ulease-db -- npx -y @modelcontextprotocol/server-postgres "$DATABASE_URL_READONLY"
```

### 10.5 בניית MCP server ייעודי ל-ULease

> 🎯 **רקע אסטרטגי:** ה-MCP הפנימי הוא לא feature — זה ה-**moat**. לפי הלקח
> מ-[`CASES/ROX_KEY.md § 5.2`](./CASES/ROX_KEY.md) ("נתונים כנכס אסטרטגי"),
> חשיפת נתוני הצי / עסקאות / תמחור כ-data assets לסטאק שלנו היא מה שמייצר
> דיפרנציאציה אמיתית. **בוצע upgrade ב-`LAUNCH.md § 5` מ-"future" ל-Q1 milestone.**

לכלים פנימיים (e.g., "סטטוס צי בזמן אמת") בנו MCP server משלכם:

```
internal-tools/
└── mcp-ulease/
    ├── package.json
    ├── src/
    │   ├── server.ts          ← entry point
    │   ├── tools/
    │   │   ├── fleet-status.ts
    │   │   ├── deal-lookup.ts
    │   │   └── pricing-quote.ts
    │   └── auth.ts
    └── README.md
```

תיעוד SDK: `docs.anthropic.com` → MCP.

---

## 11. Layer Y · Computer Use — האוטונומיה

### 11.1 מה זה

**Computer Use** הוא היכולת של Claude להפעיל מחשב כמו אדם — להזיז עכבר, להקליק, להקליד, לקרוא screen. גם זו לא סביבת עבודה — זו יכולת שאפשר להפעיל מתוך כל track.

### 11.2 מתי כן ומתי לא ב-Leasing

| תרחיש | להשתמש? |
|--------|----------|
| בדיקת UI ידנית של פיצ'ר חדש | ✅ |
| הזנה חוזרת של 200 רשומות למערכת legacy בלי API | ✅ (בסביבת test) |
| גריפת מתחרים | ⚠️ ToS — להיזהר |
| אוטומציה על מערכת CRM ייצור | ❌ — תכתבו API integration |
| משימות עם PII של לקוחות | ❌ — לא בלי DPO approval |

### 11.3 הפעלה דרך API

Computer Use הוא beta capability ב-Anthropic API. הוא לא חלק מה-Desktop / IDE plugins סטנדרטית — מפעילים אותו דרך קוד:

```python
# pseudo — לבדיקה בלבד
import anthropic
client = anthropic.Anthropic()
client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    tools=[{"type": "computer_20250124", "name": "computer", ...}],
    messages=[{"role": "user", "content": "open Chrome, login to staging, run smoke test"}]
)
```

זה עניין של QA / R&D — לא day-to-day של רוב המפתחים.

---

## 12. Integration — חיבור ל-COMMAND_API

זה החלק שמייחד את הסטאק שלנו: **כל track מדבר לאותו `COMMAND_API.md`**.

### 12.1 איך זה עובד

`COMMAND_API.md` הוא drop-in system prompt. אפשר לטעון אותו:

| Track | איך |
|-------|------|
| Desktop | Project → Custom Instructions → הדבק את סעיף 7 מ-COMMAND_API.md |
| VS Code Ext | `.vscode/claude.systemPrompt.md` → קישור לקובץ |
| JetBrains | Settings → Claude → System Prompt → טעינה מקובץ |
| Cursor | `.cursorrules` → אזכור + טעינה |
| Windsurf | `.windsurfrules` → אזכור + טעינה |
| Claude Code | אוטומטי — `CLAUDE.md` כבר טוען אותו |

### 12.2 דוגמה — אותה פקודה, ארבעה כלים

```
/tldr
```

| מ-Track | התוצאה |
|---------|---------|
| Desktop | tldr של השיחה |
| VS Code | tldr של הקובץ הפתוח |
| Cursor | tldr של ה-selection |
| Claude Code | tldr של ה-diff מול main |

ההתנהגות זהה (≤3 שורות, bullets, no preamble) — רק ה-input משתנה לפי הקונטקסט.

### 12.3 הוספת פקודות ייעודיות לפיתוח

הרחבת `COMMAND_API.md` בפקודות dev-specific:

```
/pr-description      → סיכום PR מ-git diff
/test-from-spec      → tests מ-OpenAPI spec
/migration-check     → ולידציה של migration
/api-endpoint        → boilerplate של endpoint לפי תבנית
/db-explain          → הסבר על schema/query
/post-mortem         → תבנית post-mortem מ-incident log
```

(כל אחת תופיע בקטלוג של `COMMAND_API.md` בעדכון הבא.)

---

## 13. Secrets & Security

### 13.1 שלושה כללי ברזל

1. **API keys אישיים, לא משותפים.** כל מפתח יוצר את שלו ב-`console.anthropic.com`.
2. **`.env*` ב-`.gitignore` ו-ב-`deny` של Claude Code permissions.**
3. **DB credentials ל-MCP — read-only בייצור. תמיד.**

### 13.2 אחסון API key

| איפה לאחסן | איפה לא |
|------------|---------|
| macOS Keychain | בקוד |
| Windows Credential Manager | ב-`.zshrc` בלי הצפנה |
| 1Password / Bitwarden | ב-Slack DM |
| Secrets manager בענן (לסביבות team) | ב-Notion |

### 13.3 גילוי דליפת מפתח

אם API key דלף:
```bash
# 1. revoke מיידי
# console.anthropic.com → Keys → Revoke

# 2. צור חדש
# console.anthropic.com → Create key

# 3. סרוק היסטוריה
git log -p | grep -i "sk-ant"

# 4. אם נמצא בהיסטוריה — BFG repo-cleaner
# או, אם זה נדיר, מחיקת ההיסטוריה הספציפית
```

### 13.4 מה Claude לא צריך לראות אצלנו

```
# .claudeignore (תקני בריפו)
.env
.env.*
secrets/
**/credentials.json
**/service-account*.json
**/*.pem
**/*.key
**/private/
```

`Claude Code` ו-Extensions מכבדים `.claudeignore` (ו-`.gitignore` כברירת מחדל).

---

## 14. Team Rollout — מ-1 ל-N מפתחים

### 14.1 שלבים

| שלב | משך | מי |
|-----|-----|-----|
| Pilot — 2-3 מפתחים | שבועיים | Tech Lead + 2 mid-level |
| Wave 1 — backend | שבוע | כל backend |
| Wave 2 — frontend | שבוע | כל frontend |
| Wave 3 — DevOps + Data | שבוע | תשתית |
| All hands | חצי-יום | ישיבת הכלל-צוותית — חוקים משותפים |

### 14.2 Onboarding script למפתח חדש

```bash
#!/usr/bin/env bash
# .bin/setup-claude.sh

set -e

echo "==> Claude dev environment setup"

# 1. CLI
if ! command -v claude &> /dev/null; then
  curl -fsSL https://claude.ai/install.sh | sh
fi

# 2. login
claude login

# 3. clone
git clone git@github.com:Avihazan7/leasing-api-co-il.git ~/code/ulease
cd ~/code/ulease

# 4. install deps
npm ci

# 5. validate Claude reads CLAUDE.md
claude -p "/health" --no-interactive

echo "==> מוכן. רוץ 'claude' מתוך ~/code/ulease להתחלת סשן."
```

### 14.3 חוקי צוות שצריך לסכם בכתב

1. **PR description נכתב על ידי מפתח, לא העתק-הדבק מ-Claude בלי עריכה.**
2. **Code review אנושי תמיד — Claude יכול לעזור לבודק, לא להחליף.**
3. **שינויים ב-`COMMAND_API.md` עוברים PR כמו כל קוד.**
4. **שימוש ב-Claude Code על main — אסור. רק על branches.**
5. **`/code-review ultra` לפני merge ל-`main`.**

### 14.4 KPIs לחודש שלוש

- זמן ממוצע מ-issue ל-PR פתוח: ירידה של 30%+.
- כיסוי tests: עלייה של 15%+.
- PRs שעוברים CI ב-first attempt: 80%+.
- מקרי "AI hallucinated code that broke prod": 0.

---

## 15. Verification & Troubleshooting

### 15.1 בדיקות per-track

```bash
# Track A — Desktop
# ידני: פתח, sign-in, "תכתוב hello world ב-TypeScript"

# Track B — VS Code Ext
code --list-extensions | grep -i claude
# צריך להחזיר את ה-extension

# Track C — JetBrains
# Tools → Claude → About — יציג גרסה

# Track D — Cursor / E — Windsurf
# הגדרות → About — יציג גרסה

# Track F — Claude Code
claude --version
claude -p "echo test" --no-interactive
```

### 15.2 בעיות נפוצות

| תופעה | סיבה סבירה | פתרון |
|--------|-------------|---------|
| "Authentication failed" | טוקן פג | `claude logout && claude login` |
| Extension לא טוען | VS Code לא מעודכן | עדכן ל-1.95+ |
| `MCP server not responding` | תהליך MCP נתקע | restart לאפליקציה |
| תוצאות "כללי מדי" | חסר context | טען `CLAUDE.md` ל-Project / טען `.cursorrules` |
| Cursor / Windsurf לא רואים את הריפו | indexing לא הסתיים | המתן 2-5 דקות אחרי פתיחה |
| Claude Code עובד איטי | context גדול מדי | `claude clear` או `/compact` |

### 15.3 בדיקה רוחבית — האם ה-OS שלנו נטען

הרץ באחת מהסביבות:

```
/health
```

הצפי: תשובה מובנית שמצביעה ש-`CLAUDE.md` ו-`COMMAND_API.md` בהקשר. אם לא — חזור לפרק 12.

---

## 16. Checklist סופי

### 16.1 לכל מפתח

```
□ חשבון Anthropic ב-leasing.co.il עם 2FA
□ API key אישי ב-Keychain / Credential Manager
□ Track ראשי הותקן (לפי טבלה 2.1)
□ Track משני הותקן (לפחות Claude Code CLI לכולם)
□ ריפו clone'd לוקלית
□ CLAUDE.md ו-COMMAND_API.md נטענים לפי Track
□ .claudeignore קיים בריפו
□ הפקודות /tldr, /focus, /code-review רצות מ-CLI ומ-IDE
□ ה-MCP servers הרלוונטיים מחוברים (לפחות GitHub + DB read-only)
```

### 16.2 לארגון

```
□ Anthropic Team / Enterprise plan פעיל
□ DPA חתום ובארכיון
□ Zero Data Retention מאומת
□ הגדרות secrets management מאוחדות לכל הצוות
□ Onboarding script (.bin/setup-claude.sh) קיים בריפו
□ חוקי צוות מתועדים (פרק 14.3)
□ KPIs מוגדרים ומדידים
□ ביקורת חודשית של PRs ב-Claude assistance ב-CI logs
```

### 16.3 חודש 6 — בגרות

```
□ 100% מהמפתחים על לפחות שני tracks
□ COMMAND_API.md מורחב ב-≥10 פקודות dev-specific
□ MCP server פנימי ל-ULease נכתב ובשימוש
□ Skills ייעודיים פרויקטליים (.claude/skills/) ≥ 8
□ מטריקות: ירידה של 40%+ בזמן פיתוח לפיצ'ר ממוצע
□ אפס אירועי security הקשורים ל-AI tooling
□ Knowledge transfer: כל מפתח בכיר מאמן ג'וניור על הסטאק
```

---

## נספח א' — מטריצת הסטאק המומלץ ל-ULease

| Role | Desktop | VS Code | JetBrains | Cursor | Windsurf | Claude Code |
|------|:-------:|:-------:|:---------:|:------:|:--------:|:-----------:|
| Tech Lead | ✅ | ✅ | — | — | — | ✅ |
| Backend (Node) | — | ✅ | — | — | — | ✅ |
| Backend (Java) | — | — | ✅ | — | — | ✅ |
| Frontend | — | ✅ | — | ✅ | — | ✅ |
| Mobile | ✅ | — | ✅ | — | — | ✅ |
| DevOps | — | ✅ | — | — | — | ✅ |
| Data | ✅ | ✅ | — | — | — | ✅ |
| QA | — | ✅ | — | — | — | ✅ |
| PM | ✅ | — | — | — | — | — |

✅ = מותקן · — = לא נדרש (אבל לא אסור)

---

## נספח ב' — תרשים האקוסיסטם

```
                    ┌─────────────────────────────┐
                    │      CLAUDE.md (OS)         │
                    │  + COMMAND_API.md (89 cmds) │
                    │  + MEMORY.md                │
                    └────────────┬────────────────┘
                                 │
       ┌───────────────┬─────────┼─────────┬────────────────┐
       │               │         │         │                │
   ┌───▼───┐     ┌─────▼───┐ ┌───▼───┐ ┌───▼────┐    ┌─────▼─────┐
   │Desktop│     │VS Code  │ │Cursor │ │Windsurf│    │Claude Code│
   │       │     │JetBrains│ │       │ │        │    │   (CLI)   │
   └───┬───┘     └─────┬───┘ └───┬───┘ └────┬───┘    └─────┬─────┘
       │               │         │          │              │
       └───────────────┴─────────┼──────────┴──────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
          ┌───▼────┐       ┌─────▼─────┐      ┌─────▼─────┐
          │  MCP   │       │ Computer  │      │  Custom   │
          │servers │       │   Use     │      │  Skills   │
          └───┬────┘       └───────────┘      └───────────┘
              │
   ┌──────────┼──────────┬──────────┬──────────┐
   │          │          │          │          │
 ┌─▼──┐  ┌────▼───┐  ┌───▼──┐  ┌────▼───┐  ┌───▼────┐
 │ DB │  │ GitHub │  │Slack │  │ Drive  │  │Internal│
 └────┘  └────────┘  └──────┘  └────────┘  └────────┘
```

---

## גרסאות

| גרסה | תאריך | שינוי |
|------|--------|-------|
| 1.0.0 | 2026-05-28 | Initial — 6 tracks + MCP + Computer Use + integration with COMMAND_API |

---

**Tie-back ל-OS:** המסמך הזה ו-`WINDOWS_DEPLOYMENT.md` הם שני הצדדים של אותו מטבע —
הראשון לעובדים העסקיים, השני לצוות הפיתוח. שניהם יוצאים מאותו `CLAUDE.md`,
מדברים לאותו `COMMAND_API.md`, ומחזיקים את ULease/Leasing.co.il על stack אחד מאוחד.
