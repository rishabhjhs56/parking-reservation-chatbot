from app.rag.retriever import ParkingRetriever
from app.utils.azure_llm import get_llm

llm = get_llm()


class ParkingRAG:

    def __init__(self):
        self.retriever = ParkingRetriever()

    def ask(self, question: str):

        documents = self.retriever.retrieve(question)

        context = "\n\n".join(documents)

        prompt = f"""
You are a Parking Assistant.

Answer ONLY using the information provided below.

If the answer is not available, politely say:
"I couldn't find that information."

Parking Information:
{context}

User Question:
{question}
"""

        response = llm.invoke(prompt)

        return response.content