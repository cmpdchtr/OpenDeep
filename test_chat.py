import opendeep as genai

genai.configure(api_key="e4cXpEk+LuEHkOGk9qOE5ehuZWesWY02LHtcoVHfrEwVFjrmgysf+BMwg142/aBH")
model = genai.GenerativeModel("deepseek-v4-flash")
print("Starting Chat...")
chat = model.start_chat()
response = chat.send_message("My name is John. Can you remember it?", stream=False)
print("Bot:", response.text)

print("Sending second message...")
response2 = chat.send_message("What is my name?", stream=False)
print("Bot:", response2.text)
