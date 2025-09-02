# chatbot_simple.py

print("🧠 Simple FAQ Chatbot (type 'exit' to quit)\n")

# our knowledge base
faq = {
    "what services do you offer": "We provide data analytics, AI prototypes, and automation consulting.",
    "how do we start a project": "We begin with a discovery call to define the problem, scope, data, and success metrics.",
    "what data do you need": "Usually a sample dataset, schema, and access details. We'll sign an NDA if needed.",
    "how long does a pilot take": "Most pilots take 2–4 weeks depending on data quality and scope.",
    "how do you price projects": "Fixed-price for pilots; retainer or time-and-materials for ongoing work.",
    "do you handle production deployment": "Yes. We containerize, set up CI/CD, monitoring, and documentation."
}

while True:
    user = input("You: ").strip().lower()  # read input, make lowercase
    if user == "exit":
        print("Bot: Bye! 👋")
        break

    # look for an exact match
    if user in faq:
        print("Bot:", faq[user])
    else:
        print("Bot: Sorry, I don’t know that yet. Try asking about services, pricing, data, pilots, or deployment.")
