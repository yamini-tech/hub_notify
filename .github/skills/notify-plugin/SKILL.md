---
name: notify-plugin
description: Create or update plugin framework components including plugin metadata, hooks, rules, skills, and agent definitions. Use when extending the notification service with reusable plugin packages that add hooks, validation rules, or custom capabilities.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 01 Jul 2026 00:00:00 GMT
---

# Notify Plugin Skill

## Contents
- [Core Guidelines](#core-guidelines)
- [Workflow: Creating a New Plugin](#workflow-creating-a-new-plugin)
- [Workflow: Adding a Hook to an Existing Plugin](#workflow-adding-a-hook-to-an-existing-plugin)
- [Examples](#examples)

## Core Guidelines

- **Plugin Structure**: Every plugin follows `plugin/<name>/` with optional subdirectories: `agents/`, `hooks/`, `rules/`, `skills/`. At minimum, the plugin must have a metadata definition (name, version, description).
- **Metadata Required**: Each plugin must declare `name`, `version` (semver), `description`, and `author` in its metadata. Dependencies on other plugins or external packages must be explicitly listed.
- **Hook Isolation**: Hooks are standalone JSON files following the `.github/hooks/` conventions. Each hook does one thing — validate, transform, or log. Hooks should not modify plugin state.
- **Rule Enforcement**: Rules must have clear descriptions, deterministic enforcement logic, and actionable error messages that tell the user how to fix the violation. Rules never modify data — they only validate and report.
- **Agent Registration**: Plugin-specific agent definitions in `agents/` must reference the parent plugin in their metadata. Agent names should be prefixed with the plugin name to avoid conflicts.

## Workflow: Creating a New Plugin

Use this checklist to create a new plugin package for the notification service.

**Task Progress:**
- [ ] 1. Define the plugin's purpose, components (hooks, rules, skills, agents), and metadata.
- [ ] 2. Create the plugin directory structure: `plugin/<name>/`.
- [ ] 3. Create the plugin metadata file with name, version, description, author, and dependencies.
- [ ] 4. Implement each component (hooks, rules, skills, agents) in its respective subdirectory.
- [ ] 5. Register the plugin so it is discoverable by the plugin loader.
- [ ] 6. Write tests that verify each component behaves correctly.
- [ ] 7. **Feedback Loop**: Run plugin registration -> test hooks and rules -> review agent definitions -> fix errors -> re-register.

1. **Define Purpose**: Document what the plugin adds to the notification service. Example: "The notify-lint plugin enforces Python code style by running Black formatter as a PostToolUse hook."
2. **Create Structure**: Run `mkdir -p plugin/<name>/{agents,hooks,rules,skills}`. Touch a metadata file (e.g., `plugin.json` or `plugin.yaml`) at the root.
3. **Write Metadata**: Include name, version, description, author, and dependencies field. Use semver for versioning.
4. **Implement Components**:
   - **Hooks**: Create JSON files following the `pre-command.json` / `post-session.json` pattern.
   - **Rules**: Create rule files with condition, action, and error message.
   - **Skills**: Create skill files referencing the plugin's capabilities.
   - **Agents**: Create agent files with handoffs scoped to the plugin's domain.
5. **Register Plugin**: Add the plugin to the plugin discovery mechanism (plugin registry, configuration file, or auto-scan directory).
6. **Test**: Verify hooks trigger correctly, rules catch violations, agents are discoverable, and skills appear in the catalog.

## Workflow: Adding a Hook to an Existing Plugin

Use this checklist when extending an existing plugin with a new hook.

**Task Progress:**
- [ ] 1. Determine the hook type (pre-command, post-command, pre-session, post-session) and trigger conditions.
- [ ] 2. Create or update the hook JSON file in `plugin/<name>/hooks/`.
- [ ] 3. Implement the hook logic with clear success/failure output.
- [ ] 4. Test the hook by simulating the trigger condition.
- [ ] 5. Update the plugin metadata version if the hook is a significant addition.

## Examples

### High-Fidelity Implementation: Plugin Metadata and Hook

**Repository-level Plugin Metadata (`plugin/.plugin/plugin.json`):**
```json
{
  "repository": "hub_notify",
  "repository_role": "worker_runtime",
  "name": "SmartHub Notification & Worker Plugins",
  "version": "1.0.0",
  "repository_priority": 80,
  "orchestrator_registration": {
    "enabled": true,
    "managed_by": "hub_infra"
  },
  "mcp_server": {
    "name": "mcp_hub_notify",
    "enabled": true,
    "auto_start": true,
    "is_controller": false
  },
  "plugin_root": "plugin",
  "supports": ["agents", "skills", "rules", "hooks"],
  "discovery": {
    "enabled": true,
    "recursive": true
  },
  "orchestration": {
    "enabled": true,
    "allow_agent_execution": true,
    "allow_skill_execution": true,
    "allow_hook_execution": true,
    "allow_rule_enforcement": true
  }
}
```

**Existing Hook — Python Black Formatter (`plugin/hooks/python-format-sync.json`):**
```json
{
  "id": "cixio.notify.hooks.blackFormat",
  "name": "Python Black Formatter Sync",
  "event": "PostToolUse",
  "action": {
    "type": "shellExecution",
    "command": "python",
    "args": ["-m", "black", "."],
    "options": {
      "env": {
        "TARGET_FILE": "${activeEditorFile}"
      }
    }
  },
  "timeout": 10000
}
```
