# Save as: chatbot.py
# Run with: streamlit run chatbot.py

import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="HealthBot - Wellness Advisor",
    page_icon="💚",
    layout="centered"
)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# System prompt
SYSTEM_PROMPT = """You are HealthBot, a friendly wellness advisor.

You provide general fitness, nutrition, sleep, and wellness tips.
Be warm, encouraging, and practical. Use bullet points for lists.

STRICT RULES:
- NEVER diagnose medical conditions
- NEVER recommend specific medication dosages
- For medical symptoms, always recommend consulting a doctor
- Keep responses concise (2-3 paragraphs max)"""

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App header
st.title("💚 HealthBot")
st.caption("Your friendly wellness advisor — general tips for a healthier life")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me about fitness, nutrition, or wellness..."):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build messages for API call (system prompt + history)
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(st.session_state.messages[-20:])  # Last 10 exchanges

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                temperature=0.7,
                max_tokens=500
            )
            reply = response.choices[0].message.content
            st.write(reply)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Sidebar
with st.sidebar:
    st.header("About HealthBot")
    st.write(
        "HealthBot provides **general wellness tips** about fitness, "
        "nutrition, sleep, and healthy habits."
    )
    st.warning(
        "HealthBot is NOT a medical professional. Always consult a "
        "doctor for medical concerns."
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(f"Messages: {len(st.session_state.messages)}")