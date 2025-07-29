# tools.py
import re
from .groq_client import client
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os 
import markdown2
import asyncpg
 

load_dotenv()

FROM=os.getenv("FROM")
APP_PASSWORD=os.getenv("APP_PASSWORD")
HOST_NAME=os.getenv("HOST_NAME")
PORT=os.getenv("PORT") 



POSTGRES_APP_USER=os.getenv("POSTGRES_APP_USER")
POSTGRES_APP_PASSWORD=os.getenv("POSTGRES_APP_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB")
DB_HOST=os.getenv("DB_HOST")  
 
 
 
DB_CONFIG = {
    "user": POSTGRES_APP_USER,
    "password": POSTGRES_APP_PASSWORD,
    "database": POSTGRES_DB,
    "host": DB_HOST,
    "port": 5432
}
 

def mathematics_calculation(query: str) -> str:
    system_prompt = (
        "You are an educational expert AI assistant that can explain any topic across all education sectors. "
        "This includes science, mathematics, technology, programming, arts, language, finance, history, geography, careers, and more.\n\n"
        "Your responses should:\n"
        "- Give a detailed, structured explanation of the topic\n"
        "- Use simple, clear language\n"
        "- Include examples if possible\n"
        "- Format with bullets, headers, or emojis for better readability\n"
        "- Avoid overly technical jargon unless necessary"
    )

    user_prompt = f"Solve this math problem and explain: {query}"

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, there was an error solving the math problem: {e}"


def education(query: str) -> str:
    system_prompt = (
        "You are an educational expert AI assistant that can explain any topic across all education sectors. "
        "This includes science, mathematics, technology, programming, arts, language, finance, history, geography, careers, and more.\n\n"
        "Your responses should:\n"
        "- Give a detailed, structured explanation of the topic\n"
        "- Use simple, clear language\n"
        "- Include examples if possible\n"
        "- Format with bullets, headers, or emojis for better readability\n"
        "- Avoid overly technical jargon unless necessary"
    )

    user_prompt = f"Explain this topic to me in detail like a professional educator: {query}"

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, there was an error generating the educational content: {e}"


def extract_destination(text: str) -> str:
    """Basic function to extract destination from user query."""
    match = re.search(
        r"trip\s*(?:plan)?\s*(?:to|for|in)?\s*(.+)", text, re.IGNORECASE)
    return match.group(1).strip() if match else text.strip()


def trip_plan(query: str) -> str:
    destination = extract_destination(query)

    system_prompt = (
        "You are a travel assistant. When given a destination, respond with a 3-day detailed travel plan, "
        "including sightseeing spots, cultural experiences, food suggestions, and travel tips. "
        "Make the plan engaging and use emojis and formatting for readability.\n\n"
        "Make sure it feels like a local guide prepared it!"
    )

    user_prompt = f"Plan a detailed 3-day itinerary for a trip to {destination}. Include famous spots, food, and shopping."

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, there was an error generating the trip plan: {e}"


def extract_location(text: str) -> str:
    match = re.search(r"(?:weather\s+(?:in|for|at)\s+)(.+)",
                      text, re.IGNORECASE)
    return match.group(1).strip() if match else text.strip()


def weather_details(query: str) -> str:
    location = extract_location(query)

    system_prompt = (
        "You are a weather assistant. When given a city or place, provide a detailed weather report "
        "including current temperature, condition (sunny, cloudy, rainy, etc.), and helpful tips like what to wear, "
        "safety precautions, and how it might affect travel or outdoor plans. Format it nicely with emojis."
    )

    user_prompt = f"What's the weather like in {location} today? Provide a detailed and friendly report."

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, there was an error generating the weather details: {e}"


async def send_email(subject: str, body: str, to_email: str):
    name_match = re.match(r"([^@]+)", to_email)
    user_name = name_match.group(1).replace('.', ' ').replace('_', ' ').title() if name_match else "User"

    personalized_body = body.replace("[Your Name]", user_name)

    html_content = markdown2.markdown(personalized_body)

    msg = EmailMessage()
    msg["From"] = FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(personalized_body)
    msg.add_alternative(html_content, subtype="html")

    await aiosmtplib.send(
        msg,
        hostname=HOST_NAME,
        port=PORT,
        username=FROM,
        password=APP_PASSWORD, 
        start_tls=True,
    )
