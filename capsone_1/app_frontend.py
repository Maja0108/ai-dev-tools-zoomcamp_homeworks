# file: frontend.py

import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("📚 GitHub Dokumentum Kérdező")

# --- GitHub repo betöltés ---
with st.expander("📂 GitHub repo betöltése"):
    owner = st.text_input("Repo tulajdonos:", "DataTalksClub")
    repo = st.text_input("Repo név:", "faq")
    branch = st.text_input("Branch (default: main):", "main")
    if st.button("📥 Dokumentumok betöltése"):
        resp = requests.get(f"{BACKEND_URL}/load_docs", params={"owner": owner, "repo": repo, "branch": branch})
        st.success(resp.json().get("message"))

# --- Kérdés bekérése ---
question = st.text_input("Írd be a kérdésed:")

if st.button("❓ Kérdés küldése"):
    if not question:
        st.warning("Adj meg egy kérdést!")
    else:
        resp = requests.get(f"{BACKEND_URL}/ask", params={"question": question})
        data = resp.json()
        if "error" in data:
            st.error(data["error"])
        else:
            st.subheader("📄 Válasz a modellből")
            st.write(data["answer"])
            st.subheader("📚 Forrás dokumentumok")
            for src in data["sources"]:
                st.write(f"- {src}")
