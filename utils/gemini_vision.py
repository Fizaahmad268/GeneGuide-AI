import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def explain_image(uploaded_image, language="English"):

    image = Image.open(uploaded_image)

    # Language instruction
    if language == "Urdu":
        lang_instruction = """
Write the ENTIRE response in simple Urdu using the Urdu script (not Roman Urdu).
Use easy words that an ordinary patient can understand.
"""
    else:
        lang_instruction = """
Write the ENTIRE response in simple English.
"""

    prompt = f"""
You are GeneGuide AI, an AI assistant that explains medical reports.

{lang_instruction}

The uploaded image is a medical report.

Your goal is to reduce fear and confusion for patients and their families.

IMPORTANT RULES:

- Read every visible part of the report carefully.
- Use very simple language.
- Never use unnecessary medical jargon.
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

Write ONLY one short paragraph reminding the user that this explanation is educational and does not replace professional medical advice.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(e)
        raise
    