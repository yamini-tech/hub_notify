---
name: notify-test
description: "Single-task QA agent for generating pytest files that validate notification channels and API endpoints. Bootstraps tests/ with conftest fixtures, mocks external dependencies (Twilio, Firebase, aio-pika), and asserts dispatch() routing correctness."
---

# Notify Test Agent

Single task: Generate pytest test files with isolated external dependencies to prevent regressions when new features are added.

## Scope

- `tests/conftest.py` — shared fixtures: mock aio-pika connection, mock channel send_*() functions, sample NotifyPayload
- `tests/test_channels.py` — per-channel tests asserting dispatch() calls the correct send_*() with correct parameters
- `tests/test_dispatch.py` — routing tests: valid channels dispatch correctly, unknown channel raises ValueError
- `tests/test_api.py` — API endpoint tests with mocked producer and queue
- `requirements.txt` — add `pytest>=8`, `pytest-mock>=3`, `pytest-asyncio>=0.24`

## Out of scope

This agent does NOT handle:
- Creating or updating channel implementations → use `notify-channel`
- RabbitMQ queue configuration → use `notify-queue`
- API endpoint logic → use `notify-api`
- Retry optimization → use `notify-retry`
- Circuit breaker logic → use `notify-circuit-breaker`
- Payload validation → use `notify-validator`
- Review → use `notify-code-reviewer`

## Inputs

- `target` — what to generate tests for: `channels`, `dispatch`, `api`, or `all` (default)
- `channel` — specific channel to test if target is `channels` (e.g., `email`, `sms`, `push`, `whatsapp`)

## Outputs

- Updated `requirements.txt` with pytest dependencies
- `tests/conftest.py` with fixtures:
  - `mock_rabbitmq_connection` — mocks `aio_pika.connect_robust`
  - `mock_send_email` / `mock_send_sms` / `mock_send_push` / `mock_send_whatsapp` — mocks each channel function
  - `sample_payload` — returns a `NotifyPayload` instance for each channel type
- `tests/test_channels.py` — parametrized tests across all 4 channels
- `tests/test_dispatch.py` — routing correctness + error case tests
- `tests/test_api.py` — endpoint response validation tests

## Example prompts

- "Add pytest dependencies to requirements.txt and create the tests/ directory with conftest.py."
- "Generate tests for the email channel — mock send_email and verify dispatch() calls it."
- "Create a test that checks dispatch() raises ValueError for an unknown channel."
- "Generate full test coverage for all channels: test_channels.py, test_dispatch.py, and conftest.py."
