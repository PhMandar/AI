import requests

def ask_llm(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    # 🔍 Print entire response for debugging
    print("Status Code:", response.status_code)
    print("Full JSON:", response.text)

    # Try to parse the actual response
    data = response.json()
    if "response" in data:
        return data["response"]
    else:
        return f"⚠️ 'response' key not found. Full data: {data}"

# Example usage
question = "Explain what an LLM is in simple terms."
answer = ask_llm(question)
print("Answer:", answer)
