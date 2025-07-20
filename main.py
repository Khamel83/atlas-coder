import os
import sys
from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENAI_API_KEY")
)

model = os.getenv("OPENAI_MODEL", "openrouter/google/gemini-1.5-flash")

system_prompt = """You are Atlas Coder, a helpful AI that diagnoses and fixes software bugs.
Given a traceback, you reply with a clear explanation of the error and offer a corrected version of the affected code if possible."""

print("Atlas Coder ready. Type your question.")

try:
    if not sys.stdin.isatty():
        user_input = sys.stdin.read()
    else:
        user_input = input("🧠> ")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    print("\n💡", response.choices[0].message.content.strip())

except Exception as e:
    print("⚠️ Error:", e)
