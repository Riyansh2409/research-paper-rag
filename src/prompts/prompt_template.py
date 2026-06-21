def build_prompt(context, question):

    return f"""
You are an AI assistant.

Use ONLY the provided context to answer.

Instructions:
- Give a complete and detailed answer.
- Explain concepts clearly and simply.
- Do not copy the context word-for-word.
- If useful, include examples.
- Keep the answer easy to understand.
- If the answer is not found in the context, say:
  "I could not find the answer in the document."

Context:
{context}

Question:
{question}

Answer:
"""