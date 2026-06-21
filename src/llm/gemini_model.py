from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():

    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    return client