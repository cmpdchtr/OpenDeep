import opendeep as genai

# 1. Configure the API key
# Retrieve your `userToken` from the localStorage on chat.deepseek.com
genai.configure(api_key="your_userToken_here")

# 2. Select the target model ('deepseek-chat' or 'deepseek-reasoner')
model = genai.GenerativeModel("deepseek-reasoner")

print("Sending request to DeepSeek...\n")

try:
    # 3. Generate content with streaming enabled
    response = model.generate_content("Explain the theory of relativity in simple terms.", stream=True)
    
    print("\n\nResponse complete.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
