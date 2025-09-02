#!/usr/bin/env python3
"""
Minimal terminal FAQ chatbot (pure Python + scikit-learn).
- Loads/creates a small FAQ knowledge base (faq.json).
- Uses TF-IDF + cosine similarity to pick the best answer.
- Falls back to "I don't know" if confidence is low.
"""

from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())

DEFAULT_FAQ = [
    {"q": "What services do you offer?", "a": "We provide data analytics, AI prototypes, and automation consulting."},
    {"q": "How do we start a project?", "a": "We begin with a discovery call to define the problem, scope, data, and success metrics."},
    {"q": "What data do you need?", "a": "Typically a sample dataset, schema, and access details. We’ll sign an NDA if needed."},
    {"q": "How long does a pilot take?", "a": "Most pilots take 2–4 weeks depending on data quality and scope."},
    {"q": "How do you price projects?", "a": "Fixed-price for well-scoped pilots; retainer or T&M for ongoing work."},
    {"q": "Do you handle production deployment?", "a": "Yes. We containerize, set up CI/CD, monitoring, and handover docs."},
]

KB_PATH = Path("faq.json")

def ensure_kb():
    if not KB_PATH.exists():
        KB_PATH.write_text(json.dumps(DEFAULT_FAQ, indent=2))
        print("Created starter knowledge base: faq.json")
    with KB_PATH.open() as f:
        data = json.load(f)
    questions = [normalize(item["q"]) for item in data]
    answers = [item["a"] for item in data]
    return questions, answers

@dataclass
class Retriever:
    questions: List[str]
    answers: List[str]
    vectorizer: object
    doc_matrix: object

    @classmethod
    def build(cls, questions: List[str], answers: List[str]) -> "Retriever":
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        doc_matrix = vectorizer.fit_transform(questions)
        return cls(questions, answers, vectorizer, doc_matrix)

    def query(self, user_text: str) -> Tuple[str, float]:
        from sklearn.metrics.pairwise import cosine_similarity
        q_vec = self.vectorizer.transform([normalize(user_text)])
        sims = cosine_similarity(q_vec, self.doc_matrix)[0]
        idx = int(sims.argmax())
        score = float(sims[idx])
        return self.answers[idx], score

def main():
    print("🧠 Simple FAQ Chatbot (type 'exit' or 'quit' to stop)\n")
    try:
        questions, answers = ensure_kb()
        retriever = Retriever.build(questions, answers)
    except ModuleNotFoundError:
        print("scikit-learn is not installed. In PowerShell run:\n  pip install scikit-learn")
        return

    CONFIDENCE = 0.25
    history: List[Tuple[str, str]] = []

    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}:
            print("Bot: Bye! 👋")
            break
        if not user:
            continue

        answer, score = retriever.query(user)

        if score < CONFIDENCE:
            print("Bot: I’m not sure about that yet. Could you rephrase or ask about services, pricing, data, pilots, or deployment?")
        else:
            print(f"Bot: {answer}  (conf:{score:.2f})")

        history.append((user, answer))

if __name__ == "__main__":
    main()
