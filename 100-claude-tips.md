# 100 Claude Tips in One Page

> The only Claude cheatsheet you need in 2026.

A plain transcription of all 100 tips, organized into the original 10 categories.

---

## 1. Setup (1–10)

1. **Pick your model** — Opus for hard tasks. Sonnet for speed. Haiku for bulk.
2. **Turn on memory** — Settings > Memory. Claude remembers you across chats.
3. **Set your style** — Settings > Style. Tell Claude how you want every reply.
4. **Use Projects** — Group files, instructions, and memory into one workspace.
5. **Upload files first** — Drop PDFs, CSVs, images before you ask anything.
6. **Enable web search** — Let Claude pull live data instead of guessing.
7. **Enable artifacts** — Turn on in Settings > Features for live code and docs.
8. **Add connectors** — Link Gmail, Drive, Calendar, Slack, Canva, Notion, and more.
9. **Try the desktop app** — Always-on access. Works on macOS, Windows, and Linux.
10. **Use keyboard shortcuts** — Cmd+K for new chat. Cmd+Shift+C to copy last response.

## 2. Prompting (11–20)

11. **Be specific first** — "Write 300 words in a casual tone about X" beats "write about X."
12. **Give examples** — Show Claude one good output and it mirrors the pattern.
13. **Use XML tags** — Wrap inputs in `<context>` or `<rules>` tags for clarity.
14. **Set a role** — "You are a senior copywriter" activates stronger domain output.
15. **Say what NOT to do** — "No bullet points. No filler. No intros." removes junk fast.
16. **Ask for options** — "Give me 3 versions" beats asking for one and hoping.
17. **Chain your prompts** — Break big tasks into steps. Feed each output into the next.
18. **Say "be concise"** — Claude defaults long. Two words fix it instantly.
19. **Paste your constraints** — Word count, tone, audience, format. All in one prompt.
20. **Iterate, don't restart** — Follow up in the same chat. Claude improves with feedback.

## 3. Memory and Context (21–30)

21. **Memory is automatic** — Claude stores your name, preferences, and project context.
22. **Edit your memory** — "Remember that I prefer short answers" updates it instantly.
23. **Delete memory** — "Forget everything about my job" removes specific items.
24. **Use user preferences** — Settings > User Preferences for permanent instructions.
25. **Pin project context** — Upload a brief or style guide and pin it to a project.
26. **Memory has limits** — It stores key facts, not full conversations. Be explicit.
27. **Check what Claude knows** — Ask "What do you remember about me?" anytime.
28. **Memory works for free** — Persistent memory is available on every plan since March 2025.
29. **New chat, same you** — Claude carries preferences into every conversation.
30. **Incognito skips memory** — Start an incognito chat when you want a blank slate.

## 4. Claude Code Basics (31–40)

31. **Install in one line** — `curl -fsSL https://claude.ai/install.sh | sh`
32. **Run from project root** — Always cd into your repo before starting a session.
33. **Create CLAUDE.md** — One file in your root gives Claude your full project context.
34. **Use plan mode** — Type "plan" before complex tasks. Claude thinks before coding.
35. **Pipe input in** — `git diff | claude -p "review this"` for instant analysis.
36. **Drag files in** — Drop files into the terminal. Claude reads them automatically.
37. **Use @mentions** — `@README.md` or `@src/components/` to include files by path.
38. **Use /compact** — Compress your session when context gets large. Do it early.
39. **Use /clear** — Resets the full context. Fresh start without leaving the session.
40. **Check your spend** — `/cost` shows token usage and spend for the current session.

## 5. Claude Code Commands (41–50)

41. **/resume** — Recover a lost or crashed session instantly.
42. **/context** — See exactly what Claude is holding in context right now.
43. **/model** — Switch models mid-session without restarting.
44. **/btw** — Ask a side question without interrupting the current task.
45. **/compact** — Condense a bloated session to free tokens for more work.
46. **/permissions** — View or change what tools Claude is allowed to use.
47. **/help** — See all available commands including plugin commands.
48. **/buddy** — Easter egg. Hatches a unique creature that watches you code.
49. **/doctor** — Diagnose environment and configuration issues instantly.
50. **/release-notes** — Check what shipped in the latest Claude Code version.

## 6. CLAUDE.md and Skills (51–60)

