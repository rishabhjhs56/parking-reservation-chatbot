
"""

# code to test document_loader.py

from app.rag.document_loader import load_documents

documents = load_documents()

print(documents)


"""



""" 
# code to test text_splitter.py

from app.rag.document_loader import load_documents
from app.rag.text_splitter import split_documents

documents = load_documents()

chunks = split_documents(documents)

print(f"Total Chunks: {len(chunks)}")

print(chunks[0].page_content)

"""


""" 
# code to test config.py

from app.utils.config import AZURE_DEPLOYMENT_NAME

print(AZURE_DEPLOYMENT_NAME)

"""

"""

# code to test azure_llm.py 

from app.utils.azure_llm import llm

print("Before invoke...")

response = llm.invoke("Hi")

print("After invoke...")

print(response.content)

"""

""" 


from app.utils.config import (
    AZURE_API_KEY,
    AZURE_API_VERSION,
    AZURE_ENDPOINT,
    AZURE_DEPLOYMENT_NAME,
)

print("API KEY:", "Loaded" if AZURE_API_KEY else "Missing")
print("API VERSION:", AZURE_API_VERSION)
print("ENDPOINT:", AZURE_ENDPOINT)
print("DEPLOYMENT:", AZURE_DEPLOYMENT_NAME)

"""

""" 

# code to test azure_embedding.py  

from app.utils.azure_embeddings import embeddings

vector = embeddings.embed_query("Parking opens at 8 AM")

print(type(vector))

print(len(vector))

print(vector[:5])


"""

"""

# code to test pymilvus

from pymilvus import connections

connections.connect(
    alias="default",
    host="localhost",
    port="19530"
)

print("Connected Successfully")


"""

"""
# code to test retriver.py

from app.rag.retriever import ParkingRetriever

retriever = ParkingRetriever()

docs = retriever.retrieve("What are the parking charges?")

print(docs)

"""

"""
# code to test rag_chain.py
from app.rag.rag_chain import ParkingRAG

bot = ParkingRAG()

answer = bot.ask("What are the parking charges?")

print(answer)

"""

"""
# code to test reservation_agent.py

from app.rag.rag_chain import ParkingRAG

bot = ParkingRAG()

print("Parking Assistant Started")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    answer = bot.ask(question)

    print(f"\nBot: {answer}\n")

"""

from app.agents.reservation_agent import ReservationAgent


def main():

    print("Parking Reservation Test Started")
    print("Type 'exit' to quit.\n")

    agent = ReservationAgent()
    active = False

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        # start reservation
        if "reserve" in user_input.lower():
            active = True
            print("\nBot:", agent.start_reservation())
            continue

        # reservation flow
        if active:
            response = agent.handle_input(user_input)
            print("\nBot:", response)

            if "Reservation Completed" in response:
                active = False

            continue

        print("\nBot: Say 'reserve' to start booking.")


if __name__ == "__main__":
    main()