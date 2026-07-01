from app.rag.retriever import ParkingRetriever


class TestRetriever:

    def test_retrieve_parking_charges(self):
        """
        Positive Test:
        Retriever should return parking charges information.
        """

        retriever = ParkingRetriever()

        docs = retriever.retrieve("What are the parking charges?")

        assert len(docs) > 0
        assert "Car" in " ".join(docs)

    def test_no_result_for_irrelevant_question(self):
        """
        Negative Test:
        Retriever should not return parking information
        for an unrelated question.
        """

        retriever = ParkingRetriever()

        docs = retriever.retrieve(
            "Who won the Cricket World Cup in 2022?"
        )

        assert docs == []