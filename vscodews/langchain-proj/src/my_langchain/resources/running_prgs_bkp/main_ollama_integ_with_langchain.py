# Sample code to test the OllamaLLM integration with LangChain. This code creates an instance of the OllamaLLM class, sets the model to "mistral" and the temperature to 0.7, and then invokes the model with a simple prompt to explain LangChain in simple terms.
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="mistral",
    temperature=0.7
)

print(llm.invoke("Explain LangChain in simple terms"))