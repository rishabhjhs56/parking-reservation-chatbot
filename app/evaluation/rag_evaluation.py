import time
import sys
from pathlib import Path

from app.rag.retriever import ParkingRetriever

# ----------------------------------------------------------
# Create Report Folder
# ----------------------------------------------------------

report_dir = Path("docs/evaluation_reports")
report_dir.mkdir(parents=True, exist_ok=True)

report_file = report_dir / "rag_evaluation_report.txt"


class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            try:
                f.write(obj)
                f.flush()
            except ValueError:
                pass

    def flush(self):
        for f in self.files:
            try:
                f.flush()
            except ValueError:
                pass


log_file = open(report_file, "w", encoding="utf-8")

# Console + File
sys.stdout = Tee(sys.__stdout__, log_file)

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
total_response_time = 0

evaluated_cases = 0
passed_cases = 0

print()
print("=" * 80)
print("                SMARTPARK AI - RAG EVALUATION REPORT")
print("=" * 80)

for index, test in enumerate(TEST_CASES, start=1):

    question = test["question"]
    expected = test["expected"]

    start_time = time.perf_counter()

    docs = retriever.retrieve(question)

    end_time = time.perf_counter()

    response_time = end_time - start_time

    total_response_time += response_time

    retrieved_text = " ".join(docs)

    matched_keywords = []

    for keyword in expected:

        if keyword.lower() in retrieved_text.lower():
            matched_keywords.append(keyword)

    matched = len(matched_keywords)

    print("\n" + "-" * 80)
    print(f"Test Case       : TC-{index:02}")
    print(f"Question        : {question}")

    # ---------------- Negative Test ----------------

    if len(expected) == 0:

        if len(docs) == 0:

            print("Expected        : No relevant documents")
            print("Actual          : No documents returned")
            print("Status          : PASS ✅")

            passed_cases += 1

        else:

            print("Expected        : No relevant documents")
            print("Actual          : Retriever returned documents")
            print("Status          : FAIL ❌")

        print(f"Response Time   : {response_time:.3f} sec")

        continue

    # ---------------- Precision / Recall ----------------

    retrieved_keywords = len(expected)

    precision = matched / retrieved_keywords if retrieved_keywords else 0

    recall = matched / len(expected) if expected else 0

    total_precision += precision
    total_recall += recall

    evaluated_cases += 1

    print(f"Expected Keywords : {expected}")
    print(f"Matched Keywords  : {matched_keywords}")
    print(f"Matched           : {matched}/{len(expected)}")
    print(f"Precision@K       : {precision:.2f}")
    print(f"Recall@K          : {recall:.2f}")
    print(f"Response Time     : {response_time:.3f} sec")

    if matched == len(expected):

        print("Status            : PASS ✅")
        passed_cases += 1

    else:

        print("Status            : FAIL ❌")

# ----------------------------------------------------------
# Final Summary
# ----------------------------------------------------------

print()
print("=" * 80)
print("                    FINAL EVALUATION SUMMARY")
print("=" * 80)

average_precision = (
    total_precision / evaluated_cases
    if evaluated_cases
    else 0
)

average_recall = (
    total_recall / evaluated_cases
    if evaluated_cases
    else 0
)

accuracy = (passed_cases / len(TEST_CASES)) * 100

average_response = (
    total_response_time / len(TEST_CASES)
)

print(f"Total Test Cases        : {len(TEST_CASES)}")
print(f"Passed                  : {passed_cases}")
print(f"Failed                  : {len(TEST_CASES)-passed_cases}")

print()

print(f"Response Accuracy       : {accuracy:.2f}%")
print(f"Average Precision@K     : {average_precision:.2f}")
print(f"Average Recall@K        : {average_recall:.2f}")
print(f"Average Response Time   : {average_response:.3f} sec")

print("=" * 80)

log_file.close()

print(f"\n📄 Evaluation report saved at: {report_file}")