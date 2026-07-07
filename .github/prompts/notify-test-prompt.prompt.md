---
mode: agent
agent: notify-test
name: notify-test-prompt
description:
  Prompt for the notify-test agent. Generates pytest test files with mocked external dependencies to validate notification channels, dispatch routing, and API endpoints.
---

### Requirements

1.  **Dependencies:** Add to `requirements.txt`:
    - `pytest>=8`
    - `pytest-mock>=3`
    - `pytest-asyncio>=0.24`

2.  **`tests/conftest.py`** — Shared fixtures:
    - `mock_rabbitmq_connection` — use `pytest.mark.asyncio` and `AsyncMock` to mock `aio_pika.connect_robust`, return a mock channel with `declare_queue` and `consume` methods
    - `mock_send_email` — `mocker.patch("app.channels.email.send_email", return_value="mocked-msg-id")`
    - `mock_send_sms` — `mocker.patch("app.channels.sms.send_sms", return_value="mocked-sid")`
    - `mock_send_push` — `mocker.patch("app.channels.push.send_push", return_value="mocked-fcm-id")`
    - `mock_send_whatsapp` — `mocker.patch("app.channels.whatsapp.send_whatsapp", return_value="mocked-sid")`
    - `sample_email_payload` / `sample_sms_payload` / `sample_push_payload` / `sample_whatsapp_payload` — `NotifyPayload` instances with channel-specific fields populated

3.  **`tests/test_channels.py`** — Per-channel parametrized test:
    ```python
    @pytest.mark.asyncio
    @pytest.mark.parametrize("channel,payload,mock_name,expected_params", [
        ("email", "sample_email_payload", "mock_send_email", {"to": ..., "subject": ..., "body": ..., "html_body": ...}),
        ("sms", "sample_sms_payload", "mock_send_sms", {"to": ..., "body": ...}),
        ("push", "sample_push_payload", "mock_send_push", {"device_token": ..., "title": ..., "body": ..., "data": ...}),
        ("whatsapp", "sample_whatsapp_payload", "mock_send_whatsapp", {"to": ..., "body": ...}),
    ])
    async def test_dispatch_calls_correct_sender(channel, payload, mock_name, expected_params, request):
        mock_fn = request.getfixturevalue(mock_name)
        await dispatch(payload)
        mock_fn.assert_called_once_with(**expected_params)
    ```

4.  **`tests/test_dispatch.py`** — Routing tests:
    - Test that `dispatch()` with each valid channel calls the corresponding `send_*()` function
    - Test that `dispatch()` with an unknown channel raises `ValueError`
    - Test that `dispatch()` passes all expected fields from `NotifyPayload` to the sender

5.  **`tests/test_api.py`** — API endpoint tests:
    - Use `TestClient` from FastAPI
    - Mock the `publish()` function to assert the correct `NotifyPayload` is published
    - Test success responses, validation errors (422), and missing fields

### Constraints

- Use `pytest.mark.asyncio` for all async test functions
- No real external calls — every external dependency must be mocked
- Test files go in `tests/` directory
- Use `ruff check tests/` to verify style after generation

### Success Criteria

- `tests/` directory exists with `__init__.py`
- `pytest tests/ -q` passes with all tests green
- Each channel has at least one test verifying parameter correctness
- Unknown channel case is tested
- API endpoints return expected status codes

### Usage Template

```
Generate pytest test infrastructure for the notification service.

1. Add pytest dependencies to requirements.txt
2. Create tests/conftest.py with fixtures for:
   - Mocked RabbitMQ connection
   - Mocked send_email / send_sms / send_push / send_whatsapp
   - Sample NotifyPayload instances for each channel
3. Create tests/test_channels.py with parametrized dispatch tests
4. Create tests/test_dispatch.py with routing correctness tests
5. Create tests/test_api.py with endpoint validation tests

Show all diffs and wait for my confirmation before applying.
```
