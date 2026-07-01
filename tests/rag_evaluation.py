from app.rag.retriever import ParkingRetriever

retriever = ParkingRetriever()

TEST_CASES = [

    {
        "question": "What are parking charges?",
        "expected": ["Car", "SUV", "Motorcycle", "Electric Vehicle"]
    },

    {
        "question": "Is overnight parking available?",
        "expected": ["overnight"]
    },

    {
        "question": "Where can I park in Jhansi?",
        "expected": ["Jhansi"]
    },

    {
        "question": "What payment methods are accepted?",
        "expected": [
            "UPI",
            "Credit Card",
            "Debit Card",
            "Cash"
        ]
    },

    {
        "question": "What is your phone number?",
        "expected": ["9876543210"]
    },

    {
        "question": "Can I modify my reservation?",
        "expected": ["modified"]
    },

    {
        "question": "What are your working hours?",
        "expected": ["24 hours"]
    },

    {
        "question": "Do you support electric vehicles?",
        "expected": ["Electric"]
    },

    {
        "question": "What facilities are available?",
        "expected": [
            "CCTV",
            "Covered parking",
            "Wheelchair",
            "Charging"
        ]
    },

    # Negative Test
    {
        "question": "Can I park my helicopter?",
        "expected": []
    }

]

total_precision = 0
total_recall = 0
evaluated_cases = 0

print("\n========== RAG EVALUATION ==========\n")

for test in TEST_CASES:

    question = test["question"]
    expected = test["expected"]

    docs = retriever.retrieve(question)
    retrieved_text = " ".join(docs)

    matched = 0

    for word in expected:

        if word.lower() in retrieved_text.lower():
            matched += 1

    print("-" * 60)
    print("Question :", question)

    # -------------------------
    # Negative Test Case
    # -------------------------
    if len(expected) == 0:

        if len(docs) == 0:
            print("Result   : PASS (No relevant documents retrieved)")
        else:
            print("Result   : FAIL (Retriever returned no matching information)")

        continue

    # -------------------------
    # Normal Precision / Recall
    # -------------------------
    precision = matched / len(expected)
    recall = matched / len(expected)

    total_precision += precision
    total_recall += recall
    evaluated_cases += 1

    print("Matched  :", matched, "/", len(expected))
    print("Precision:", round(precision, 2))
    print("Recall   :", round(recall, 2))

    if matched == len(expected):
        print("Status   : PASS ✅")
    else:
        print("Status   : FAIL ❌")

# -------------------------
# Final Summary
# -------------------------

print("\n====================================")

if evaluated_cases > 0:
    print("Average Precision@K :", round(total_precision / evaluated_cases, 2))
    print("Average Recall@K    :", round(total_recall / evaluated_cases, 2))

print("Total Test Cases     :", len(TEST_CASES))
print("Evaluated Cases      :", evaluated_cases)

print("====================================")