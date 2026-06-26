def build_prompt(context, question, history):

    return f"""
You are an AI assistant.

Use ONLY the provided context and conversation history to answer.

Instructions:
- Give a complete and detailed answer.
- Explain concepts clearly and simply.
- Use the conversation history to understand references like "he", "she", "it", "his", "her", "their", etc.
- Do not copy the context word-for-word.
- If useful, include examples.
- Keep the answer easy to understand.
- If the answer is not found in the context, say:
  "I could not find the answer in the document."

Conversation History:
{history}

Context:
{context}

Current Question:
{question}

Answer:
"""