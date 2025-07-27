import requests

def ask_llm(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3",      # 👈 Make sure this matches the model you're running
        "prompt": prompt,
        "stream": False          # If set to True, response will come in chunks
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        if "response" in data:
            return data["response"]
        else:
            return f"⚠️ 'response' key not found. Full data: {data}"

    except requests.exceptions.RequestException as e:
        return f"❌ Request failed: {e}"

# ----------- Main Program ------------
if __name__ == "__main__":
    print("💬 Local LLM (Gemma3) Chat")
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        answer = ask_llm(question)
        print("🤖 LLM:", answer)
