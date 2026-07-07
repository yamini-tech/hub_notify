---
mode: agent
agent: notify-retry
name: notify-retry-prompt
description:
  Prompt for the notify-retry agent. Analyzes historical retry/error logs and recommends optimized exponential backoff parameters per channel.
---

### Analysis Checklist

1.  **Failure Pattern Detection:** Group records by `channel` and `last_error_code`. Identify which error codes dominate per channel (e.g., 429 Rate Limit, 503 Service Unavailable, 401 Auth Failure). Flag channels where a single error code accounts for >50% of failures.

2.  **Time-to-Success Calculation:** For each channel, compute:
    - Average retry count before success
    - Average total wall-clock time from first attempt to success
    - Median time-to-success (less sensitive to outliers)
    - P90 and P99 tail latencies

3.  **Parameter Recommendation:** Based on the patterns, suggest exponential backoff parameters:
    - `initial_delay`: if most failures are rate limits (429), start higher (5-10s); if transient (503), start lower (1-2s)
    - `multiplier`: aggressive for rate-limited channels (2.0-3.0), conservative for auth failures (1.0-1.5)
    - `max_retries`: derived from the observed retry count distribution — set just above P90 to avoid wasted attempts
    - `max_delay`: optional ceiling to cap backoff (e.g., 300s)

### Constraints

- Read-only analysis — do not modify any source files
- All recommendations must cite supporting evidence from the log data
- Logs may be pasted inline or attached as a file

### Success Criteria

- Outputs a JSON report with per-channel analysis and recommended config
- Each recommendation includes a brief rationale citing log evidence
- The config snippet is immediately copyable into `app/config.py` or a JSON config file
- Recommendations reference the existing `RETRY_DELAYS` and `max_retry_attempts` values as baselines

### Usage Template

```
Analyze the following retry logs and suggest optimized exponential backoff parameters for each channel.

Log data:
[CSV or JSON data]

Output:
1. Per-channel failure pattern summary
2. Per-channel time-to-success metrics
3. Suggested config.json snippet with initial_delay, multiplier, max_retries
4. Brief rationale for each recommendation

Do not apply any changes to the codebase — output only analysis and recommendations.
```
