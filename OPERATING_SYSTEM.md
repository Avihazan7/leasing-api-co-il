# OPERATING_SYSTEM.md — מסמך-העל

**Module:** `OPERATING_SYSTEM.md` · **Version:** 1.0.0
**Status:** מסמך-על. סוגר את ה-dangling ref הראשון ב-load order (ראה `AGENT_BLUEPRINT § 7`).
**Thesis:** *ה-OS הוא לא ערימת מסמכים — הוא חוזה הפעלה.*

---

## 0. מה זה ה-Claude Operating System

ה-OS הוא שכבת ה-orchestration שהופכת ריפו תיעוד לסביבת עבודה אופרטיבית ל-agents.
הוא עונה על שלוש שאלות לכל agent שנכנס:

1. **מה לטעון** (ובאיזה סדר) — `CLAUDE.md › Module Load Order`.
2. **איך להתנהג** — `CLAUDE.md › Working Rules` (דוקטרינת Karpathy, מקור `AGENT_BLUEPRINT § 10`).
3. **מה אני יכול לקרוא לו** — `COMMAND_API.md` (תחביר `/command`).

## 1. שכבות ה-OS

```
┌──────────────────────────────────────────────────────────┐
│ ENTRY      CLAUDE.md            ← load order + working rules │
├──────────────────────────────────────────────────────────┤
│ MEMORY     MEMORY.md            ← 4 tiers + לולאת לקחים       │
│ COMMANDS   COMMAND_API.md       ← 100 פקודות, /syntax        │
│ DOCTRINE   AGENT_BLUEPRINT.md   ← Docs OS ⇄ Agent Runtime    │
│ KNOWLEDGE  SYSTEM_DESIGN_PATTERNS · AI_ENGINEER_STACK ·      │
│            power-bi · N8N · BRANCH_KNOWLEDGE                  │
│ LAUNCH     LAUNCH.md            ← master switch, go-live      │
│ RUNTIME    stage-a/             ← manager · worker · memory  │
└──────────────────────────────────────────────────────────┘
```

## 2. חוזה הטעינה

agent תקין טוען לפי `CLAUDE.md › Module Load Order` ולא מדלג. דילוג על מודול = חוב
טכני שצריך לתעד ב-`MEMORY.md`, לא חור שקט. כל מודול נושא **גרסה** (`vX.Y.Z`) ו-`CLAUDE.md ›
Active Modules` הוא ה-manifest הסמכותי — אם קובץ קיים בדיסק אך לא במניפסט, זה באג סנכרון.

## 3. עקרון ה-System-First

ה-OS מאמץ את תזת `AGENT_BLUEPRINT`: *Design the SYSTEM first. The model is only one layer.*
המודל הוא שכבה אחת מתוך 8 (purpose · prompt · model · tools · memory · orchestration · UI · evals).
מסמך זה הוא ה-anchor שמצהיר שהשכבות האלה קיימות ומחוברות.

## 4. Roadmap

ראה `AGENT_BLUEPRINT § 7` למפת הדרכים המלאה (Stage-B/C, Evals harness, A2A). מסמך זה
ייהפך מ-anchor ל-spec מלא כשכל המודולים יתייצבו (תלות: כל המודולים).
