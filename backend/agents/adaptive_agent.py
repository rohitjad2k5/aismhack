import random

TRAITS = [
    "analytical","creative","social","leadership",
    "practical","empathy","risk","focus","curiosity"
]


QUESTION_BANK = {
    "analytical":[
        "Do you enjoy solving logic puzzles?",
        "Can you quickly find patterns in numbers?",
        "Do you like analyzing problems deeply?"
    ],
    "creative":[
        "Do you often think of new ideas?",
        "Do you enjoy designing things?",
        "Do you like imagining possibilities?"
    ],
    "social":[
        "Do you enjoy meeting new people?",
        "Do you like group discussions?",
        "Do you feel energized in social events?"
    ],
    "leadership":[
        "Do you naturally take charge in teams?",
        "Do people look to you for decisions?",
        "Do you enjoy guiding others?"
    ],
    "practical":[
        "Do you like hands-on activities?",
        "Do you prefer doing rather than planning?",
        "Do you enjoy building things?"
    ],
    "empathy":[
        "Can you easily understand others' feelings?",
        "Do people confide in you?",
        "Do you feel affected by others' emotions?"
    ],
    "risk":[
        "Do you take bold decisions?",
        "Are you comfortable with uncertainty?",
        "Do you enjoy risky challenges?"
    ],
    "focus":[
        "Can you work for hours without distraction?",
        "Do you finish tasks you start?",
        "Can you ignore noise while working?"
    ],
    "curiosity":[
        "Do you ask many questions?",
        "Do you enjoy learning new topics?",
        "Do you explore things deeply?"
    ]
}


def initialize_state():
    return {
        "scores": {t:0 for t in TRAITS},
        "asked": [],
        "confidence": {t:0 for t in TRAITS}
    }


def choose_trait(state):
    return min(state["confidence"], key=state["confidence"].get)


def next_question(state):

    trait = choose_trait(state)

    remaining = [
        q for q in QUESTION_BANK[trait]
        if q not in state["asked"]
    ]

    if not remaining:
        return {"status":"complete"}

    question = random.choice(remaining)
    state["asked"].append(question)

    return {
        "trait": trait,
        "question": question,
        "remaining": len(remaining)-1
    }


def update_state(state, trait, score):

    state["scores"][trait] += score
    state["confidence"][trait] += 1

    return state
