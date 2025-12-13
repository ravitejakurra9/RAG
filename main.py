# main.py

from rag_system import RAGSystem

if __name__ == "__main__":
    rag = RAGSystem(model_name="gemma3:4b")
    print("RAG system ready. Type exit to quit.")

    while True:
        q = input("You: ")
        if q.lower() in ["quit", "exit"]:
            break

        result = rag.ask(q)
        print("\nAnswer:", result["answer"])
        # print("Sources:", result["source_docs"])
