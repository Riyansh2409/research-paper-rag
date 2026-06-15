from src.loader.pdf_loader import load_pdf

docs = load_pdf("data/papers/NLP- MODULE 1.pptx.pdf")

print(f"Total Pages: {len(docs)}")
print()
print(docs[0].page_content[:1000])
print(docs[0].metadata)