51. **CLAUDE.md loads auto** — Claude reads it at the start of every session. No setup needed.
52. **Keep it lean** — Too many rules burn context. Stick to what matters most.
53. **Add coding standards** — Put your linting rules, naming conventions, and stack info.
54. **Define what to avoid** — "Never refactor files outside the task" prevents AI drift.
55. **Add project goals** — A one-liner on what you are building gives Claude focus.
56. **Use skills folder** — `.claude/skills/` holds reusable prompt workflows.
57. **Create custom commands** — Add `.claude/commands/review.md` for repeatable workflows.
58. **Scope by project** — Project-level CLAUDE.md overrides user-level defaults.
59. **Update regularly** — Revise your CLAUDE.md monthly. Remove anything outdated.
60. **Use the Karpathy 4** — Ask first. Simplest fix. Don't touch unrelated. Flag uncertainty.

## 7. Artifacts and Output (61–70)

61. **Artifacts preview live** — HTML, React, SVG, Mermaid, and code all render in the panel.
62. **Ask for artifacts** — "Make this an artifact" for anything you plan to share.
63. **Version history** — Every edit creates a version. Roll back if a revision breaks it.
64. **Share via link** — Click Share on any artifact. Anyone with the link can view it.
65. **Download source** — Grab the raw code, doc, or file from any artifact.
66. **Build full apps** — Claude can create interactive React apps inside artifacts.
67. **Make diagrams** — "Draw a flowchart of this process" creates live Mermaid output.
68. **Create dashboards** — Ask for a data dashboard. Claude builds it with charts.
69. **Use code execution** — Claude runs Python, analyzes data, and returns results live.
70. **Export to file** — Ask Claude to save output as .md, .html, .csv, or .docx.

## 8. MCP and Connectors (71–80)

71. **MCP is the bridge** — Model Context Protocol connects Claude to your real tools.
72. **500+ connectors** — Gmail, Calendar, Drive, Slack, Notion, Canva, Stripe, and more.
73. **One-click connect** — Settings > Connectors. Authorize with your existing login.
74. **Claude reads your tools** — Once connected, Claude can search, read, and take actions.
75. **Connectors in Code** — Claude Code uses MCP to access GitHub, DBs, and APIs.
76. **Creative connectors** — Blender, Figma, and 7 more launched April 2025.
77. **Build custom MCPs** — Create your own MCP server for internal tools.
78. **Connectors in Excel** — Claude connects to external data directly inside spreadsheets.
79. **Works across plans** — Free and Pro users both get connector access.
80. **Reconnect per session** — Some connectors require re-auth each time. By design.

## 9. Cowork and Agents (81–90)

81. **Cowork is persistent** — Files, skills, and memory carry across every session.
82. **Plugins bundle everything** — Skills + connectors + commands in one installable package.
83. **Try one-click plugins** — Legal, sales, finance, marketing, data, and more.
84. **Plugin marketplace** — Browse and install community plugins since February 2026.
85. **Dispatch agents** — Trigger Cowork agents remotely, including from your phone.
86. **Multi-agent orchestration** — Commander and sub-agents split complex tasks automatically.
87. **Dreaming mode** — Claude reviews past sessions overnight and self-improves.
88. **Routines** — Set up async automations. Wakes up to PRs ready to merge.
89. **Live artifacts** — Artifacts in Cowork pull real-time data from MCP servers.
90. **Scheduled tasks** — Set recurring tasks that run on a schedule with full context.

## 10. Power User (91–100)

91. **Combine tools** — Web search + connectors + artifacts in one prompt.
92. **Use opusplan** — Opus thinks, Sonnet writes. Best of both in one session.
93. **Set hooks** — Run custom code before or after every tool use automatically.
94. **Use sub-agents** — Delegate sub-tasks to specialized agents from one session.
95. **Pipe to DevOps** — `claude -p "write a PR description" | gh pr create`
96. **Create custom skills** — Build reusable prompt workflows Claude loads on demand.
97. **Use fast mode** — Same Opus model, faster output for simpler tasks.
98. **Use worktrees** — Run agents in separate git worktrees for parallel work.
99. **Audit with /context** — Check what Claude holds before it takes any major action.
100. **Read the changelog** — `/release-notes` after every update. New features ship weekly.

---

*100 tips done.*
