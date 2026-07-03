from app.rag.retriever import ParkingRetriever


class FakeEmbedding:

    def embed_query(self, query):
        return [0.1, 0.2, 0.3]


class FakeStore:

    def search(self, vector, limit):

        return [
            [
                {
                    "entity": {
                        "text": "Car parking charges are ₹50/hour"
                    }
                }
            ]
        ]


class EmptyStore:

    def search(self, vector, limit):
        return [[]]


class TestRetriever:

    def test_retrieve_parking_charges(self):

        retriever = ParkingRetriever(
            store=FakeStore(),
            embedding_model=FakeEmbedding()
        )

        docs = retriever.retrieve("parking charges")

        assert len(docs) == 1
        assert "Car" in docs[0]

    def test_no_result_for_irrelevant_question(self):

        retriever = ParkingRetriever(
            store=EmptyStore(),
            embedding_model=FakeEmbedding()
        )

        docs = retriever.retrieve("Who won World Cup?")

        assert docs == []