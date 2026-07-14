import os

from dotenv import load_dotenv
from google import genai
import traceback



client = genai.Client(
    
)


def generate_embedding(text):

    try:
       
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values
    
    except Exception:
        traceback.print_exc()
        raise