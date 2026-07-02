---
mode: agent
agent: notify-monitoring
name: notify-monitoring-prompt
description:
  Prompt for the notify-monitoring agent. Creates or updates notification monitoring, tracking, and observability features.
---

### Requirements

1.  **Delivery Tracking:** Add delivery confirmation tracking for each notification channel — log success, failure, bounce, and delay events.
2.  **Metrics Collection:** Collect and expose key metrics: delivery rate, failure rate, queue depth, processing latency, and retry counts.
3.  **Dashboard Endpoints:** Provide API endpoints to query current and historical metrics with optional time-range filtering.
4.  **Alerting:** Define alert rules based on metric thresholds with configurable severity levels and notification channels.

### Constraints

- Python 3.11+ with async/await
- Metrics should be collected in-memory with optional persistence to the database
- Dashboard endpoints must support pagination and time-range filtering
- Alert rules must not trigger repeatedly for the same condition (deduplication with cooldown)

### Success Criteria

- Delivery events are logged with channel, status, timestamp, and message ID
- Metrics endpoint returns accurate counts for the requested time range
- Alerts trigger when thresholds are exceeded and include actionable context
- `pytest -q` passes for monitoring-related tests

### Usage Template

```
Add monitoring for [channel/metric] in the notification service.
Include:
- Tracking of [specific events]
- Metrics endpoint or dashboard integration
- Alert rules for [threshold conditions]
Show the diff and wait for my confirmation before applying.
```
