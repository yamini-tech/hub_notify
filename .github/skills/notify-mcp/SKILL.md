---
name: notify-mcp
description: Create or update MCP (Model Context Protocol) server tools and configuration in the mcp_hub_notify/ TypeScript project. Use when adding new discovery tools, updating existing tool logic, or modifying MCP server registration (.vscode/mcp.json).
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 01 Jul 2026 00:00:00 GMT
---

# Notify MCP Skill

## Contents
- [Core Guidelines](#core-guidelines)
- [Workflow: Adding a New MCP Tool](#workflow-adding-a-new-mcp-tool)
- [Workflow: Modifying Server Configuration](#workflow-modifying-server-configuration)
- [Examples](#examples)

## Core Guidelines

- **Tool Isolation**: Each tool lives in its own file under `mcp_hub_notify/src/tools/<tool_name>.ts`. The file exports a single async function that accepts typed parameters and returns a structured response.
- **Tool Registration**: Every new tool must be registered in `mcp_hub_notify/src/server.ts` with a unique name, a clear description (for LLM dispatch), and an input schema defining the expected parameters.
- **Error Handling**: Tool functions must catch all errors and return structured error responses (`{ success: false, error: string }`) instead of throwing. Never let uncaught exceptions reach the MCP client.
- **TypeScript Standards**: Use strict TypeScript with ESM modules. Define input and output types/interfaces at the top of each tool file. Use async/await for all I/O operations.
- **Config Parity**: When adding tools that connect to external services, update `.vscode/mcp.json` with the required environment variables.

## Workflow: Adding a New MCP Tool

Use this checklist to implement a new discovery or utility tool for the MCP server.

**Task Progress:**
- [ ] 1. Define the tool's purpose, input parameters, and return type.
- [ ] 2. Create `mcp_hub_notify/src/tools/<tool_name>.ts` with the exported async function.
- [ ] 3. Implement input validation and error handling within the tool function.
- [ ] 4. Register the tool in `mcp_hub_notify/src/server.ts` with name, description, and input schema.
- [ ] 5. If the tool requires new environment variables, update `.vscode/mcp.json`.
- [ ] 6. Build and verify: `npm run build` passes with no TypeScript errors.
- [ ] 7. **Feedback Loop**: Check MCP server output for tool discovery -> review errors -> fix registration or type mismatches -> rebuild.

1. **Define the Tool**: Determine what data the tool returns (API routes, queue status, worker list, etc.) and what parameters it needs to filter or scope the results.
2. **Implement the Tool**: Create the TypeScript file following the pattern in existing tools (`discoverApiRoutes.ts`, `discoverQueues.ts`, etc.). Use the same response format as other tools.
3. **Handle Errors**: Wrap the main logic in try/catch. Return `{ success: false, error: message }` on failure and `{ success: true, data: result }` on success.
4. **Register in Server**: Add the tool to the tools array in `server.ts`. The description field is critical — it must clearly tell an LLM when to invoke this tool.
5. **Update Config**: If the tool connects to a database, queue, or external API, add the connection string or endpoint to `.vscode/mcp.json` under the server's `env` block.
6. **Test**: Run `npm run build` to verify compilation. Run the MCP server locally and confirm the new tool appears in the capabilities list.

## Workflow: Modifying Server Configuration

Use this checklist when updating MCP server registration details (command, args, environment variables).

**Task Progress:**
- [ ] 1. Identify which config files need updating: `.vscode/mcp.json`.
- [ ] 2. Update the `command` and `args` arrays if the server executable or arguments change.
- [ ] 3. Add, remove, or update environment variables in the `env` block. Use `{env:VAR_NAME}` interpolation for secrets.
- [ ] 4. Verify the JSON is valid (no trailing commas, valid string values).
- [ ] 5. Test that the MCP server starts and connects successfully.

## Examples

### High-Fidelity Implementation: Creating a New MCP Tool

**Tool File (`mcp_hub_notify/src/tools/discoverEnvironmentConfig.ts`):**
```typescript
export async function discoverEnvironmentConfigHandler() {
  try {
    const config = {
      ai_service_url: process.env.AI_SERVICE_URL || "http://localhost:8001",
      rabbitmq_url: process.env.RABBITMQ_URL || "amqp://guest:guest@localhost:5672/",
      upload_dir: process.env.UPLOAD_DIR || "./uploads",
    };
    return { content: [{ type: "text", text: JSON.stringify(config, null, 2) }] };
  } catch (error) {
    return { content: [{ type: "text", text: `Error: ${error}` }], isError: true };
  }
}
```

**Registration in `server.ts`:**
```typescript
import { discoverEnvironmentConfigHandler } from "./tools/discoverEnvironmentConfig.js";

server.tool(
  "discover_environment_config",
  "Discover notification service configuration",
  {},
  discoverEnvironmentConfigHandler
);
```
