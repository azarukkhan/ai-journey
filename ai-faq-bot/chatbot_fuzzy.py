# chatbot_fuzzy.py
from difflib import SequenceMatcher

print("🧠 Fuzzy FAQ Chatbot (type 'exit' to quit)\n")

# 1) our knowledge base (same as before)
faq = {
    "what services do you offer": "We provide data analytics, AI prototypes, and automation consulting.",
    "how do we start a project": "We begin with a discovery call to define the problem, scope, data, and success metrics.",
    "what data do you need": "Usually a sample dataset, schema, and access details. We'll sign an NDA if needed.",
    "how long does a pilot take": "Most pilots take 2–4 weeks depending on data quality and scope.",
    "how do you price projects": "Fixed-price for pilots; retainer or time-and-materials for ongoing work.",
    "do you handle production deployment": "Yes. We containerize, set up CI/CD, monitoring, and documentation."
}

def normalize(s: str) -> str:
    # lowercase + basic whitespace cleanup; you could also strip punctuation if you like
    return " ".join(s.lower().strip().split())



def best_match(user_text: str, candidates: list[str]) -> tuple[str, float]:
    """Return (best_candidate, similarity) using difflib's SequenceMatcher ratio."""
    best_q = ""
    best_score = 0.0
    for q in candidates:
        score = SequenceMatcher(None, user_text, q).ratio()
        if score > best_score:
            best_q, best_score = q, score
    return best_q, best_score

THRESHOLD = 0.72  # increase = stricter, decrease = more permissive

while True:
    user_raw = input("You: ").strip()
    if user_raw.lower() == "exit":
        print("Bot: Bye! 👋")
        break
    if not user_raw:
        continue

    user = normalize(user_raw)

    # 2) exact match first (fast path)
    if user in faq:
        print("Bot:", faq[user])
        continue

    # 3) otherwise, fuzzy match to closest known question
    q, score = best_match(user, list(faq.keys()))
    if score >= THRESHOLD:
        print("Bot:", faq[q], f"(matched: '{q}', score:{score:.2f})")
    else:
        print("Bot: Sorry, I’m not sure about that yet. Try asking about services, pricing, data, pilots, or deployment.")
