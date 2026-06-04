---
description: Verify CLAUDE.md manifest (Active Modules + Load Order) matches the .md files on disk
allowed-tools: Bash(ls:*), Glob, Read
---

מימוש לולאת הלקח מ-`MEMORY.md` (manifest drift). בדוק שה-manifest ב-`CLAUDE.md` כן:

1. רשום את כל קובצי ה-`*.md` ברמת השורש + `CASES/` + `BRANCHES/` + תיקיית `stage-a/`.
2. הצלב מול `CLAUDE.md › Active Modules` ו-`CLAUDE.md › Module Load Order`.
3. דווח שני סוגי דריפט:
   - **קובץ קיים בדיסק אך חסר מהמניפסט** (השמטה).
   - **מודול מוזכר במניפסט אך לא קיים בדיסק** (קישור מת) — אלא אם מסומן במפורש `roadmap`.

אם נמצא דריפט, הצע את העדכון המדויק (אל תערוך בלי אישור). אם הכול מסונכרן — אמור זאת.
