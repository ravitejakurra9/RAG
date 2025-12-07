from typing import List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np
from data_loader import DataLoader
from langchain_ollama import OllamaEmbeddings


class EmbeddingPipeline:

    def __init__(self, model_name: str ="nomic-embed-text", chunk_size: int = 1000, chunk_overlap: int = 200):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = OllamaEmbeddings(model=model_name)
        print(f"[INFO] Loaded embedding model: {model_name}")

    
    def chunk_documents(self,documents: list):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function=len,
            separators = ["\n\n","\n"," ",""]
        )
        chunks = splitter.split_documents(documents)
        print(f"[INFO] Splitted {len(documents)} documents into {len(chunks)} chunks.")
        return chunks
    
    def embed_chunks(self, chunks: list) -> np.ndarray:
        texts = [chunk.page_content for chunk in chunks]

        embeddings = self.model.embed_documents(texts)
        embeddings = np.array(embeddings, dtype="float32")
        return embeddings


if __name__ == "__main__":
    data_loader = DataLoader("sourcefiles", ['pdf','xlsx','txt','csv','docx'])
    docs = data_loader.load_files()
    emb_pipe = EmbeddingPipeline()
    chunks = emb_pipe.chunk_documents(docs)
    embeddings = emb_pipe.embed_chunks(chunks)
    print("[INFO] Example embeddings:", embeddings[0] if len(embeddings) > 0 else None)