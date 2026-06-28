<div align="center">

# OpenDeep [v0.9]

### Unofficial Python Client for DeepSeek API

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.9.0-orange.svg)](https://github.com/yourusername/opendeep)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Access DeepSeek's powerful AI models with a clean, Pythonic interface — no official API key required.**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Examples](#-examples)

</div>

---

## Overview

**OpenDeep** is a lightweight, unofficial Python library that provides programmatic access to DeepSeek's AI models by reverse-engineering the `chat.deepseek.com` web interface. It offers a simple, intuitive API inspired by Google's Generative AI SDK.

### Why OpenDeep?

- **No API Key Required** — Uses your existing DeepSeek web account token
- **Full Feature Parity** — Access all models including Pro, Flash, Reasoner, and Expert
- **Thinking Mode** — Enable DeepThink reasoning for complex problems
- **Web Search** — Integrated search capabilities (Flash model)
- **Streaming Support** — Real-time response streaming with colored reasoning output
- **Async Ready** — Full async/await support for modern applications
- **Cloudflare Bypass** — Optional `curl_cffi` integration for reliable access

---

## Features

### Supported Models

| Model | Description | Thinking | Search | Best For |
|-------|-------------|----------|--------|----------|
| `deepseek-v4-pro` | Latest flagship model | Default | No | Complex reasoning, coding, analysis |
| `deepseek-v4-flash` | Fast & efficient | Optional | Yes | Quick responses, web search tasks |
| `deepseek-chat` | General purpose | Optional | No | Everyday conversations |
| `deepseek-reasoner` | Reasoning-focused | Default | No | Math, logic, step-by-step problems |
| `deepseek-expert` | Expert mode | Optional | No | Specialized tasks |

### Core Capabilities

- **Single-turn Completions** — Quick question-answer interactions
- **Multi-turn Conversations** — Maintain context across multiple messages
- **Streaming Output** — Watch responses generate in real-time
- **Thinking Visualization** — See the model's reasoning process (gray text)
- **Proof of Work** — Automatic challenge solving for API access
- **Session Management** — Automatic chat session handling

---

## Installation

### Basic Installation

```bash
pip install opendeep
```

### With Cloudflare Bypass (Recommended)

```bash
pip install opendeep[cf]
```

This installs `curl_cffi` which provides TLS fingerprinting to bypass Cloudflare protection.

### From Source

```bash
git clone https://github.com/yourusername/opendeep.git
cd opendeep
pip install -e .
```

### Requirements

- Python 3.10+
- `curl_cffi>=0.7.0` (recommended)
- `requests>=2.31.0`
- `wasmtime>=18.0.0`
- `numpy>=1.26.0`

---

## Quick Start

### 1. Get Your API Token

1. Visit [chat.deepseek.com](https://chat.deepseek.com)
2. Log in to your account
3. Open browser DevTools (F12)
4. Go to **Application** → **Local Storage** → `https://chat.deepseek.com`
5. Find the `userToken` value
6. Copy the token value

### 2. Configure and Use

```python
import opendeep

# Configure with your token
opendeep.configure(api_key="your_token_here")

# Create a model
from opendeep import GenerativeModel
model = GenerativeModel("deepseek-v4-pro")

# Generate content
response = model.generate_content("Explain quantum computing in simple terms")
print(response.text)
```

---

## Documentation

### Configuration

```python
import opendeep

opendeep.configure(
    api_key="your_token",              # Required: userToken from localStorage
    base_url="https://chat.deepseek.com/api/v0",  # Optional: custom endpoint
    user_agent="Custom Agent/1.0"      # Optional: custom user agent
)
```

### Synchronous API

#### Single-turn Completion

```python
from opendeep import GenerativeModel

model = GenerativeModel("deepseek-v4-pro")
response = model.generate_content("What is the meaning of life?")
print(response.text)
```

#### Multi-turn Conversation

```python
from opendeep import GenerativeModel

model = GenerativeModel("deepseek-v4-pro")
chat = model.start_chat(thinking_enabled=True)

# First message
response1 = chat.send_message("What is Python?")
print(response1.text)

# Follow-up (context is maintained)
response2 = chat.send_message("How do I install it?")
print(response2.text)

# Another follow-up
response3 = chat.send_message("Show me a hello world example")
print(response3.text)
```

#### Streaming Output

```python
from opendeep import GenerativeModel

model = GenerativeModel("deepseek-v4-pro")

# Stream output to console with colored reasoning
model.generate_content(
    "Write a poem about artificial intelligence",
    stream=True,
    thinking_enabled=True
)
```

#### Web Search (Flash Model Only)

```python
from opendeep import GenerativeModel

model = GenerativeModel("deepseek-v4-flash")
response = model.generate_content(
    "What are the latest developments in AI?",
    search_enabled=True
)
print(response.text)
```

### Asynchronous API

#### Basic Async Usage

```python
import asyncio
from opendeep import AsyncGenerativeModel

async def main():
    model = AsyncGenerativeModel("deepseek-v4-pro")
    response = await model.generate_content("Hello, DeepSeek!")
    print(response.text)

asyncio.run(main())
```

#### Async Multi-turn Conversation

```python
import asyncio
from opendeep import AsyncGenerativeModel

async def main():
    model = AsyncGenerativeModel("deepseek-v4-pro")
    chat = model.start_chat(thinking_enabled=True)
    
    response1 = await chat.send_message("What is machine learning?")
    print(response1.text)
    
    response2 = await chat.send_message("Give me an example")
    print(response2.text)

asyncio.run(main())
```

#### Concurrent Requests

```python
import asyncio
from opendeep import AsyncGenerativeModel

async def main():
    model = AsyncGenerativeModel("deepseek-v4-pro")
    
    # Run multiple requests concurrently
    tasks = [
        model.generate_content("Question 1"),
        model.generate_content("Question 2"),
        model.generate_content("Question 3"),
    ]
    
    responses = await asyncio.gather(*tasks)
    for i, response in enumerate(responses, 1):
        print(f"Response {i}: {response.text[:100]}...")

asyncio.run(main())
```

### Advanced Options

#### Thinking Mode

Enable DeepThink reasoning for complex problems:

```python
# Thinking is enabled by default for Pro and Reasoner models
model = GenerativeModel("deepseek-v4-pro")  # thinking_enabled=True by default

# Explicitly enable/disable
response = model.generate_content(
    "Solve this math problem: ...",
    thinking_enabled=True  # or False to disable
)
```

#### Model Selection

```python
from opendeep import GenerativeModel

# Pro model (best quality, slower)
pro_model = GenerativeModel("deepseek-v4-pro")

# Flash model (fast, supports search)
flash_model = GenerativeModel("deepseek-v4-flash")

# Reasoner model (optimized for reasoning tasks)
reasoner_model = GenerativeModel("deepseek-reasoner")

# Expert model (specialized)
expert_model = GenerativeModel("deepseek-expert")
```

---

## Examples

### Code Generation

```python
from opendeep import GenerativeModel

model = GenerativeModel("deepseek-v4-pro")

prompt = """
Write a Python function that:
1. Takes a list of numbers
2. Returns the moving average with window size 3
3. Includes type hints and docstring
"""

response = model.generate_content(prompt, thinking_enabled=True)
print(response.text)
```

### Data Analysis

```python
from opendeep import GenerativeModel

model = GenerativeModel("deepseek-v4-pro")

data = """
Sales data for Q1 2024:
- January: $45,000
- February: $52,000
- March: $48,000
"""

response = model.generate_content(
    f"Analyze this sales data and provide insights:\n{data}",
    thinking_enabled=True
)
print(response.text)
```

### Web Search Integration

```python
from opendeep import GenerativeModel

model = GenerativeModel("deepseek-v4-flash")

response = model.generate_content(
    "What are the top 5 programming languages in 2024?",
    search_enabled=True
)
print(response.text)
```

### Streaming with Progress

```python
from opendeep import GenerativeModel

model = GenerativeModel("deepseek-v4-pro")

print("Generating response...")
print("-" * 50)

# Stream shows reasoning in gray, then final response
model.generate_content(
    "Explain the theory of relativity",
    stream=True,
    thinking_enabled=True
)

print("-" * 50)
print("Done!")
```

---

## Architecture

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                         User Code                           │
│  model.generate_content("Hello")                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      GenerativeModel                        │
│  - Manages HTTP sessions                                    │
│  - Handles authentication                                   │
│  - Coordinates request/response                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        ChatSession                          │
│  - Creates chat session                                     │
│  - Manages conversation context                             │
│  - Handles multi-turn interactions                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Proof of Work                          │
│  - Requests POW challenge from API                          │
│  - Solves challenge using WebAssembly                       │
│  - Adds solution to request headers                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DeepSeek API                           │
│  POST /chat/completion                                      │
│  - SSE streaming response                                   │
│  - Thinking + content chunks                                │
└─────────────────────────────────────────────────────────────┘
```

### Proof of Work (POW)

DeepSeek uses a Proof of Work mechanism to prevent abuse. OpenDeep solves these challenges automatically using a WebAssembly module compiled from Rust. The POW solver:

1. Receives a challenge from the API
2. Computes a valid hash using the WASM module
3. Includes the solution in the `x-ds-pow-response` header

This happens transparently — you don't need to handle it manually.

---

## Troubleshooting

### Cloudflare Protection

If you encounter Cloudflare blocks:

```bash
# Install with curl_cffi
pip install opendeep[cf]
```

The `curl_cffi` library provides TLS fingerprinting that mimics Chrome 120, bypassing most Cloudflare protections.

### Invalid Token

If you get authentication errors:

1. Re-login to [chat.deepseek.com](https://chat.deepseek.com)
2. Refresh the page
3. Get a fresh `userToken` from localStorage
4. Update your configuration

### Rate Limiting

DeepSeek may rate limit requests. If you encounter this:

- Add delays between requests
- Reduce concurrent requests
- Wait a few minutes before retrying

### Missing Dependencies

If you see import errors:

```bash
# Install all dependencies
pip install curl_cffi requests wasmtime numpy
```

---

## Security Considerations

### API Token Security

- **Never commit tokens to version control**
- Use environment variables in production:

```python
import os
import opendeep

token = os.environ.get("DEEPSEEK_TOKEN")
if not token:
    raise ValueError("DEEPSEEK_TOKEN environment variable not set")

opendeep.configure(api_key=token)
```

### Token Rotation

- Tokens may expire or be invalidated
- Re-login to get a fresh token if requests fail
- Consider implementing automatic token refresh

---

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/opendeep.git
cd opendeep

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install dev dependencies
pip install pytest pytest-asyncio ruff pyright
```

### Code Quality

```bash
# Format code
ruff format opendeep/

# Lint code
ruff check opendeep/ --select ALL --ignore ANN401,D203,D213 --fix

# Type check
pyright opendeep/

# Run tests
pytest tests/ -v
```

---

## Limitations

- **Unofficial API** — This library reverse-engineers the web interface; it may break if DeepSeek changes their API
- **No Official Support** — Use at your own risk
- **Rate Limits** — Subject to DeepSeek's rate limiting
- **Token Expiry** — Web tokens may expire and need refresh

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This is an **unofficial** library and is not affiliated with, endorsed by, or supported by DeepSeek. Use responsibly and in accordance with DeepSeek's terms of service.

---

<div align="center">

**made with hate to corps by @cmpdchtr**

[Report Bug](https://github.com/yourusername/opendeep/issues) • [Request Feature](https://github.com/yourusername/opendeep/issues)

</div>
