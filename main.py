from src.loader.pdf_loader import load_pdf
from src.chunking.text_splitter import create_chunks
from src.embeddings.embedding_model import get_embedding_model
from src.vectorstore.faiss_store import create_vectorstore
from src.retriever.retriever import get_retriever

docs = load_pdf("data/papers/NLP- MODULE 1.pptx.pdf")
chunks = create_chunks(docs)

print(f"Total Pages: {len(docs)}")
print(f"Total Chunks: {len(chunks)}")

embeddings = get_embedding_model()

vectorstore = create_vectorstore(
    chunks=chunks,
    embeddings=embeddings
)

print("✅ Vector Store Created Successfully")

retriever = get_retriever(vectorstore)

query = "What is Natural Language Processing?"

results = retriever.invoke(query)

print(f"\nQuery: {query}")

for i, doc in enumerate(results, start=1):
    print(f"\n{'=' * 50}")
    print(f"Result {i}")
    print(f"{'=' * 50}")
    print(doc.page_content[:500])