import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Load examples once at startup
with open("examples.json", "r", encoding="utf-8") as f:
    EXAMPLES = json.load(f)

def build_prompt(user_prompt: str, mode: str):
    """
    If storytelling mode is chosen, attach examples.
    Otherwise, just return the user prompt.
    """
    if mode == "storytelling":
        # join multiple examples nicely
        examples_text = "\n\n---\n\n".join(EXAMPLES["storytelling"])
        return f"""Here are some examples of the desired style:
{examples_text}

Now, write a new reel script in the same style for this topic:
{user_prompt}"""
    else:
        return user_prompt

def query_groq(prompt, model="llama3-8b-8192", mode="default"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # build final prompt depending on mode
    final_prompt = build_prompt(prompt, mode)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who writes engaging reel scripts."},
            {"role": "user", "content": final_prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ Error: {response.status_code} - {response.text}"
