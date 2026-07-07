import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)



def parse_resume(resume_text):

    prompt = f"""
            You are a resume parsing AI.

            Extract the candidate information from the resume below.

            Return ONLY valid JSON.
            Do not include markdown or explanations.

            The JSON format must be:

            {{
                "skills": [],
                "education": [],
                "experience": []
            }}

            Resume:
            {resume_text}
            """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    result = response.text.strip()

    # Remove markdown formatting if Gemini adds it

    if result.startswith("```json"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    return json.loads(result)