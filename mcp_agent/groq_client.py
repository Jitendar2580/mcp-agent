# groq_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)