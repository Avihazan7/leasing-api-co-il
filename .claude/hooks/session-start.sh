#!/bin/bash
set -euo pipefail

# SessionStart hook: מזריק את 12 עקרונות העבודה עם Claude כהקשר לכל סשן.
PRINCIPLES_FILE="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}/.claude/prompting-principles.md"

if [ ! -f "$PRINCIPLES_FILE" ]; then
  exit 0
fi

CONTEXT="$(cat "$PRINCIPLES_FILE")"

jq -n --arg ctx "$CONTEXT" '{
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: $ctx
  }
}'
