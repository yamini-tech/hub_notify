---
mode: agent
agent: notify-agent
name: notify-agent-prompt
description:
  Coordinator prompt for the hub_notify repository. Routes requests to the appropriate single-task agent based on the task domain.
---

This coordinator does NOT implement tasks directly. It identifies the task type and hands off:

| Task type | Agent | Prompt file |
|---|---|---|
| Create/update a notification channel | `notify-channel` | `notify-channel-prompt.prompt.md` |
| Configure/inspect RabbitMQ queues | `notify-queue` | `notify-queue-prompt.prompt.md` |
| Create/update FastAPI endpoints | `notify-api` | `notify-api-prompt.prompt.md` |
| Create/update queue workers | `notify-worker` | `notify-worker-prompt.prompt.md` |
| Create/update MCP server tools | `notify-mcp` | `notify-mcp-prompt.prompt.md` |
| Create/update RAG pipeline components | `notify-rag` | `notify-rag-prompt.prompt.md` |
| Create/update plugin framework | `notify-plugin` | `notify-plugin-prompt.prompt.md` |
| Create/update AI workflow orchestration | `notify-ai-workflow` | `notify-ai-workflow-prompt.prompt.md` |
| Create/update monitoring and tracking | `notify-monitoring` | `notify-monitoring-prompt.prompt.md` |
| Generate an implementation plan | `notify-planner` | `notify-planner.agent.md` |
| Review code before merge | `notify-code-reviewer` | `notify-code-reviewer.agent.md` |

If the request spans multiple domains, ask the user to break it into single-task prompts.
