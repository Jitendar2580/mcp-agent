# agent.py
from .tools import mathematics_calculation, weather_details, education, trip_plan ,send_email ,sql_query
from .groq_client import client 


# Memory store for the conversation (you can later switch to Redis, DB, or per-user memory)
conversation_history = []

async def ask_agent(question: str) -> str:
    global conversation_history

    system_prompt = """
        You are a helpful AI assistant designed to respond using specialized tools only, except for greetings.
        
        You MUST decide which tool to invoke based on the user's question. Choose only one tool per question unless explicitly asked to do multiple things.
        
        ✅ You can respond to basic greetings like "hi", "hello", or "how are you?" with a short, friendly message.
        
        🏁 Your Task:

            When a user sends a message, analyze the intent. Then:

            1. Identify which tool (if any) fits the request.
            2. Call the tool with the right argument.
            3. Return the result to the user clearly.

        If the question is vague, ask the user for clarification.

        Never guess a result — always rely on the correct tool output.
        
    """

    if not conversation_history:
        conversation_history.append({"role": "system", "content": system_prompt})

    conversation_history.append({"role": "user", "content": question})
 
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=conversation_history
    )

    reply = chat_completion.choices[0].message.content.strip()
 
    conversation_history.append({"role": "assistant", "content": reply})
    result = ""

    if "math" in question.lower() or "calculate" in question.lower():
        print("Caclulation Tool Triggered----------------------->")
        result = mathematics_calculation(question)
    elif "weather" in question.lower():
        print("Weather Tool Triggered----------------------->")
        result = weather_details(question)
    elif "trip" in question.lower() or "plan" in question.lower():
        print("Trip Tool Triggered----------------------->")
        result = trip_plan(question) 
    elif "explain" in question.lower() or "learn" in question.lower():
        print("Education Tool Triggered----------------------->")
        result = education(question)
    elif "select" in question.lower() or "insert" in question.lower() or "update" in question.lower():
        print("Sql Query Tool Triggered----------------------->")
        result = await sql_query(question)
    if not result:
        result = reply
         
    last_result = result

    # -------------------- Detect send email intent --------------------
    if "send on email" in question.lower() or "email this" in question.lower() or "send via email" in question.lower():
        print("Email Tool Triggered----------------------->")
        await send_email(
            subject="📧 Requested Info from AI Assistant",
            body=last_result,
            to_email="jitendra@amplework.com"  
        )
        result += "\n\n✅ Trip plan has been sent to your email."
    if result != reply:
        conversation_history.append({"role": "assistant", "content": result})

    return result



 
# async def ask_agent(question: str) -> str:
#     system_prompt = """You are a helpful AI assistant with access to the following four specialized tools.

#             You MUST decide which tool to invoke based on the user's question. Choose only one tool per question unless explicitly asked to do multiple things.

#             Each tool is described below. Think carefully before calling a tool. Always return the result from the tool.

#             ---

#             🔢 Tool Name: mathematics_calculation(query: str)

#             - Purpose: Perform basic or advanced arithmetic calculations, such as addition, multiplication, division, algebraic expressions, or percentage-based calculations.
#             - Example inputs:
#             - "What is 12 * 8 + 5?"
#             - "Calculate the area of a rectangle with length 10 and width 4."
#             - "Solve 2x + 4 = 10"

#             ---

#             ☁️ Tool Name: weather_details(location: str)

#             - Purpose: Provide weather-related details for a specific city or place.
#             - Example inputs:
#             - "What's the weather like in Mumbai today?"
#             - "Tell me the current temperature in New York."
#             - "Is it raining in Paris?"

#             ---

#             📘 Tool Name: education(topic: str)

#             - Purpose: Explain academic topics or educational subjects (science, history, programming, mathematics, language, etc.).
#             - Example inputs:
#             - "Explain Newton's second law."
#             - "What is photosynthesis?"
#             - "Teach me the basics of Python functions."

#             ---

#             ✈️ Tool Name: trip_plan(destination: str)

#             - Purpose: Suggest a travel plan or itinerary for a city, region, or country.
#             - Example inputs:
#             - "Plan a 3-day trip to Goa."
#             - "What should I visit in Tokyo?"
#             - "Give me a travel guide for Kerala."

#             ---

#             🏁 Your Task:

#             When a user sends a message, analyze the intent. Then:

#             1. Identify which tool (if any) fits the request.
#             2. Call the tool with the right argument.
#             3. Return the result to the user clearly.

#             If the question is vague, ask the user for clarification.

#             Never guess a result — always rely on the correct tool output.
            
#             """

#     chat_completion = client.chat.completions.create(
#         model="llama3-70b-8192",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": question}
#         ]
#     )

#     reply = chat_completion.choices[0].message.content.strip()
#     # VERY basic keyword mapping (you can improve with LLM function calling)
#     if "math" in question.lower() or "calculate" in question.lower():
#         return mathematics_calculation(question)
#     elif "weather" in question.lower():
#         return weather_details(question)
#     elif "trip" in question.lower() or "plan" in question.lower():
#         return trip_plan(question)
#     elif "explain" in question.lower() or "learn" in question.lower():
#         return education(question)
#     else:
#         return reply

