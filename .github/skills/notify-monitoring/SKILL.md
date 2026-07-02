---
name: notify-monitoring
description: Create or update notification monitoring, tracking, and observability features including delivery confirmation tracking, metrics collection, monitoring dashboards, and alerting rules. Use when adding delivery analytics, failure detection, or visibility into notification system health.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 01 Jul 2026 00:00:00 GMT
---

# Notify Monitoring Skill

## Contents
- [Core Guidelines](#core-guidelines)
- [Workflow: Adding Delivery Tracking to a Channel](#workflow-adding-delivery-tracking-to-a-channel)
- [Workflow: Implementing a Metrics Dashboard Endpoint](#workflow-implementing-a-metrics-dashboard-endpoint)
- [Examples](#examples)

## Core Guidelines

- **Event Logging**: Every notification delivery attempt must log: channel, recipient, message ID, status (sent/failed/bounced/pending), timestamp, and duration. Use structured logging with a consistent schema across all channels.
- **Metrics Collection**: Collect at minimum: delivery rate (per channel), failure rate (per channel), queue depth (per queue), processing latency (p95/p99), and retry counts. Metrics should be updatable in real-time and queryable with time-range filters.
- **Alert Deduplication**: Alert rules must include a cooldown period (default: 5 minutes) to prevent alert storms. An alert for "queue depth > 1000" should not fire every evaluation cycle if the condition persists.
- **Non-blocking**: Monitoring code must never block or slow down notification delivery. Use background tasks for metrics aggregation and alert evaluation. Delivery tracking should be fire-and-forget (log and continue).
- **Persistence Strategy**: Recent metrics (last 1 hour) live in memory for fast queries. Historical metrics (beyond 1 hour) are persisted to the database with configurable retention (default: 30 days).

## Workflow: Adding Delivery Tracking to a Channel

Use this checklist to add delivery confirmation tracking for a notification channel.

**Task Progress:**
- [ ] 1. Identify the channel to track (email, SMS, push, WhatsApp) and the delivery events to capture.
- [ ] 2. Add structured logging to the channel's `send()` function — log before sending, on success, and on failure.
- [ ] 3. Update the analytics worker to consume delivery events and aggregate metrics.
- [ ] 4. Add an API endpoint to query delivery metrics for the tracked channel.
- [ ] 5. Define alert thresholds for the channel (e.g., failure rate > 5% over 10 minutes).
- [ ] 6. Test with dry-run mode — verify events are logged without actual delivery.
- [ ] 7. **Feedback Loop**: Trigger test deliveries through the channel -> check metrics endpoint -> verify logged events match actual outcomes -> adjust tracking or aggregation logic.

1. **Identify Events**: Determine what constitutes a delivery event for the channel:
   - Email: sent, delivered, bounced, opened, clicked
   - SMS: sent, delivered, failed, undelivered
   - Push: sent, delivered, dismissed, failed
   - WhatsApp: sent, delivered, read, failed

2. **Instrument the Channel**: Add logging calls in the channel's `send()` function. Use the channel name as a structured field. Always include a unique message ID for cross-referencing with queue logs.

3. **Wire Analytics**: Create or update the analytics worker (`app/workers/analytics_worker.py`) to consume delivery events from a dedicated analytics queue.

4. **Build Metrics Endpoint**: Implement a query endpoint (`GET /api/v1/jobs/stats`) that returns per-queue counts and status distributions.

5. **Set Alerts**: Define threshold-based alert rules. Alerts should specify: metric name, condition, threshold, duration, severity (info/warning/critical), and notification target.

## Workflow: Implementing a Metrics Dashboard Endpoint

Use this checklist to create or update a monitoring API endpoint that exposes delivery and system metrics.

**Task Progress:**
- [ ] 1. Define the metrics to expose and the query parameters (channel filter, time range, granularity).
- [ ] 2. Implement in-memory metric storage with periodic flushing to the database.
- [ ] 3. Create the API endpoint in `app/routers/` following the existing pattern.
- [ ] 4. Implement data aggregation logic (counts, rates, percentiles) with the requested granularity.
- [ ] 5. Add pagination for historical queries.
- [ ] 6. Write tests that verify the endpoint returns correct metrics.
- [ ] 7. **Feedback Loop**: Call the endpoint with various parameters -> validate metric accuracy against raw logs -> fix aggregation logic -> re-test.

## Examples

### High-Fidelity Implementation: Analytics Event Processing

**Analytics Worker (`app/workers/analytics_worker.py`):**
```python
import asyncio
import random
from app.queue.job_store import job_store
from app.queue.schemas import Job, JobStatus

async def _process(job: Job) -> None:
    task_type = job.payload.get("task_type", "engagement_analysis")
    event_count = job.payload.get("event_count", random.randint(500, 10000))
    job.total = event_count

    steps: list[tuple[int, str]] = {
        "engagement_analysis": [
            (10, f"Loading {event_count:,} user events from database…"),
            (25, "Parsing event payloads & normalising timestamps…"),
            (40, "Segmenting users by activity cohort…"),
            (58, "Computing session duration & page-view metrics…"),
            (72, "Calculating retention & churn signals…"),
            (85, "Aggregating engagement scores per user…"),
            (95, "Writing results to analytics store…"),
            (100, f"✓ {event_count:,} events analysed · engagement report ready"),
        ],
        "user_logs": [
            (15, f"Ingesting {event_count:,} log lines…"),
            (35, "Parsing log levels, services & trace IDs…"),
            (55, "Detecting error patterns & anomalies…"),
            (75, "Building per-service error rate timeline…"),
            (90, "Generating alert digest…"),
            (100, f"✓ {event_count:,} log lines processed"),
        ],
    }.get(task_type, [
        (20, "Loading data…"),
        (50, "Processing…"),
        (80, "Aggregating results…"),
        (100, "✓ Task complete"),
    ])

    await job_store.update(job.job_id, JobStatus.PROCESSING,
                           progress=0, message=steps[0][1])
    for pct, msg in steps:
        await asyncio.sleep(random.uniform(0.3, 1.0))
        status = JobStatus.DONE if pct == 100 else JobStatus.PROCESSING
        done = int(event_count * pct / 100)
        await job_store.update(job.job_id, status, progress=pct,
                               message=msg, done_count=done)
```

**Queue Stats Endpoint (`app/routers/jobs.py`):**
```python
@router.get("/stats")
async def queue_stats():
    return {"queues": list(job_store.stats().values())}

@router.get("/stream")
async def stream_events():
    q = job_store.subscribe()
    async def generator():
        try:
            async for chunk in job_store.stream(q):
                yield chunk
        finally:
            job_store.unsubscribe(q)
    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        },
    )
```
