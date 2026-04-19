# OpenDeep 🚀

**OpenDeep** is an elegant, free, and unofficial Python client for the DeepSeek API. It provides a clean, Google Gemini-like syntax while seamlessly handling DeepSeek's underlying security mechanisms (Cloudflare bypass, Proof of Work challenges, and Server-Sent Events). 

Whether you need quick text generation or complex reasoning from the R1 model, OpenDeep abstracts away the messy backend logic so you can focus on building.

## ✨ Key Features

- 💎 **Gemini-Like Syntax:** Familiar and highly readable API design (`model.generate_content`).
- 🛡️ **Cloudflare Bypass:** Uses `curl_cffi` to impersonate browser TLS fingerprints, preventing blocking.
- 🧩 **Native POW Solver:** WebAssembly-powered challenge solver to effortlessly bypass DeepSeek's rate-limiting/bot protection.
- 📡 **Real-Time Streaming:** Full support for Server-Sent Events (SSE) parsing, including the newest DeepSeek patch formats.
- 🧠 **Reasoner Support (DeepSeek-R1):** Seamlessly handles the "thinking" process of the reasoner model.

## 📦 Installation

Ensure you have Python 3.8+ installed. You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Get your API Key (User Token)
To use OpenDeep, you need your active session token from the browser:
1. Log into [chat.deepseek.com](https://chat.deepseek.com/).
2. Open your browser's Developer Tools (F12) -> Application (or Storage) -> Local Storage.
3. Find the key named `userToken` and copy its value.

### 2. Basic Usage (Without Streaming)
If you just want the final answer without any real-time console output or "thinking" logs, set `stream=False` (this is the default behavior).

```python
import opendeep as genai

genai.configure(api_key="your_userToken_here")
model = genai.GenerativeModel("deepseek-chat") # V3 model

# Waits for the full generation to complete
response = model.generate_content("Explain the theory of relativity in simple terms.")

print("Final Output:")
print(response.text)
```

### 3. Real-Time Streaming & Reasoner Output
When using the `deepseek-reasoner` (R1) model with `stream=True`, OpenDeep will stream the internal "thinking" process directly to your console in a subtle gray color, followed by the actual answer.

```python
import opendeep as genai

genai.configure(api_key="your_userToken_here")

# Select the reasoning model (R1)
model = genai.GenerativeModel("deepseek-reasoner")

# stream=True enables real-time console output
# It will print the reasoning process (in gray) and then the final answer!
response = model.generate_content("How many R's are in the word strawberry?", stream=True)

# The response object still captures the final text (excluding the thinking process)
print(f"\nCaptured text length: {len(response.text)} characters")
```

**💡 Note on Reasoner and Streams:**
- If you use `deepseek-reasoner` with `stream=True`, you will **see** the thoughts live in the console.
- If you use `deepseek-reasoner` with `stream=False`, the thoughts are **silently discarded** during processing, and you only get the final, clean answer in `response.text`.

## 🏗️ Architecture Under the Hood

- **`models.py`:** Handles the HTTP session, impersonation, header generation, stream decoding, and payload construction.
- **`pow.py`:** A highly optimized WebAssembly (WASM) bridge that calculates Custom SHA3 hashes for DeepSeek's Proof of Work challenge.
- **`config.py`:** Global state management for authentication and endpoints.

## 🛠️ Troubleshooting

- **`422 Unprocessable Entity`**: This usually means your `userToken` is invalid or expired. Get a fresh one from your browser.
- **`Cloudflare / Empty Response`**: Ensure `curl_cffi` is properly installed. Standard `requests` will get blocked by Cloudflare.
- **`WASM errors`**: Make sure both `wasmtime` and `numpy` are installed to solve the Proof of Work challenges.

## 📜 Disclaimer

This is an unofficial, reverse-engineered client intended for educational purposes and personal use. DeepSeek may update their internal APIs or protection mechanisms at any time. Use responsibly!

---
*made with hate to corps by @cmpdchtr*