from src.retriever.retriever import get_retriever
from src.prompts.prompt_template import build_prompt
from src.llm.gemini_model import get_llm


def ask_question(query, vectorstore):

    # Create Retriever
    retriever = get_retriever(vectorstore)

    # Retrieve Relevant Chunks
    docs = retriever.invoke(query)

    # Create Context
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # Build Prompt
    prompt = build_prompt(
        context=context,
        question=query
    )

    # Load Gemini
    llm = get_llm()

    # Generate Response
    response = llm.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text