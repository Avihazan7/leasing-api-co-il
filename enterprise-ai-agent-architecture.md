# Enterprise AI Agent System Architecture

> A plain transcription of the infographic by Habib Shaikh (AI Expert).

---

## Entry point

- **Microservice** exchanges **Task** / **Result** with the AI Agent.
- Note on the connection: *No exposure to cost-flooding attacks.*

## AI Agent (core)

- **AI Task controller**
  - AI task state
  - Cache
- **Analysis task based on current context**
- **MCP tools calls**
- **Response generation**
- **Evaluate results, confidence calculation**
- **Low confidence** → No → loops back to **Return response**
- **Return response**

## Author's notes (caveats)

- Logging and audit features are not part of this version; regulatory needs may require them later.
- Manual review steps (Human-in-the-Loop) were left out for simplicity.
- Retrieval-augmented generation is not included here.
- Responsible AI design is highly advanced — too complex for early-stage projects.

## External LLM path

- **External LLM task** / **External LLM result** →
- **MCP server** (MCP state, Cache) →
- **Really smart LLM**
- Notes:
  - Reasoning models like GPT-5.2
  - Custom model heads with Monte Carlo techniques

## Specialized LLM path

- **Specialized LLM task** / **Specialized LLM result** →
- **MCP server** (MCP state, Cache)
  - Load balancing retry
  - **AI agent (LangGraph)**
  - **Specialized LLM** (Finance, Healthcare, etc.)
  - **AI agent state**
  - Usual LangGraph project level
- Note: LLMs trained on synthetic datasets, including sample queries.

## Web scraper path

- **Web scrapper task** / **Web scrapper result** →
- **MCP server** (MCP state, Cache) →
- **Web scrapper** (Up-to-date information)
- Note: Web UI testing via Selenium Python script.
