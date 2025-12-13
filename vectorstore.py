# vectorstore.py

import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class FaissVectorStore:
    def __init__(
        self,
        persist_dir: str = "faiss_store",
        model_name: str = "nomic-embed-text",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.persist_dir = persist_dir
        self.embeddings = OllamaEmbeddings(model=model_name)

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )

        self.vectorstore = None
        os.makedirs(self.persist_dir, exist_ok=True)

    def build(self, documents: List[Document]):
        chunks = self.splitter.split_documents(documents)

        self.vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings,
        )

        self.vectorstore.save_local(self.persist_dir)

    def load(self):
        self.vectorstore = FAISS.load_local(
            self.persist_dir,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

if __name__ == '__main__':
    from  data_loader import DataLoader
    data_loader = DataLoader("sourcefiles",["pdf","xlsx","csv","docx"])
    docs = data_loader.load_files()

    vector_store = FaissVectorStore(persist_dir='faiss_store')
    vector_store.build(docs)