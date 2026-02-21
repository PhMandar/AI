from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# --- Build RAG pipeline once at import ---
docs = PyPDFLoader("data/TheThreeLittlePigs.pdf").load()

chunks = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
).split_documents(docs)

vectorstore = FAISS.from_documents(
    chunks,
    OllamaEmbeddings(model="mistral")
)
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = ChatPromptTemplate.from_template("""
If helpful, you may add general knowledge or reasonable inferences,
but clearly separate them from the context.

Context:
{context}

Question:
{question}
""")

llm = OllamaLLM(model="mistral", temperature=0.7)

rag_chain = (
    {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
    | prompt
    | llm
)

def get_answer(question: str) -> str:
    """Pass a question through the RAG pipeline and return the answer."""
    return rag_chain.invoke(question)