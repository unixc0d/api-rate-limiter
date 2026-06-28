# API Rate Limiter

A production-ready asynchronous Python rate limiter implementing the Token Bucket algorithm to protect sensitive API endpoints from DDoS, automation boți, and brute-force attacks.

## Features
- **Token Bucket Architecture**: Precise calculation of traffic allowances based on time elapsed.
- **Asynchronous Execution**: Native integration with `asyncio` workflows for non-blocking network environments.
- **Zero Dependencies**: Developed strictly using Python standard libraries (`asyncio`, `time`, `logging`).

## How to Run

### 1. Execution
Execute the rate limiting script directly via the CLI:
```bash
python rate_limiter.py
```

### 2. Expected Traffic Audit Trail
When running the simulation, the engine logs instant security grants and blocks based on available request tokens:
```text
2026-06-29 02:22:00 [INFO] Access GRANTED for 192.168.43.10. Remaining security tokens: 2
2026-06-29 02:22:00 [INFO] Access GRANTED for 192.168.43.10. Remaining security tokens: 1
2026-06-29 02:22:00 [INFO] Access GRANTED for 192.168.43.10. Remaining security tokens: 0
2026-06-29 02:22:00 [WARNING] Access DENIED for 192.168.43.10. Rate limit threshold breached.
```
