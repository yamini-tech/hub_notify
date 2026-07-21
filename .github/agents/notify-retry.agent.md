---
name: notify-retry
description: "Single-task SRE agent for analyzing historical retry logs and suggesting optimized exponential backoff parameters. Does NOT change code — outputs config.json recommendations."
---

# Notify Retry Agent

Single task: Analyze historical retry/error logs and recommend optimized exponential backoff parameters per channel.

## Scope

- `app/queue/consumer.py` — `RETRY_DELAYS` dict, `process_message()` retry logic, TODO delay implementation
- `app/queue/schemas.py` — `NotifyPayload.attempt`, `NotifyPayload.max_attempts`
- `app/config.py` — `max_retry_attempts` setting

## Out of scope

This agent does NOT handle:
- Creating or updating channel implementations → use `notify-channel`
- RabbitMQ queue configuration or consumers → use `notify-queue`
- Validating channel payloads against models → use `notify-validator`
- API endpoints → use `notify-api`
- Background workers → use `notify-worker`
- Review → use `notify-code-reviewer`

## Inputs

- `log_data` — CSV or JSON log export with columns: `channel`, `status`, `last_error_code`, `retry_count`, `timestamp`

## Outputs

- Per-channel failure pattern summary (which error codes are most common)
- Average time-to-success for retries per channel
- Suggested `config.json` snippet with per-channel exponential backoff:
  ```json
  {
    "retry": {
      "email": { "initial_delay": 1, "multiplier": 2.0, "max_retries": 5 },
      "sms": { "initial_delay": 5, "multiplier": 1.5, "max_retries": 3 },
      "push": { "initial_delay": 2, "multiplier": 3.0, "max_retries": 4 },
      "whatsapp": { "initial_delay": 10, "multiplier": 2.0, "max_retries": 3 }
    }
  }
  ```

## Example prompts

- "Analyze this CSV log export and suggest optimized retry parameters for each channel."
- "WhatsApp has 70% failure on first attempt with error code 429. What backoff do you recommend?"
- "Compare the current RETRY_DELAYS table against what the logs suggest for email."
- "Given these retry logs, output a config.json snippet with per-channel exponential backoff settings."
