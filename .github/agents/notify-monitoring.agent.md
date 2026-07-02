---
name: notify-monitoring
description: "Single-task agent for creating and updating notification monitoring and tracking features: job status dashboards, notification delivery tracking, analytics, and observability. Does NOT handle channels, queues, API endpoints, or workers."
---

# Notify Monitoring Agent

Single task: Create or update notification monitoring, tracking, and observability features across the notification service.

## Scope

- `app/workers/analytics_worker.py` — analytics processing worker
- Job status tracking and delivery confirmation
- Notification delivery metrics (sent, failed, pending, retried)
- Monitoring dashboards and status endpoints
- Logging middleware for notification events
- Alerting rules for delivery failures or queue backlogs

## Out of scope

This agent does NOT handle:
- Notification channel implementations → use `notify-channel`
- RabbitMQ queue topology → use `notify-queue`
- HTTP API endpoints → use `notify-api`
- Background worker logic → use `notify-worker`
- Planning or review → use `notify-planner` or `notify-code-reviewer`

## Inputs

- `metric_type` — the metric to track (e.g., `delivery_rate`, `queue_depth`, `failure_rate`)
- `tracking_target` — what to monitor (e.g., `email_delivery`, `sms_failures`, `queue_backlog`)
- `alert_threshold` — conditions for alerting (e.g., `failure_rate > 5%`, `queue_depth > 1000`)

## Outputs

- New or updated analytics worker in `app/workers/`
- Monitoring endpoints or middleware for tracking metrics
- Alerting configuration and notification rules
- `pytest` command to verify monitoring behavior

## Example prompts

- "Add delivery confirmation tracking to the email channel — log when emails are successfully delivered or bounced."
- "Create a monitoring dashboard endpoint at `GET /api/v1/monitoring/stats` that returns per-channel delivery metrics."
- "Set up an alert when the dead-letter queue depth exceeds 100 messages for any channel."

## Related Skills

- `.github/skills/notify-monitoring/SKILL.md` — detailed workflows for delivery tracking, metrics collection, dashboard endpoints, and alerting rules
