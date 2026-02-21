'''
8 Feb 2026
1. Basic RAG with LangChain and Ollama program.
This code builds a RAG pipeline:
- Load → Split → Embed → Store → Retrieve
- Wrap retrieved context + question into a prompt
- Send to LLM → Get answer

It’s essentially:
“Search your documents → Feed results into the LLM → Answer based on them.”


In this program, you're using RunnableSequence.

Here's why:

The pipe operator | chains runnables together sequentially. Your chain:
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)
executes in this order:

First, the dictionary {"context": retriever, "question": RunnablePassthrough()} runs (this is a 
    RunnableParallel internally, but it's the input stage)
Then the result flows sequentially to prompt
Then the result flows sequentially to llm
So the overall chain type is RunnableSequence because you're chaining three stages together with |.

Note: The dictionary syntax {"context": ..., "question": ...} does create a 
      RunnableParallel internally (it runs the retriever and RunnablePassthrough in parallel), 
      but that's just the first step. The overall chain composition is a RunnableSequence  because you're chaining three stages together with |.
'''

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


# Load
docs = TextLoader("src/my_langchain/data/sample.txt", encoding="utf-8").load()

# Split
chunks = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
).split_documents(docs)

# Vector store
vectorstore = FAISS.from_documents(
    chunks,
    OllamaEmbeddings(model="mistral")
)

retriever = vectorstore.as_retriever()

# Prompt
prompt = ChatPromptTemplate.from_template("""
Answer the question using only the context below.

Context:
{context}

Question:
{question}
""")

llm = OllamaLLM(model="mistral", temperature=0.7)

# LCEL chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

print(rag_chain.invoke("What is LangChain?"))
