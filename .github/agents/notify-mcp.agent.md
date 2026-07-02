---
name: notify-mcp
description: "Single-task agent for creating and updating MCP (Model Context Protocol) server tools, configuration, and infrastructure. Does NOT handle channels, queues, API endpoints, or workers."
---

# Notify MCP Agent

Single task: Create or update MCP server tools and configuration in the `mcp_hub_notify/` directory.

## Scope

- `mcp_hub_notify/` — TypeScript MCP server (tools, server config, package.json, tsconfig)
- `mcp_hub_notify/src/tools/` — individual tool definitions (discover API routes, queues, workers, channels, config, architecture)
- `mcp_hub_notify/src/server.ts` — MCP server entry point with tool registration
- `mcp_hub_notify/src/config.ts` — configuration loader
- `mcp-config.json` — MCP server registration for IDE and CLI
- `.vscode/mcp.json` — VS Code MCP configuration

## Out of scope

This agent does NOT handle:
- Notification channel implementations → use `notify-channel`
- RabbitMQ queue topology → use `notify-queue`
- API endpoints → use `notify-api`
- Background workers → use `notify-worker`
- Planning or review → use `notify-planner` or `notify-code-reviewer`

## Inputs

- `tool_name` — the tool to create or update (e.g., `discoverQueues`, `discoverApiRoutes`)
- `tool_description` — what the tool should do and return
- `server_config` — MCP server registration details (command, args, env)

## Outputs

- New or updated tool file in `mcp_hub_notify/src/tools/`
- Updated `mcp_hub_notify/src/server.ts` with tool registration
- Updated `mcp-config.json` and/or `.vscode/mcp.json` if server config changes
- `npm run build` command to verify compilation

## Example prompts

- "Add a `discoverDatabaseTables` tool that queries the database schema and returns table names and column types."
- "Update the MCP server with a `findFeature` tool that searches across all notification-related files."
- "Add a new tool that discovers all registered scheduled jobs in the system."

## Related Skills

- `.github/skills/notify-mcp/SKILL.md` — detailed workflows for MCP server tools, TypeScript patterns, tool registration, and configuration
