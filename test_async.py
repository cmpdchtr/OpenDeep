import asyncio
import opendeep as genai

genai.configure(api_key="e4cXpEk+LuEHkOGk9qOE5ehuZWesWY02LHtcoVHfrEwVFjrmgysf+BMwg142/aBH")

async def main():
    print("Starting Async Chat...")
    model = genai.AsyncGenerativeModel("deepseek-v4-flash")
    chat = model.start_chat()
    
    response = await chat.send_message("What is 2+2?", stream=False)
    print("Bot:", response.text)
    
    response2 = await chat.send_message("What was my previous question?", stream=False)
    print("Bot:", response2.text)

asyncio.run(main())
