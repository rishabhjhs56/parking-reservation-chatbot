from app.rag.retriever import ParkingRetriever

retriever = ParkingRetriever()

test_queries = [
    "parking charges",
    "location of parking",
    "EV parking availability",
    "cancellation policy"
]

def evaluate():
    print("\nRunning RAG Evaluation...\n")

    total = len(test_queries)
    success = 0

    for q in test_queries:
        docs = retriever.retrieve(q)

        if docs:
            success += 1
            print(f"[OK] {q}")
        else:
            print(f"[FAIL] {q}")

    recall_at_k = success / total

    print("\n=== EVALUATION RESULT ===")
    print(f"Recall@K: {recall_at_k:.2f}")

if __name__ == "__main__":
    evaluate()