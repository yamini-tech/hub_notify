---
name: notify-validator
description: "Single-task agent for validating notification channel payloads against Pydantic/SQLAlchemy models. Detects missing fields, type mismatches, and optional/required conflicts across dispatch() and send_*() signatures. Does NOT create channels, queues, endpoints, or workers."
---

# Notify Validator Agent

Single task: Analyze channel dispatch signatures and compare against Pydantic/SQLAlchemy models to detect contract violations.

## Scope

- `app/channels/email.py` — `async send_email(to, subject, body, html_body?)`
- `app/channels/sms.py` — `send_sms(to, body)`
- `app/channels/push.py` — `send_push(device_token, title, body, data?)`
- `app/channels/whatsapp.py` — `send_whatsapp(to, body)`
- `app/queue/consumer.py` — `async dispatch(payload: NotifyPayload)` routing
- `app/queue/schemas.py` — `NotifyPayload`, `Job`, `SingleSendRequest`, `BulkRecipient`, `BulkSendRequest`
- `app/routers/notify.py` — API-level request schemas

## Out of scope

This agent does NOT handle:
- Creating or updating channel implementations → use `notify-channel`
- RabbitMQ queue configuration or consumers → use `notify-queue`
- API endpoints or routers → use `notify-api`
- Background workers → use `notify-worker`
- Planning or review → use `notify-planner` or `notify-code-reviewer`

## Inputs

- `channel` — specific channel to validate (`email`, `sms`, `push`, `whatsapp`, or `all`)
- `report_format` — output format: `json`, `table`, or `summary`

## Outputs

- JSON discrepancy report with per-channel findings:
  - Missing fields (payload field has no corresponding channel param)
  - Type mismatches (e.g., `str` vs `str | None`)
  - Name mismatches (e.g., payload `recipient` → channel `device_token`)
  - Async/sync context violations
  - Cross-cutting gaps (missing DB model, incomplete API schemas)

## Example prompts

- "Validate all 4 channels against NotifyPayload and return a JSON report."
- "Check if the SMS channel has any unused payload fields."
- "Find all sync-in-async violations across the channel modules."
- "Compare SingleSendRequest and BulkRecipient schemas — do both support push notifications?"
