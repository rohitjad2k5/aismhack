import sys
# Fix encoding for Windows console to support emojis
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from agents.master_orchestrator import orchestrate
from agents.adaptive_agent import initialize_state


print("\n===== STARTING AI SYSTEM TEST =====\n")

state = initialize_state()

profile = {
    "analytical":7,
    "creative":6,
    "social":5,
    "leadership":8,
    "practical":6,
    "empathy":5,
    "risk":7,
    "focus":9,
    "curiosity":8
}


while True:

    result = orchestrate(state, profile)

    print("\nAI:", result)

    if result["action"] == "ask_question":

        trait = result["data"]["trait"]

        fake_score = 7
        state["scores"][trait] += fake_score
        state["confidence"][trait] += 1

    elif result["action"] == "final_result":
        break


print("\n\n========= FINAL RESULT =========")

for k, v in result.items():
    print(f"\n{k.upper()}:\n{v}")

print("\n===== SYSTEM TEST COMPLETE =====")