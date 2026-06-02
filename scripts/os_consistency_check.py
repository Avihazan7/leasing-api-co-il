#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude OS — בדיקות עקביות מכניות (CI)
=========================================
המקבילה הדטרמיניסטית של סוכן os-auditor (.claude/agents/os-auditor.md):
רץ אוטומטית על כל PR (ראו .github/workflows/os-consistency.yml) ותופס
סטיות עקביות לפני merge — בלי לחכות לביקורת ידנית.

בדיקות:
  1. גרסה תלת-כיוונית: header ↔ שורת End ↔ ציטוט CLAUDE.md ↔ ציטוט README.md
  2. ספירת החלטות: שורות D-XXX ב-DECISION_LOG ↔ הספירה המוצהרת ב-CLAUDE.md וב-README.md
  3. No Dangling Modules: כל קובץ שמצוטט עם גרסה — קיים בפועל
  4. No Orphan Modules: כל מודול עם Version header — מצוטט ב-CLAUDE.md וב-README.md

הרצה מקומית:   python3 scripts/os_consistency_check.py
חלוקת עבודה:   הסקריפט = בדיקות מכניות · os-auditor (סוכן) = בדיקות סמנטיות עמוקות
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRY_POINTS = {"CLAUDE.md", "README.md"}  # נקודות כניסה — ללא גרסה משלהן

errors = []
checks = 0


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def header_version(path: pathlib.Path):
    """גרסה מ-header סטנדרטי (**Version:**) או מ-HTML comment (קבצי Marp)."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^\*\*Version:\*\*\s*(\d+\.\d+\.\d+)", text, re.M)
    if m:
        return m.group(1)
    m = re.search(r"<!--[^>]*?Version:\s*(\d+\.\d+\.\d+)[^>]*?-->", text, re.S)
    return m.group(1) if m else None


def end_line_version(path: pathlib.Path):
    """גרסה משורת '— End of FILE vX.Y.Z —' בסוף מודול (אם קיימת)."""
    m = re.search(r"End of\s+\S+\s+v(\d+\.\d+\.\d+)", path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


# ---------- איסוף: כל המודולים עם גרסה ----------
modules = {}
for pattern in ("*.md", "CASES/*.md"):
    for path in sorted(ROOT.glob(pattern)):
        rel = path.relative_to(ROOT).as_posix()
        if rel in ENTRY_POINTS:
            continue
        v = header_version(path)
        if v:
            modules[rel] = v

# ---------- איסוף: ציטוטי גרסה בנקודות הכניסה ----------
claude_md = read("CLAUDE.md")
readme_md = read("README.md")

# CLAUDE.md:   `FILE.md` v1.2.3
claude_cites = dict(re.findall(r"`([^`]+\.(?:md|html))`\s+v(\d+\.\d+\.\d+)", claude_md))
# README.md:   [`FILE.md`](./FILE.md) v1.2.3
readme_cites = dict(re.findall(r"\[`([^`]+\.(?:md|html))`\]\([^)]+\)\s+v(\d+\.\d+\.\d+)", readme_md))

# ---------- בדיקה 1: עקביות גרסאות תלת-כיוונית ----------
for rel, v_header in sorted(modules.items()):
    checks += 1
    path = ROOT / rel
    v_end = end_line_version(path)
    if v_end and v_end != v_header:
        errors.append(f"{rel}: גרסת header ({v_header}) ≠ גרסת שורת End ({v_end})")
    if rel in claude_cites and claude_cites[rel] != v_header:
        errors.append(f"{rel}: גרסת header ({v_header}) ≠ ציטוט CLAUDE.md (v{claude_cites[rel]})")
    if rel in readme_cites and readme_cites[rel] != v_header:
        errors.append(f"{rel}: גרסת header ({v_header}) ≠ ציטוט README.md (v{readme_cites[rel]})")

# ---------- בדיקה 2: ספירת החלטות ----------
checks += 1
decision_rows = len(re.findall(r"^\| D-\d{3} \|", read("DECISION_LOG.md"), re.M))
m = re.search(r"(\d+)\s+החלטות", claude_md)
if m and int(m.group(1)) != decision_rows:
    errors.append(f"CLAUDE.md מצהיר {m.group(1)} החלטות; ב-DECISION_LOG.md יש {decision_rows}")
m = re.search(r"(\d+)\s+founding", readme_md)
if m and int(m.group(1)) != decision_rows:
    errors.append(f"README.md מצהיר {m.group(1)} החלטות; ב-DECISION_LOG.md יש {decision_rows}")

# ---------- בדיקה 3: No Dangling Modules ----------
for cited in sorted(set(claude_cites) | set(readme_cites)):
    checks += 1
    if not (ROOT / cited).exists():
        errors.append(f"הפניה תלויה (dangling): {cited} מצוטט עם גרסה אך הקובץ לא קיים")

# ---------- בדיקה 4: No Orphan Modules ----------
for rel in sorted(modules):
    checks += 1
    if rel not in claude_cites:
        errors.append(f"מודול יתום (orphan): {rel} נושא Version header אך אינו מצוטט ב-CLAUDE.md")
    if rel not in readme_cites:
        errors.append(f"מודול יתום (orphan): {rel} נושא Version header אך אינו מצוטט ב-README.md")

# ---------- דוח ----------
print(f"Claude OS consistency check · {len(modules)} מודולים · {checks} בדיקות")
print("-" * 60)
if errors:
    print(f"❌ {len(errors)} ממצאים:")
    for e in errors:
        print(f"  • {e}")
    sys.exit(1)
print("✅ הכל עקבי — גרסאות, ספירות והפניות תואמות בכל המקומות.")
