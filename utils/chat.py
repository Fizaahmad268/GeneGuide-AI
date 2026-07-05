import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model=genai.GenerativeModel("gemini-2.5-flash")

def chat_with_report(report,question):

    prompt=f"""
You are GeneGuide AI.

Medical report:

{report}

Patient asks:

{question}

Reply in simple language.

Do NOT diagnose.

Do NOT prescribe medicines.

Maximum 150 words.
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
    