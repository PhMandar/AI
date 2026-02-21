'''
1. Basic RAG with LangChain and Ollama program.
This code builds a RAG pipeline:
- Load → Split → Embed → Store → Retrieve
- Wrap retrieved context + question into a prompt
- Send to LLM → Get answer

It’s essentially:
“Search your documents → Feed results into the LLM → Answer based on them.”
'''

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


# Load
docs = PyPDFLoader("src/my_langchain/data/TheThreeLittlePigs.pdf").load()

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
If helpful, you may add general knowledge or reasonable inferences,
but clearly separate them from the context.

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

print(rag_chain.invoke("What is the wolf saying?"))
