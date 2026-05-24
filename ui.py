import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Page title
st.title("📚 AI Study Assistant")


# Initialize memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input form (auto clears after submit)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask your question:")
    send = st.form_submit_button("Send")

if send and user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    try:
        # Get AI response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI Study Assistant. "
                        "Explain concepts simply with examples."
                    )
                }
            ] + st.session_state.messages
        )

        answer = response.choices[0].message.content

        # Save AI response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Refresh page
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")