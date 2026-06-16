from src.loader.pdf_loader import load_pdf
from src.chunking.text_splitter import create_chunks

docs = load_pdf("data/papers/NLP- MODULE 1.pptx.pdf")

chunks = create_chunks(docs)

print(f"Total Pages: {len(docs)}")
print(f"Total Chunks: {len(chunks)}")

print("\nFirst Chunk:\n")
print(chunks[0].page_content[:500])

print("\nMetadata:\n")
print(chunks[0].metadata)
print(len(chunks[0].page_content))