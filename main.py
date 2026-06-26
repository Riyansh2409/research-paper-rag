from src.chunking.text_splitter import create_chunks
from src.embeddings.embedding_model import get_embedding_model
from src.vectorstore.faiss_store import create_vectorstore
from src.chains.rag_chain import ask_question
from src.loader.pdf_loader import load_pdfs
from src.memory.chat_memory import ChatMemory


# Create Chat Memory
memory = ChatMemory()


# Load PDFs
docs = load_pdfs("data/papers")


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

    # Store User Question
    memory.add_message("User", query)

    answer = ask_question(
        query=query,
        vectorstore=vectorstore,
        memory=memory
    )

    # Store AI Response
    memory.add_message("Assistant", answer)

    print("\n" + "=" * 50)
    print("RAG ANSWER")
    print("=" * 50)
    print(answer)