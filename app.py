import streamlit as st
import os

from src.loader.pdf_loader import load_pdf
from src.chunking.text_splitter import create_chunks
from src.embeddings.embedding_model import get_embedding_model
from src.vectorstore.faiss_store import create_vectorstore
from src.chains.rag_chain import ask_question

st.set_page_config(
    page_title="AI Research Paper Assistant",
    layout="wide"
)

st.title("📚 AI Research Paper Assistant")

uploaded_file = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)

if uploaded_file is not None:

    os.makedirs("data/papers", exist_ok=True)

    pdf_path = os.path.join(
        "data/papers",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ PDF Uploaded Successfully")

    if "vectorstore" not in st.session_state:

        with st.spinner("Processing PDF..."):

            docs = load_pdf(pdf_path)

            st.write("📄 Total Docs:", len(docs))

            chunks = create_chunks(docs)

            st.write("✂️ Total Chunks:", len(chunks))
            st.write("Total Docs:", len(docs))

            st.write("First Doc Content Length:")
            st.write(len(docs[0].page_content))

            st.code(docs[0].page_content[:1000])
              
            if len(chunks) > 0:
                st.write("First Chunk Preview:")
                st.code(chunks[0].page_content[:500])

            else:
                st.error("❌ No chunks created.")
                st.stop()

            embeddings = get_embedding_model()

            vectorstore = create_vectorstore(
                chunks=chunks,
                embeddings=embeddings
            )

            st.session_state.vectorstore = vectorstore

        st.success("✅ PDF Processed Successfully")

    question = st.text_input(
        "Ask a Question"
    )

    if st.button("Ask"):

        if question.strip():

            with st.spinner("Generating Answer..."):

                answer = ask_question(
                    query=question,
                    vectorstore=st.session_state.vectorstore
                )

            st.subheader("Answer")
            st.write(answer)

        else:
            st.warning("Please enter a question.")
            
            
            
            
