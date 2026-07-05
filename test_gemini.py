import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

print("Loaded key:", key[:10] + "..." if key else "No key found")

genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-2.5-flash")

try:
    response = model.generate_content("Hello!")
    print("SUCCESS!")
    print(response.text)

except Exception as e:
    print("ERROR:")
    print(e)