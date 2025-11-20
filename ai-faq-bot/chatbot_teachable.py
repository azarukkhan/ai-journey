# chatbot_teachable.py
from difflib import SequenceMatcher
from pathlib import Path
import json
import re

print("🧠 Teachable Fuzzy FAQ Bot (type 'help' for commands, 'exit' to quit)\n")

KB_PATH = Path("faq.json")

DEFAULT_FAQ = {
    "what services do you offer": "We provide data analytics, AI prototypes, and automation consulting.",
    "how do we start a project": "We begin with a discovery call to define the problem, scope, data, and success metrics.",
    "what data do you need": "Usually a sample dataset, schema, and access details. We'll sign an NDA if needed.",
    "how long does a pilot take": "Most pilots take 2–4 weeks depending on data quality and scope.",
    "how do you price projects": "Fixed-price for pilots; retainer or time-and-materials for ongoing work.",
    "do you handle production deployment": "Yes. We containerize, set up CI/CD, monitoring, and documentation."
}

def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]", "", s)  # remove punctuation
    return " ".join(s.split())

def load_kb() -> dict[str, str]:
    if KB_PATH.exists():
        try:
            data = json.loads(KB_PATH.read_text(encoding="utf-8"))
            # normalize keys on load
            return {normalize(k): v for k, v in data.items()}
        except Exception:
            print("⚠️ Could not read faq.json, starting with defaults.")
    return DEFAULT_FAQ.copy()

def save_kb(kb: dict[str, str]) -> None:
    # write original (non-normalized) questions by capitalizing a bit
    # but keep keys normalized for matching internally
    KB_PATH.write_text(json.dumps(kb, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"💾 Saved {len(kb)} entries to {KB_PATH.name}")

def best_match(user_text: str, candidates: list[str]) -> tuple[str, float]:
    best_q = ""
    best_score = 0.0
    for q in candidates:
        score = SequenceMatcher(None, user_text, q).ratio()
        if score > best_score:
            best_q, best_score = q, score
    return best_q, best_score

def print_help():
    print(
        "📎 Commands:\n"
        "  help  — show this help\n"
        "  list  — list known questions\n"
        "  teach — add a new question & answer\n"
        "  exit  — quit\n"
    )

def cmd_list(kb: dict[str, str]):
    print("📚 Known questions:")
    for q in sorted(kb.keys()):
        print(" -", q)

def teach_flow(kb: dict[str, str], user_raw: str | None = None):
    # Suggest the user's text (normalized) as the default question
    if user_raw:
        suggested_q = normalize(user_raw)
        print(f"📝 Teaching mode. Press Enter to accept the suggested question, or type your own.")
        q = input(f"Question [{suggested_q}]: ").strip()
        q = normalize(q) if q else suggested_q
    else:
        q = normalize(input("Question: ").strip())

    if not q:
        print("❌ No question provided. Cancelled.")
        return

    a = input("Answer: ").strip()
    if not a:
        print("❌ No answer provided. Cancelled.")
        return

    kb[q] = a
    save_kb(kb)
    print("✅ Learned new Q&A!")

def main():
    kb = load_kb()
    THRESHOLD = 0.72

    while True:
        user_raw = input("You: ").strip()
        if not user_raw:
            continue

        low = user_raw.lower()
        if low == "exit":
            print("Bot: Bye! 👋")
            break
        if low == "help":
            print_help()
            continue
        if low == "list":
            cmd_list(kb)
            continue
        if low == "teach":
            teach_flow(kb)
            continue

        user = normalize(user_raw)

        # exact match first
        if user in kb:
            print("Bot:", kb[user])help
            continue

        # fuzzy match fallback
        q, score = best_match(user, list(kb.keys()))
        if score >= THRESHOLD:
            print("Bot:", kb[q], f"(matched: '{q}', score:{score:.2f})")
        else:
            print("Bot: I’m not sure about that yet.")
            choice = input("🤖 Would you like to TEACH me this? (y/n) ").strip().lower()
            if choice == "y":
                teach_flow(kb, user_raw=user_raw)
            else:
                print("Bot: Okay! You can also type 'teach' anytime to add answers.")

if __name__ == "__main__":
    main()
