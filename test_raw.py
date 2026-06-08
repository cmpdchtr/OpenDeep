import opendeep as genai

genai.configure(api_key="e4cXpEk+LuEHkOGk9qOE5ehuZWesWY02LHtcoVHfrEwVFjrmgysf+BMwg142/aBH")
model = genai.GenerativeModel("deepseek-v4-flash")
print("Generating content...")
response = model.generate_content("Hi", stream=True)
print(f"Done. Final: {response.text}")
