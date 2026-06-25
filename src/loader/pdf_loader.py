import os
from langchain_community.document_loaders import PyPDFLoader


def load_pdfs(folder_path):
    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)

            print(f"Loading: {file}")

            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            documents.extend(docs)

    print(f"\nTotal PDFs Loaded: {len([f for f in os.listdir(folder_path) if f.endswith('.pdf')])}")
    print(f"Total Pages Loaded: {len(documents)}")

    return documents