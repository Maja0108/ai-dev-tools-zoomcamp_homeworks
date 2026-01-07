# file: app.py

from fastapi import FastAPI, Query
from typing import List

# Model abstraction
class BaseModelInterface:
    def answer(self, question: str, context: List[str]) -> str:
        raise NotImplementedError

# OpenAI implementation
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
            max_tokens=200
        )
        return response.choices[0].text.strip()

# Using local model (HuggingFace or LLaMA)
class LocalModel(BaseModelInterface):
    def answer(self, question: str, context: List[str]) -> str:
        
        snippet = context[0] if context else "No context available"
        return f"[LOCAL MODEL] Question: {question}\nContext snippet: {snippet}"

# Using model
USE_LOCAL = True  # True = Local, False = OpenAI

if USE_LOCAL:
    model = LocalModel()
else:
    model = OpenAIModel(api_key="YOUR_OPENAI_KEY")

#Setup FastAPI
app = FastAPI(title="Selectable Model QA API")

@app.get("/ask")
def ask(
    question: str = Query(..., description="Question waht we want to ask"),
    context: List[str] = Query([], description="Optional context")
):
    """
    Question-answer endpoint.
    Answer based on the choosen model.
    """
    answer = model.answer(question, context)
    return {"question": question, "answer": answer}
