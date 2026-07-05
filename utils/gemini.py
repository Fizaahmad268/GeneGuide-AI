import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print("Loaded Key:", key[:15] + "...")

genai.configure(api_key=key)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def explain_report(report_text, language="English"):

    lang_instruction = ""
    if language == "Urdu":
        lang_instruction = """
Write the ENTIRE response in simple Urdu using the Urdu script (اردو), not Roman Urdu.
Use easy words that an ordinary patient and their family can understand.
"""
    else:
        lang_instruction = """
Write the ENTIRE response in simple English.
Use easy words that an ordinary patient and their family can understand.
"""

    prompt = f"""
You are GeneGuide AI, an AI assistant that explains medical reports.

{lang_instruction}

IMPORTANT RULES:

- Explain everything in patient-friendly language.
- Use very simple words.
- Never diagnose.
- Never recommend treatment.
- Never replace a doctor's advice.
- Be empathetic but do not provide false reassurance.

Return EXACTLY in this format.

## HEALTH SNAPSHOT

Patient:
Age:
Gender:
Report Type:
Affected Organ:
Diagnosis:
Risk Level:
## HEALTH SNAPSHOT

Diagnosis:
Severity:
Body Part:
Report Type:
Urgency:
## HEALTH SNAPSHOT

Patient Name:
Age:
Body Part:
Diagnosis:
Severity:
Report Type:
Urgency:

## SUMMARY

...

## MEDICAL TERMS

...

## QUESTIONS FOR THE DOCTOR

...

## NEXT STEPS

...

## DISCLAIMER

...

Medical Report:
{report_text}
"""

    
    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(e)
        raise
    