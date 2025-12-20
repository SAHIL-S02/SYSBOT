import ollama
import json

def ask_llm(command):
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an automation planner. "
                    "Return ONLY valid JSON. "
                    "Actions allowed: open_app, click, type, scrape, wait."
                )
            },
            {"role": "user", "content": command}
        ]
    )
    return json.loads(response["message"]["content"])
print(ask_llm("Open the calculator app and add 2 and 3."))