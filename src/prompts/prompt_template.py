def build_prompt(context, question):

    return f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

If the answer is not present in the context,
say "I could not find the answer in the document."

Context:
{context}

Question:
{question}

Answer:
"""