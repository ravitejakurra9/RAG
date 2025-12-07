from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, Docx2txtLoader, UnstructuredExcelLoader, JSONLoader
from langchain_core.documents import Document
from typing import List


class DataLoader:
    """
    This Class will load file into langchain Document objects
    """

    def __init__(self,source_dir:str, file_types: list):
        self.source_dir: Path = Path(source_dir).resolve()
        self.file_types: list = file_types

    
    def load_files(self):
        all_documents = []
        for file_type in self.file_types:
            if file_type == 'pdf':
                docs = self.load_pdf_files()
                all_documents.extend(docs)
            elif file_type == 'xlsx':
                docs = self.load_excel_files()
                all_documents.extend(docs)
            elif file_type == 'csv':
                docs = self.load_csv_files()
                all_documents.extend(docs)
            elif file_type == 'docx':
                docs = self.load_doc_files()
                all_documents.extend(docs)
            elif file_type == 'txt':
                docs = self.load_text_files()
                all_documents.extend(docs)

        return all_documents
        
    def load_excel_files(self):
        documents = []
        for file in self.source_dir.glob("**/*.xlsx"):
            loader = UnstructuredExcelLoader(file)
            doc = loader.load()
            documents.extend(doc)
        return documents
    def load_text_files(self):
        documents = []
        for file in self.source_dir.glob("**/*.txt"):
            loader = TextLoader(file)
            doc = loader.load()
            documents.extend(doc)
        return documents
    
    def load_pdf_files(self):
        documents = []
        for file in self.source_dir.glob("**/*.pdf"):
            loader = PyPDFLoader(file)
            doc = loader.load()
            documents.extend(doc)
        return documents
    
    def load_csv_files(self):
        documents = []
        for file in self.source_dir.glob("**/*.csv"):
            loader = CSVLoader(file)
            doc = loader.load()
            documents.extend(doc)
        return documents
    
    def load_doc_files(self):
        documents = []
        for file in self.source_dir.glob("**/*.docx"):
            loader = Docx2txtLoader(file)
            doc = loader.load()
            documents.extend(doc)
        return documents


if __name__ == "__main__":
    data_loader = DataLoader("sourcefiles",["pdf","xlsx","csv","docx"])
    docs = data_loader.load_files()
    print(docs)
    