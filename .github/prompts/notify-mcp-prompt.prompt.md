---
mode: agent
agent: notify-mcp
name: notify-mcp-prompt
description:
  Prompt for the notify-mcp agent. Creates or updates MCP server tools and configuration in the mcp_hub_notify/ TypeScript project.
---

### Requirements

1.  **Tool Implementation:** Create a new file `mcp_hub_notify/src/tools/<tool_name>.ts` following the pattern in existing tool files.
2.  **Tool Registration:** Register the new tool in `mcp_hub_notify/src/server.ts` with a name, description, and input schema.
3.  **Server Config:** If a new MCP server is needed, update `mcp-config.json` and `.vscode/mcp.json` with command, args, and environment variables.
4.  **TypeScript Standards:** Use proper TypeScript types, async/await, and error handling. All tool functions return structured responses.

### Constraints

- TypeScript with ESM modules — use `import`/`export` syntax
- Tools must handle errors gracefully and return structured error responses
- Tool descriptions must be clear so an LLM knows when to invoke them
- Environment variables use `{env:VAR_NAME}` interpolation in mcp-config.json

### Success Criteria

- `npm run build` passes with no TypeScript errors
- Tool appears when querying MCP server capabilities
- Tool returns accurate data from the notification service
- Tool handles edge cases (empty results, missing config) without crashing

### Usage Template

```
Create a new MCP tool [tool_name] in mcp_hub_notify/src/tools/ that [description].
Include:
- Input schema for any parameters
- Error handling for common failure modes
- Registration in mcp_hub_notify/src/server.ts
Show the diff and wait for my confirmation before applying.
```
