---
mode: agent
agent: notify-plugin
name: notify-plugin-prompt
description:
  Prompt for the notify-plugin agent. Creates or updates plugin framework components including metadata, hooks, rules, skills, and agent definitions.
---

### Requirements

1.  **Plugin Structure:** Create the plugin directory with standard layout: `plugin/<name>/agents/`, `hooks/`, `rules/`, `skills/`.
2.  **Metadata:** Define plugin metadata with name, version, description, author, and dependencies in a standard format.
3.  **Hooks:** Implement pre/post hooks for commands and sessions following the existing hook patterns in `.github/hooks/`.
4.  **Rules:** Define validation rules with clear descriptions, enforcement logic, and error messages.
5.  **Skills:** Define skill files with name, description, and trigger keywords.

### Constraints

- Plugin directories follow the naming convention `plugin/<plugin_name>/`
- Hook files use JSON format matching `.github/hooks/` conventions
- Rules must have clear failure messages and suggested fixes
- Skills must reference existing agents or tools

### Success Criteria

- Plugin directory structure matches the established pattern
- Hooks execute correctly in pre/post command and session contexts
- Rules validate inputs and provide actionable error messages
- Skills are discoverable and contain accurate trigger descriptions
- `pytest -q` passes for plugin-related tests

### Usage Template

```
Create a new plugin [name] that provides [hooks/rules/skills/agents] for [purpose].
Include:
- Plugin metadata with version [x.y.z]
- [Hook/rule/skill/agent] definitions
- Registration and discovery support
Show the diff and wait for my confirmation before applying.
```
