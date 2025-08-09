import requests
import json
import os


def load_examples():
    with open("data/instructions.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Load the prompt template
def load_prompt_template(filepath="prompts/base_prompt.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(format, role, tone, cta, idea):
    template = load_prompt_template()
    examples = load_examples()

    # Find matching examples
    matched_examples = examples.get(role, {}).get(format, [])
    examples_text = ""
    if matched_examples:
        examples_text = "\n\nHere are examples of similar scripts:\n" + "\n\n---\n\n".join(matched_examples[:2])

    # Fill in template with all inputs + examples
    return template.format(format=format, role=role, tone=tone, cta=cta, idea=idea) + examples_text


# Send the prompt to your local Ollama model
def query_ollama(prompt, model_name="mistral"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"⚠️ Error: {response.status_code} - {response.text}"
