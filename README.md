# OpenDeep 🐋

**OpenDeep** is an elegant, free, and unofficial Python client for the DeepSeek API. It provides a clean, Google Gemini-like syntax while seamlessly handling DeepSeek's underlying security mechanisms (Cloudflare bypass, Proof of Work challenges, and Server-Sent Events). 

Whether you need quick text generation or complex reasoning from the DeepSeek V4 Pro model, OpenDeep abstracts away the messy backend logic so you can focus on building.

## ✨ Key Features

- 💎 **Gemini-Like Syntax:** Familiar and highly readable API design (`model.generate_content`).
- 🔄 **Multi-Turn Chat History:** Seamlessly remember context with `ChatSession`.
- ⚡ **Asynchronous Client:** Full async support for high-performance applications.
- 🔍 **Web Search:** Native support for DeepSeek's web search capabilities (Instant model).
- 🧠 **Thinking Support (DeepThink):** Captures and streams the reasoning process of advanced models (V4 Pro, Reasoner).
- 🛡️ **Cloudflare & POW Bypass:** Uses `curl_cffi` and WebAssembly to automatically solve browser challenges.

## 📦 Installation

Ensure you have Python 3.8+ installed. You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Get your API Key (User Token)
To use OpenDeep, you need your active session token from the browser:
1. Log into [chat.deepseek.com](https://chat.deepseek.com/).
2. Open your browser's Developer Tools (F12).
3. **Option A:** Go to Application (or Storage) -> Local Storage -> find the key named `userToken` and copy its value.
4. **Option B:** Go to the Console tab and run: `JSON.parse(localStorage.getItem("userToken")).value`

### 2. Basic Usage
```python
import opendeep as genai

genai.configure(api_key="your_userToken_here")
model = genai.GenerativeModel("deepseek-v4-flash")

response = model.generate_content("Explain the theory of relativity in simple terms.")
print(response.text)
```

### 3. Multi-Turn Chat (ChatSession)
Maintain context across multiple messages.
```python
import opendeep as genai

genai.configure(api_key="your_userToken_here")
model = genai.GenerativeModel("deepseek-v4-flash")
chat = model.start_chat()

response = chat.send_message("My name is John.")
print("Bot:", response.text)

response = chat.send_message("What is my name?")
print("Bot:", response.text)
```

### 4. DeepThink & Web Search
You can explicitly enable reasoning (for complex math/logic) and web search (for real-time data).
```python
import opendeep as genai

genai.configure(api_key="your_userToken_here")
model = genai.GenerativeModel("deepseek-v4-flash")

# Web Search
response = model.generate_content("What is the weather in Tokyo today?", search_enabled=True)
print(response.text)

# DeepThink (Streaming)
response = model.generate_content("Solve 2 + 2 * 2", thinking_enabled=True, stream=True)
```

### 5. Vision Support (DeepSeek-Vision)
Upload images and ask questions about them.
```python
import opendeep as genai

genai.configure(api_key="your_userToken_here")
model = genai.GenerativeModel("deepseek-vision")

# 1. Upload the image
file_id = model.upload_file("path/to/your/image.jpg")

# 2. Ask a question about it
response = model.generate_content("What is in this image?", file_ids=[file_id])
print(response.text)
```

### 6. Asynchronous Client
For FastAPI, Telegram bots, or Discord integrations, use the non-blocking Async client.
```python
import asyncio
import opendeep as genai

genai.configure(api_key="your_userToken_here")

async def main():
    model = genai.AsyncGenerativeModel("deepseek-v4-pro")
    chat = model.start_chat()
    
    response = await chat.send_message("Write a short poem.", stream=False)
    print(response.text)

asyncio.run(main())
```

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