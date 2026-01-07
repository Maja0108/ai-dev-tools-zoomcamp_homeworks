# file: app_frontend.py

import streamlit as st
import requests

#Configuration
API_URL = "http://127.0.0.1:8000/ask"  # FastAPI backend URL

st.set_page_config(page_title="Mini QA", page_icon="🤖", layout="centered")
st.title("🤖 Mini QA Frontend")
st.caption("Question-answer based on the choosen model")

#Chat input
question = st.text_input("Question:", "")
context = st.text_area("Optional context, Enter new line, one line = one item", "")

if st.button("Send") and question:
    context_list = [line.strip() for line in context.splitlines() if line.strip()]

    payload = {
        "question": question,
        "context": context_list
    }

    try:
        response = requests.get(API_URL, params=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            st.markdown(f"**Answer:** {data['answer']}")
        else:
            st.error(f"Backend error: {response.status_code} {response.text}")
    except Exception as e:
        st.error(f"Error in the request: {e}")
