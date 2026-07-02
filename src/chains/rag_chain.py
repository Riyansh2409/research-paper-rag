import os

from src.retriever.retriever import get_retriever
from src.prompts.prompt_template import build_prompt
from src.llm.gemini_model import get_llm


def ask_question(query, vectorstore, memory, top_k=3):

    # Create Retriever
    retriever = get_retriever(
        vectorstore,
        top_k=top_k
    )

    # Retrieve Relevant Chunks
    docs = retriever.invoke(query)

    # Create Context
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # Get Conversation History
    history = memory.get_history()

    # Build Prompt
    prompt = build_prompt(
        context=context,
        question=query,
        history=history
    )

    # Load Gemini
    llm = get_llm()

    # Generate Response
    response = llm.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # Collect Sources
    sources = []

    for doc in docs:

        source = os.path.basename(
            doc.metadata.get("source", "Unknown")
        )

        page = doc.metadata.get("page", 0) + 1

        source_text = f"📄 {source} | Page {page}"

        if source_text not in sources:
            sources.append(source_text)

    return {
        "answer": response.text,
        "sources": sources,
        "docs": docs
    }