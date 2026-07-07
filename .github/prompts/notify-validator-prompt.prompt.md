---
mode: agent
agent: notify-validator
name: notify-validator-prompt
description:
  Prompt for the notify-validator agent. Analyzes channel dispatch signatures against Pydantic/SQLAlchemy models, detects contract violations, missing fields, type mismatches, and async/sync conflicts.
---

### Validation Checklist

1.  **Signature Extraction:** For each channel in `app/channels/`, extract the full `send_*()` function signature — all parameter names, types, defaults, and return types.
2.  **Model Comparison:** Compare each channel signature against `NotifyPayload` in `app/queue/schemas.py`. Flag:
    - Payload fields with no corresponding channel parameter (e.g., `subject` in payload but no `subject` param in `send_sms`)
    - Channel parameters whose names differ from the corresponding payload field (e.g., payload `recipient` → channel `device_token`)
    - Type mismatches (e.g., `str` vs `str | None`)
    - Optional/required mismatches (field required in payload but optional in channel, or vice versa)
3.  **Context Analysis:** Identify sync functions called from async context — flag as blocking the event loop and suggest `asyncio.to_thread()` or conversion to `async def`.
4.  **Cross-Cutting Checks:**
    - Verify `dispatch()` in `consumer.py` maps every `NotifyPayload` field to the correct channel param
    - Check that `SingleSendRequest` and `BulkRecipient` both support all `NotifyPayload` fields
    - Note any TODO comments referencing a `notification_jobs` table that does not exist
    - Verify the `QUEUE_FOR_TYPE` dict includes all channels handled in `dispatch()`

### Constraints

- Python 3.11+ type annotations (`str | None`, `dict | None`)
- Only analyze existing code — do not generate new channels, schemas, or dispatch logic

### Success Criteria

- Outputs a JSON report where keys are channel names and values are lists of discrepancies
- Each discrepancy includes: `field`, `type` (missing_field | type_mismatch | name_mismatch | sync_in_async), `payload_field`, `channel_param`, `payload_type`, `channel_type`, and `recommendation`
- Cross-cutting findings are listed under a `_meta` key
- Report is actionable — each finding has a concrete fix recommendation

### Usage Template

```
Validate the [email|sms|push|whatsapp|all] channel(s) against NotifyPayload and SingleSendRequest.
Output a JSON report with:
- Per-channel field mapping
- Missing/unused fields
- Type mismatches
- Async/sync context violations
- Cross-cutting gaps (DB model, API schema coverage)
Show the report and ask for confirmation before any code changes.
```
