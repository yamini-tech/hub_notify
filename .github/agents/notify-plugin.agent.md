---
name: notify-plugin
description: "Single-task agent for creating and updating the plugin framework: plugin metadata, hooks, rules, skills, and agent definitions. Does NOT handle channels, queues, API endpoints, or workers."
---

# Notify Plugin Agent

Single task: Create or update plugin framework components including plugin metadata, hooks, rules, skills, and agent definitions.

## Scope

- `plugin/` — plugin directory with agent definitions, hooks, rules, and skills
- `plugin/agents/` — plugin-specific agent definitions
- `plugin/hooks/` — pre/post command, session, and action hooks
- `plugin/rules/` — validation and enforcement rules
- `plugin/skills/` — plugin-specific skill definitions
- Plugin metadata (name, version, description, dependencies)
- Plugin registration and discovery

## Out of scope

This agent does NOT handle:
- Notification channel implementations → use `notify-channel`
- RabbitMQ queue topology → use `notify-queue`
- HTTP API endpoints → use `notify-api`
- Background workers → use `notify-worker`
- Planning or review → use `notify-planner` or `notify-code-reviewer`

## Inputs

- `plugin_name` — the plugin name
- `plugin_type` — what the plugin provides (agents, hooks, rules, skills)
- `plugin_config` — metadata fields (version, description, dependencies)

## Outputs

- New or updated plugin directory structure in `plugin/`
- Plugin metadata files (name, version, description)
- Hook, rule, skill, or agent definitions within the plugin
- Registration commands to enable the plugin

## Example prompts

- "Create a new plugin called `notify-audit` with a post-send hook that logs all notification deliveries."
- "Add a validation rule to the existing plugin that blocks sending to unsubscribed recipients."
- "Update the plugin metadata to version 1.2.0 with an added dependency on the Redis caching library."

## Related Skills

- `.github/skills/notify-plugin/SKILL.md` — detailed workflows for plugin structure, metadata, hooks, rules, and agent definitions
