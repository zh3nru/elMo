from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

# url = os.environ["SUPABASE_URL"] 
# key = os.environ["SUPABASE_KEY"] 

url = st.secrets.get("SUPABASE_URL")
key = st.secrets.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def get_emotion() -> str | None:
    response = (
        supabase
        .table("emotion_tracking")
        .select("emotion")
        .order("timestamp", desc=True)  
        .limit(1)
        .execute()
    )
    if response.data:
        return response.data[0]["emotion"]
    return None

def get_username() -> str | None:
    user_id_response = (
        supabase
        .table("emotion_tracking")
        .select("user_id")
        .order("timestamp", desc=True)  
        .limit(1)
        .execute()
    )
    if not user_id_response.data or "user_id" not in user_id_response.data[0]:
        return None

    user_id = user_id_response.data[0]["user_id"]

    username_response = (
        supabase
        .table("user_admin")
        .select("username")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )
    if username_response.data and "username" in username_response.data[0]:
        return username_response.data[0]["username"]

    return None

