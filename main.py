from src.loader.pdf_loader import load_pdf
from src.chunking.text_splitter import create_chunks
from src.embeddings.embedding_model import get_embedding_model
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

print("KEY FOUND:", key is not None)
print("KEY PREFIX:", key[:10] if key else "NO KEY")

docs = load_pdf("data/papers/NLP- MODULE 1.pptx.pdf")

chunks = create_chunks(docs)

print(f"Total Pages: {len(docs)}")
print(f"Total Chunks: {len(chunks)}")

embeddings = get_embedding_model()

vector = embeddings.embed_query(
    chunks[0].page_content
)

print("\nVector Length:")
print(len(vector))

print("\nFirst 10 Values:")
print(vector[:10])