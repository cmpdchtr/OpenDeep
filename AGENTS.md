# OpenDeep Agent Guidelines

This file provides high-signal context, conventions, and architectural details for AI agents working in this repository. `opendeep` is a lightweight, unofficial Python library providing free access to DeepSeek models by reverse-engineering the `chat.deepseek.com` API.

## Project Goal
- Provide a 1:1 public API match with the official `google-genai` SDK (`Client`, `client.models`, `client.chats`, and `client.aio` namespaces).
- Ensure an extremely low footprint: minimal memory buffering, connection pooling, strict type checking, and clean exception handling.

## Commands

- **Setup**: `python -m venv venv && source venv/bin/activate && pip install -e ".[cf]" pytest pytest-asyncio ruff pyright`
- **Tests**: `pytest tests/ -v` (Tests run against a mocked HTTPX transport in `tests/conftest.py`. They do not hit the live API).
- **Formatting**: `ruff format opendeep/ tests/`
- **Linting**: `ruff check opendeep/ tests/ --select ALL --ignore ANN401,D203,D213 --fix`
- **Type Checking**: `pyright opendeep/` (Strict mode is enforced in `pyproject.toml`). All code must pass `pyright` cleanly.

## Architecture & Internals

### Package Layout
- **Public API** (`opendeep/client.py`, `opendeep/types.py`): Mirrors `google.genai` perfectly. `Client` exposes `.models`, `.chats`, and `.aio` via lazy descriptors to ensure zero initialization cost until first access.
- **Internal Layer** (`opendeep/_internal/`): All implementation details (HTTP transport, payloads, streaming, authentication) are isolated here to keep the public namespace absolutely clean.

### Core Components
- **Models Map** (`constants.py`): Maps user aliases to internal DeepSeek IDs.
  - `"deepseek-instant"` -> `deepseek_v3`
  - `"deepseek-expert"`  -> `deepseek_r1`
- **Dual Transport (`_HttpxTransport`)**: Defaults to `httpx` (HTTP/2 enabled, connection pooled). If a user provides `Client(bypass=True)`, it lazily imports and seamlessly swaps internal engines to `curl_cffi` to bypass Cloudflare TLS fingerprinting.
  - *Never* import `curl_cffi` at the top level. It is an optional dependency (`opendeep[cf]`).
  - Keep exactly one sync client and one async client per `Client` instance. Do not create new clients per request.
- **Payload & Serialization (`payload.py`)**: Responsible for normalizing inputs (string, lists, `Part`, `Content`) into a strict `list[Content]` format and translating Pydantic models into DeepSeek's JSON schema.
- **Streaming (`stream.py`)**: `_SseParser` handles Server-Sent Events natively. It distinguishes between `'thinking'` and `'text'` chunks, filters empty deltas, and handles the `[DONE]` sentinel. It must remain O(1) in memory (no full response buffering).

### Sync/Async Parity
- The library fully supports synchronous (`client.models`) and asynchronous (`client.aio.models`) workflows.
- **CRITICAL**: Do *not* duplicate payload building or parsing logic between sync and async paths. Use the same shared logic in `payload.py` and `stream.py`; only the transport layer invocation should differ (`client.stream` vs `client.astream`).
- `generate_content()` MUST internally delegate to `generate_content_stream()` and accumulate the result, ensuring a single source of truth for request execution.

### Types & Data Models (`types.py`)
- All models use `pydantic` v2 with `model_config = ConfigDict(frozen=True)` to enforce immutability.
- `GenerateContentConfig`: Central configuration exposing `deep_think` (bool) and `search` (bool). `search` is strictly validated and only allowed on `deepseek-instant`.

### Error Handling & Auth (`exceptions.py` & `auth.py`)
- Always raise typed exceptions from `opendeep.exceptions` (e.g., `AuthenticationError`, `RateLimitError`, `CloudflareError`, `APIError`). Do not raise bare standard exceptions like `Exception` or `RuntimeError`.
- Auth tokens are picked up from the `DEEPSEEK_TOKEN` environment variable or passed directly.
- The token is immediately validated on `Client` initialization via a lightweight API request (usually `/chat_session/create`) to fail fast.
- If a Cloudflare 403 is hit and `bypass` is not enabled, raise a `CloudflareError` combined with a `RuntimeWarning` advising the user to install `opendeep[cf]` and enable the flag.

## Agent Workflow Conventions
1. When asked to fix bugs, always refer to the test suite (`pytest tests/`) first.
2. If tests are failing due to HTTP mocking issues, adjust `MockClient` and `MockAsyncClient` in `tests/conftest.py`.
3. Do not modify the public signature of classes unless instructed to match a change in `google-genai`.
4. Ensure 0 type errors via `pyright opendeep/` after every code change.
