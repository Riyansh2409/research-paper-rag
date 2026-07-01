# import os
# import streamlit as st
# from src.chains.rag_chain import ask_question
# from src.loader.pdf_loader import load_pdfs
# from src.chunking.text_splitter import create_chunks
# from src.embeddings.embedding_model import get_embedding_model
# from src.vectorstore.faiss_store import create_vectorstore
# from src.memory.chat_memory import ChatMemory
# from src.utils.hash_utils import generate_documents_hash


# # ----------------------------------------------------
# # Page Configuration
# # ----------------------------------------------------

# st.set_page_config(
#     page_title="AI Research Paper Assistant",
#     page_icon="🤖",
#     layout="wide"
# )

# st.title("🤖 AI Research Paper Assistant")
# st.markdown("Chat with your PDFs using RAG + Gemini")


# # ----------------------------------------------------
# # Session State
# # ----------------------------------------------------
# if "vectorstore" not in st.session_state:
#     st.session_state.vectorstore = None

# if "memory" not in st.session_state:
#     st.session_state.memory = ChatMemory()

# if "documents_loaded" not in st.session_state:
#     st.session_state.documents_loaded = False

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ----------------------------------------------------
# # Sidebar
# # ----------------------------------------------------

# with st.sidebar:

#     st.header("📂 Upload PDFs")

#     uploaded_files = st.file_uploader(
#         "Select one or more PDF files",
#         type=["pdf"],
#         accept_multiple_files=True
#     )
   

#     st.divider()

#     if st.button("🗑 Clear Chat", use_container_width=True):

#         st.session_state.messages = []

#         st.session_state.memory = ChatMemory()

#         st.rerun()

# # ----------------------------------------------------
# # Process PDFs
# # ----------------------------------------------------

# if uploaded_files:

#     os.makedirs("data/papers", exist_ok=True)
    
#     # Clear old PDFs
#     for file in os.listdir("data/papers"):

#       if file.endswith(".pdf"):

#         os.remove(
#             os.path.join(
#                 "data/papers",
#                 file
#             )
#         )

# # Reset Session
#     st.session_state.documents_loaded = False
#     st.session_state.vectorstore = None
#     st.session_state.messages = []
#     st.session_state.memory = ChatMemory()
    
#     # Save uploaded PDFs
#     for file in uploaded_files:
        
#         save_path = os.path.join(
#             "data/papers",
#             file.name
#         )

#         with open(save_path, "wb") as f:
#             f.write(file.getbuffer())

#     with st.spinner("Processing documents..."):

#         # Generate Hash
#         document_hash = generate_documents_hash("data/papers")

#         # Load PDFs
#         docs = load_pdfs("data/papers")

#         # Create Chunks
#         chunks = create_chunks(docs)

#         # Embeddings
#         embeddings = get_embedding_model()

#         # Vector Store
#         vectorstore = create_vectorstore(
#             chunks=chunks,
#             embeddings=embeddings,
#             current_hash=document_hash
#         )

#         st.session_state.vectorstore = vectorstore
#         st.session_state.documents_loaded = True

#     st.success("✅ Documents processed successfully!")


# # ----------------------------------------------------
# # Status
# # ----------------------------------------------------

# if st.session_state.documents_loaded:

#     st.success("🟢 Knowledge Base Ready")

# else:

#     st.info("📄 Upload PDFs to get started.")
# # ----------------------------------------------------
# # Chat Interface
# # ----------------------------------------------------

# if st.session_state.documents_loaded:

#     # Display Chat History
#     for message in st.session_state.messages:

#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Chat Input
#     question = st.chat_input(
#         "Ask anything about your documents..."
#     )

#     if question:

#         # Display User Message
#         with st.chat_message("user"):
#             st.markdown(question)

#         st.session_state.messages.append(
#             {
#                 "role": "user",
#                 "content": question
#             }
#         )

#         # Store User Message in Memory
#         st.session_state.memory.add_message(
#             "User",
#             question
#         )

#         # Generate AI Response
#         # Generate AI Response
#         with st.chat_message("assistant"):

#           with st.spinner("Thinking..."):

#              try:

#                answer = ask_question(
#                 query=question,
#                 vectorstore=st.session_state.vectorstore,
#                 memory=st.session_state.memory
#              )

#                st.markdown(answer)

#              except Exception as e:

#                  answer = "⚠️ Gemini API is temporarily unavailable. Please try again in a few moments."

#                  st.error(answer)
 
#             # Development ke liye (baad me hata dena)
#                  st.caption(str(e))

#     # Save Assistant Response
#           st.session_state.memory.add_message(
#           "Assistant",
#            answer
#           )

#           st.session_state.messages.append(
#             {
#              "role": "assistant",
#              "content": answer
#             }
#           )



import os
import streamlit as st

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

                    answer = ask_question(
                        query=question,
                        vectorstore=st.session_state.vectorstore,
                        memory=st.session_state.memory
                    )

                    st.markdown(answer)

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