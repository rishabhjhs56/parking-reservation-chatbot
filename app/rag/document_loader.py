from pathlib import Path

from langchain_community.document_loaders import TextLoader


def load_documents():
    """
    Load parking knowledge base documents from the data/documents folder.
    """

    data_path = Path("data/documents/parking_information.txt")

    loader = TextLoader(
        file_path=str(data_path),
        encoding="utf-8"
    )

    documents = loader.load()

    return documents