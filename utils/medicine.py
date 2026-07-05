import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model=genai.GenerativeModel("gemini-2.5-flash")

def explain_medicine(name):

    prompt=f"""
Explain this medicine in simple language.

Medicine:

{name}

Return

Purpose

How it works

Common side effects

Important precautions

Never prescribe.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return """
⚠️ GeneGuide AI Chat is temporarily unavailable.

The AI service has reached its free usage limit.

Please try again in a minute.

Your medical report explanation above is still available.
"""