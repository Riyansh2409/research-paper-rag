from src.loader.pdf_loader import load_pdf
from src.chunking.text_splitter import create_chunks
from src.embeddings.embedding_model import get_embedding_model
from src.vectorstore.faiss_store import create_vectorstore
from src.chains.rag_chain import ask_question

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

# Chat Loop
while True:

    query = input("\nAsk a question: ")

    if query.lower() in ["exit", "quit", "stop"]:
        print("\n👋 Goodbye!")
        break

    answer = ask_question(
        query=query,
        vectorstore=vectorstore
    )

    print("\n" + "=" * 50)
    print("RAG ANSWER")
    print("=" * 50)
    print(answer)