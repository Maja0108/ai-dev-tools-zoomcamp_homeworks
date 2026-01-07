# file: app.py

from fastapi import FastAPI, Query
from typing import List

# ---- Dokumentumok (példa) ----
DOCUMENTS = [
    {"title": "Application System Set", "content": "Ez az alkalmazás rendszerbeállítási leírás..."},
    {"title": "Data Pipeline", "content": "Adatfeldolgozás lépései Pythonban..."},
    {"title": "Machine Learning", "content": "ML modellek építése, predikciók..."}
]

def search_docs(query: str, docs=DOCUMENTS, top_k=3):
    """Egyszerű full-text keresés a dokumentumok között"""
    query_lower = query.lower()
    matches = []
    for doc in docs:
        if query_lower in doc["title"].lower() or query_lower in doc["content"].lower():
            matches.append(doc)
    return matches[:top_k]

# ---- Model abstraction ----
class BaseModelInterface:
    def answer(self, question: str, context: List[str]) -> str:
        raise NotImplementedError

# ---- OpenAI implementation ----
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class OpenAIModel(BaseModelInterface):
    def __init__(self, api_key: str):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package is not installed")
        openai.api_key = api_key

    def answer(self, question: str, context: List[str]) -> str:
        prompt = "Use only the following context to answer the question:\n"
        prompt += "\n".join(context)
        prompt += f"\n\nQuestion: {question}\nAnswer:"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        return response.choices[0].text.strip()

# ---- Local model ----
class LocalModel(BaseModelInterface):
    def answer(self, question: str, context: List[str]) -> str:
        snippet = context[0] if context else "No context available"
        return f"[LOCAL MODEL] Question: {question}\nContext snippet: {snippet}"

# ---- Model selection ----
USE_LOCAL = True  # True = Local, False = OpenAI

if USE_LOCAL:
    model = LocalModel()
else:
    model = OpenAIModel(api_key="YOUR_OPENAI_KEY")

# ---- FastAPI setup ----
app = FastAPI(title="Selectable Model QA API with Docs")

@app.get("/ask")
def ask(
    question: str = Query(..., description="Question we want to ask"),
    top_k: int = Query(3, description="Number of documents to consider")
):
    """
    Question-answer endpoint.
    - Performs document search
    - Passes top-k documents as context to selected model
    """
    # 1️⃣ Keresés a dokumentumok között
    matched_docs = search_docs(question, top_k=top_k)
    context_texts = [doc["content"] for doc in matched_docs]

    # 2️⃣ Modell válasz
    answer = model.answer(question, context_texts)

    # 3️⃣ Források visszaadása
    sources = [doc["title"] for doc in matched_docs]

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }
