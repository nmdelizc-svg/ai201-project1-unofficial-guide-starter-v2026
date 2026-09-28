QUESTIONS = [
    # {"question": "...", "expects": "..."},

    {"question": "How long is the bike ride to campus?", "expects": "about 6"},

    {
        "question": "For summer internships, around what month should I start applying?",
        "expects": "October",
    },

    {
        "question": "Is it weird to go to office hours without a specific question?",
        "expects": "not weird",
    },

    {"question": "How much RAM do I need for a CS laptop?", "expects": "16GB"},

    {
        "question": "When do small local employers hire summer interns?",
        "expects": "February",
    },
]


OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
