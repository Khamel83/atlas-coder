import os
import openai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
budget = float(os.getenv("BUDGET_PER_HOUR", 0.05))
model = os.getenv("MODEL_NAME", "google/gemini-2.0-flash-lite-001")

openai.api_key = api_key
openai.api_base = "https://openrouter.ai/api/v1"

def ask(prompt):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print("Atlas Coder ready. Type your question.")
    while True:
        try:
            prompt = input("🧠> ")
            if prompt.lower() in ["exit", "quit"]:
                break
            response = ask(prompt)
            print("🤖>", response)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("⚠️ Error:", e)
