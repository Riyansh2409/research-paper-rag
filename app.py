import os
import streamlit as st
from pypdf import PdfReader
from src.loader.pdf_loader import load_pdfs
from src.chunking.text_splitter import create_chunks
from src.embeddings.embedding_model import get_embedding_model
from src.vectorstore.faiss_store import create_vectorstore
from src.chains.rag_chain import ask_question
from src.memory.chat_memory import ChatMemory
from src.utils.hash_utils import generate_documents_hash


# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Research Paper Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Research Paper Assistant")
st.markdown("Chat with your PDFs using RAG + Gemini")


# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "memory" not in st.session_state:
    st.session_state.memory = ChatMemory()

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_hash" not in st.session_state:
    st.session_state.current_hash = None
if "pdf_count" not in st.session_state:
    st.session_state.pdf_count = 0
if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = []
if "uploaded_file_pages" not in st.session_state:
    st.session_state.uploaded_file_pages = []
if "total_pages" not in st.session_state:
    st.session_state.total_pages = 0

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0    
    
    
def export_chat():

    chat = ""

    for message in st.session_state.messages:

        role = message["role"].capitalize()

        chat += f"{role}:\n"
        chat += f"{message['content']}\n"
        chat += "-" * 60 + "\n"

    return chat


# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:

    st.header("📂 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Select one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):

        st.session_state.messages = []
        st.session_state.memory = ChatMemory()

        st.rerun()
    # ----------------------------------------------------
   # Statistics
   # ----------------------------------------------------

    st.divider()

    st.subheader("📊 Statistics")

    if st.session_state.documents_loaded:

        pdf_count = st.session_state.pdf_count

        total_pages = st.session_state.total_pages

        total_chunks = st.session_state.total_chunks

        st.metric(
            "PDFs Loaded",
            pdf_count
        )

        st.metric(
            "Total Pages",
            total_pages
        )

        st.metric(
            "Total Chunks",
            total_chunks
        )

        st.markdown("---")

        st.markdown("**Embedding Model**")
        st.caption("all-MiniLM-L6-v2")

        st.markdown("**LLM**")
        st.caption("Gemini 2.5 Flash")
        st.divider()

        st.subheader("📂 Uploaded Documents")

        for name, pages in zip(
          st.session_state.uploaded_file_names,
          st.session_state.uploaded_file_pages
        ):

            st.markdown(f"📄 **{name}**")
            st.caption(f"{pages} Pages")
    else:

        st.info("Upload PDFs to view statistics.")
    st.divider()

    st.subheader("💾 Export Chat")

    st.download_button(
        label="⬇ Download Chat (.txt)",
        data=export_chat(),
        file_name="chat_history.txt",
        mime="text/plain",
        use_container_width=True
    )   
    st.divider()

    st.subheader("⚙️ Retrieval Settings")

    top_k = st.slider(
        "Retrieved Chunks",
        min_value=1,
        max_value=10,
        value=3
    )    
# ----------------------------------------------------
# Process PDFs
# ----------------------------------------------------

if uploaded_files:

    os.makedirs("data/papers", exist_ok=True)

    # Remove Previous PDFs
    for file in os.listdir("data/papers"):

        if file.endswith(".pdf"):

            os.remove(
                os.path.join(
                    "data/papers",
                    file
                )
            )

    # Save Uploaded PDFs
    for file in uploaded_files:

        save_path = os.path.join(
            "data/papers",
            file.name
        )

        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

    # Generate Hash
    document_hash = generate_documents_hash("data/papers")

    # Process Only If Documents Changed
    if document_hash != st.session_state.current_hash:

        st.session_state.current_hash = document_hash

        st.session_state.documents_loaded = False
        st.session_state.vectorstore = None
        st.session_state.messages = []
        st.session_state.memory = ChatMemory()

        with st.spinner("Processing PDFs..."):

            docs = load_pdfs("data/papers")

            chunks = create_chunks(docs)
            # Save Uploaded File Information
            st.session_state.uploaded_file_names = []
            st.session_state.uploaded_file_pages = []
            
            for file in uploaded_files:

                pdf_path = os.path.join(
                "data/papers",
                file.name
              )
                reader = PdfReader(pdf_path)
                st.session_state.uploaded_file_names.append(file.name)
                st.session_state.uploaded_file_pages.append(len(reader.pages))

            st.session_state.pdf_count = len(uploaded_files)

            st.session_state.total_pages = len(docs)

            st.session_state.total_chunks = len(chunks)

            embeddings = get_embedding_model()

            vectorstore = create_vectorstore(
                chunks=chunks,
                embeddings=embeddings,
                current_hash=document_hash
            )

            st.session_state.vectorstore = vectorstore
            st.session_state.documents_loaded = True

        st.success("✅ Documents Processed Successfully")
        
    else:

        st.info("📄 Same documents are already loaded.")    
# ----------------------------------------------------
# Status
# ----------------------------------------------------

if st.session_state.documents_loaded:

    st.success("🟢 Knowledge Base Ready")

else:

    st.info("📄 Upload PDFs to get started.")


# ----------------------------------------------------
# Chat Interface
# ----------------------------------------------------

if st.session_state.documents_loaded:

    # Show Previous Messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Chat Input
    question = st.chat_input(
        "Ask anything about your documents..."
    )

    if question:

        # ---------------- User Message ----------------

        with st.chat_message("user"):

            st.markdown(question)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        st.session_state.memory.add_message(
            "User",
            question
        )

        # ---------------- Assistant ----------------

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    result = ask_question(
                        query=question,
                        vectorstore=st.session_state.vectorstore,
                        memory=st.session_state.memory,
                        top_k=top_k
                    )

                    answer = result["answer"]
                    sources = result["sources"]
                    st.markdown(answer)

                    with st.expander("📚 Sources Used"):
                        for source in sources:
                            st.container(border=True).markdown(source)
                    
                    with st.expander("📄 Retrieved Chunks"):

                        for i, doc in enumerate(result["docs"], start=1):

                            st.markdown(f"*** Chunk {i}")

                            st.caption(
                                f"📄 {os.path.basename(doc.metadata['source'])} | "
                                f"Page {doc.metadata['page'] + 1}"
                                )       
                            st.container(border=True).markdown(
                                doc.page_content
                            ) 

                except Exception as e:

                    answer = (
                        "⚠️ Gemini API is temporarily unavailable.\n\n"
                        "Please try again in a few moments."
                    )

                    st.error(answer)

                    # Debug (remove later if deploying)
                    st.caption(str(e))

        # Save Assistant Response
        st.session_state.memory.add_message(
            "Assistant",
            answer
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )        