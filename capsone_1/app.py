# file: app.py

from fastapi import FastAPI, Query
from typing import List
import requests, zipfile, io

# --- Model abstraction ---
class BaseModelInterface:
    def answer(self, question: str, context: List[str]) -> str:
        raise NotImplementedError

# --- OpenAI ---
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class OpenAIModel(BaseModelInterface):
    def __init__(self, api_key: str):
        if not OPENAI_AVAILABLE:
            raise ImportError("Openai package is not installed")
        openai.api_key = api_key

    def answer(self, question: str, context: List[str]) -> str:
        prompt = "Use only the following context to answer the question:\n"
        prompt += "\n".join(context)
        prompt += f"\n\nQuestion: {question}\nAnswer:"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )
        return response.choices[0].text.strip()

# --- Local model ---
class LocalModel(BaseModelInterface):
    def answer(self, question: str, context: List[str]) -> str:
        snippet = context[0] if context else "No context available"
        return f"[LOCAL MODEL] Question: {question}\nContext snippet: {snippet}"

# --- Model választás ---
USE_LOCAL = True
if USE_LOCAL:
    model = LocalModel()
else:
    model = OpenAIModel(api_key="YOUR_OPENAI_KEY")

# --- Dokumentum betöltés GitHub-ról ---
def load_github_docs(owner: str, repo: str, branch: str = "main", file_exts: list = [".md", ".mdx"]):
    url = f"https://codeload.github.com/{owner}/{repo}/zip/refs/heads/{branch}"
    resp = requests.get(url)
    resp.raise_for_status()
    docs = []

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for f in zf.infolist():
            if any(f.filename.lower().endswith(ext) for ext in file_exts):
                with zf.open(f) as file:
                    try:
                        content = file.read().decode("utf-8", errors="ignore")
                        docs.append({"filename": f.filename, "content": content})
                    except:
                        continue
    return docs

# --- FastAPI setup ---
app = FastAPI(title="GitHub Docs QA API")
DOCUMENTS = []

@app.get("/load_docs")
def load_docs(owner: str = Query(...), repo: str = Query(...), branch: str = Query("main")):
    global DOCUMENTS
    DOCUMENTS = load_github_docs(owner, repo, branch)
    return {"message": f"Loaded {len(DOCUMENTS)} documents from {owner}/{repo} ({branch} branch)"}


@app.get("/ask")
def ask(question: str = Query(...)):
    if not DOCUMENTS:
        return {"error": "No documents loaded yet!"}

    # Egyszerű keresés: szavak előfordulása
    context_snippets = []
    for doc in DOCUMENTS:
        if any(word.lower() in doc["content"].lower() for word in question.split()):
            context_snippets.append(doc["content"])

    answer = model.answer(question, context_snippets[:5])
    return {"question": question, "answer": answer, "sources": [d["filename"] for d in DOCUMENTS[:5]]}
