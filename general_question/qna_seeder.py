import json
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from llm.config import text_embedding
from pathlib import Path

class QnaSeeder:
    def __init__(self, json_path="general_question/qna.json", index_path="qna_index_db"):
        self.json_path = json_path
        self.index_path = index_path
        self.embeddings = text_embedding

    def run(self):
        # ✅ Skip if already seeded
        faiss_file = Path(self.index_path) / "index.faiss"
        pkl_file = Path(self.index_path) / "index.pkl"
        if faiss_file.exists() and pkl_file.exists():
            print(f"⚠️  Vector store already exists at '{self.index_path}'. Skipping seeding.")
            return

        # Load JSON
        with open(self.json_path, "r", encoding="utf-8") as f:
            qa_data = json.load(f)

        # Convert to Documents
        documents = [
            Document(
                page_content=item["question"] +"  " + item["answer"],
                metadata={
                    "question": item["question"],
                    "lang": "ar"
                }
            )
            for item in qa_data
        ]

        print(f"📄 Loaded {len(documents)} documents. Creating vector store...")

        # Build and save vector store
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        vectorstore.save_local(self.index_path)

        print(f"✅ Vector store saved at '{self.index_path}'.")

    def load_vectorstore(self):
        faiss_file = Path(self.index_path) / "index.faiss"
        pkl_file = Path(self.index_path) / "index.pkl"

        if not faiss_file.exists() or not pkl_file.exists():
            raise FileNotFoundError(f"Vector index not found in {self.index_path}. Run `run()` first.")

        return FAISS.load_local(self.index_path, embeddings=self.embeddings, allow_dangerous_deserialization=True)
