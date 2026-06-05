# Claude Code Project Structure

> A plain transcription of the infographic created by Robbert van Vlijmen.

---

## Project tree

```
your-project/
├── CLAUDE.md
├── CLAUDE.local.md
├── .mcp.json
├── .claude/
│   ├── settings.json
│   └── settings.local.json
├── rules/
│   ├── code-style.md
│   ├── testing.md
│   └── api-conventions.md
├── commands/
│   ├── review.md
│   └── fix-issue.md
├── skills/
│   └── deploy/
│       ├── SKILL.md
│       └── deploy-config.md
├── agents/
│   ├── code-reviewer.md
│   └── security-auditor.md
└── hooks/
    └── validate-bash.sh
```

---

## CLAUDE.md
- Main instruction file loaded at session start
- Defines project overview, tech stack, build/test commands
- Stores coding conventions & architecture rules
- Supports personal overrides via CLAUDE.local.md (gitignored)

## .mcp.json
- Stores MCP integration configurations
- Connects tools like GitHub, JIRA, Slack, databases
- Shared through git for team-wide access

## settings.json
- Stores permissions and project configuration
- Controls tools, model selection, and hooks
- Supports local overrides with settings.local.json (gitignored)

## rules/
- Modular instruction files split by topic
- Covers style, testing, API conventions, etc.
- Can target specific files using frontmatter
- Loaded automatically when relevant files open

## commands/
- Manual custom slash commands
- Each .md becomes `/project:<filename>`
- Supports shell execution using `!` backtick syntax
- Useful for repeatable workflows like reviews

## skills/
- Auto-triggered workflows based on task context
- Each skill contains SKILL.md + support files
- Loaded only when needed to save context
- Best for automated context-aware workflows

## agents/
- Specialized subagents with isolated context
- Defines persona, tools, and model preferences
- Runs independently from the main session
- Examples: code-reviewer.md, security-auditor.md

## hooks/
- Event-based automation scripts
- Runs before or after tool usage
- Blocks risky operations when needed
- Can auto-format, lint, or validate actions
