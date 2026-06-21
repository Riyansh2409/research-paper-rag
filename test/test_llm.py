from src.llm.gemini_model import get_llm

llm = get_llm()

response = llm.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is NLP?"
)

print(response.text)