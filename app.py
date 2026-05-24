import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("API Key:", api_key)  # test

client = Groq(api_key=api_key)

print("AI Study Assistant Started!")
print("Type 'exit' to stop.\n")

# Memory
messages = [
    {
        "role": "system",
        "content": """
        You are an AI Study Assistant.

        Rules:
        - Explain concepts simply
        - Help students learn
        - Use examples
        """
    }
]

# Quiz function
def generate_quiz(topic):

    prompt = f"""
    Create 3 quiz questions about {topic}.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            { 
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# Summary function
def summarize(topic):

    prompt = f"""
    Summarize {topic} in simple words.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# Main loop
while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    # Quiz command
    if question.startswith("quiz:"):

        topic = question.replace("quiz:", "")

        result = generate_quiz(topic)

        print("\nQuiz:\n", result)

        continue

    # Summary command
    if question.startswith("summary:"):

        topic = question.replace("summary:", "")

        result = summarize(topic)

        print("\nSummary:\n", result)

        continue

    # Save user input
    messages.append({
        "role": "user",
        "content": question
    })

    # AI response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content

    print("\nAgent:", reply, "\n")

    # Save AI response
    messages.append({
        "role": "assistant",
        "content": reply
    })