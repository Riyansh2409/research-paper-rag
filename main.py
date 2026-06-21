from src.loader.pdf_loader import load_pdf
from src.chunking.text_splitter import create_chunks
from src.embeddings.embedding_model import get_embedding_model
from src.vectorstore.faiss_store import create_vectorstore
from src.retriever.retriever import get_retriever
from src.llm.gemini_model import get_llm
from src.prompts.prompt_template import build_prompt

# Load PDF
docs = load_pdf("data/papers/NLP- MODULE 1.pptx.pdf")

# Create Chunks
chunks = create_chunks(docs)

print(f"Total Pages: {len(docs)}")
print(f"Total Chunks: {len(chunks)}")

# Load Embedding Model
embeddings = get_embedding_model()

# Create FAISS Vector Store
vectorstore = create_vectorstore(
    chunks=chunks,
    embeddings=embeddings
)

print("✅ Vector Store Created Successfully")

# Create Retriever
retriever = get_retriever(vectorstore)

# User Query
query = input("Ask a question: ")

# Retrieve Relevant Chunks
results = retriever.invoke(query)

# Build Context
context = "\n\n".join(
    [doc.page_content for doc in results]
)

print("\nRetrieved Context:")
print("=" * 50)
print(context[:1000])

# Load Gemini
llm = get_llm()

# Create Prompt
prompt = build_prompt(
    context=context,
    question=query
)

# Generate Answer
response = llm.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\n")
print("=" * 50)
print("RAG ANSWER")
print("=" * 50)
print(response.text)