import streamlit as st
import os
from dotenv import load_dotenv
from supabase_utils import get_emotion, get_username
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://models.github.ai/inference",
    # api_key=os.environ["GITHUB_TOKEN"] 
    api_key=st.secrets.get("GITHUB_TOKEN")
)

st.title("🎭 elMo - Your eMotion-based chatbot!")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_info" not in st.session_state:
    st.session_state.user_info = {
        "user": get_username(),
        "emotion": get_emotion()
    }

def generate_response():
    history = st.session_state.messages
    formatted_history = [{"role": m["role"], "content": m["content"]} for m in history]

    formatted_history.insert(0, {
        "role": "system",
        "content": (
            "You are a great psychotherapist and you are helping a user understand their emotions better. "
            f"Their name is {st.session_state.user_info['user']} and they are currently feeling {st.session_state.user_info['emotion']}. "
            "Engage with them in a warm, natural, and comforting way. No technical jargon. Feel like a trusted friend or therapist."
        )
    })

    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=formatted_history
    )
    return response.choices[0].message.content

if len(st.session_state.messages) == 0:
    first_message = generate_response()
    st.session_state.messages.append({"role": "assistant", "content": f"**elMo:** {first_message}"})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Say something...")

if prompt:
    user_msg = f"**You:** {prompt}"
    st.session_state.messages.append({"role": "user", "content": user_msg})

    with st.chat_message("user"):
        st.markdown(user_msg)

    assistant_reply = generate_response()
    assistant_reply = f"**elMo:** {assistant_reply}"
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
