import os
from langchain_community.vectorstores import FAISS

VECTOR_DB_PATH = "data/vectorstore"
INDEX_FILE = os.path.join(VECTOR_DB_PATH, "index.faiss")


def create_vectorstore(chunks, embeddings):

    if os.path.exists(INDEX_FILE):

        print("Loading existing FAISS index...")

        vectorstore = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    else:

        print("Creating new FAISS index...")

        vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )

        vectorstore.save_local(VECTOR_DB_PATH)

        print("FAISS index saved successfully.")

    return vectorstore