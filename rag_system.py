# rag_system.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

from model_config import MODEL_CONFIGS
from token_budget import TokenBudget
from history import SimpleHistory
from vectorstore import FaissVectorStore

class RAGSystem:
    def __init__(self, model_name="gemma3:4b", persist_dir="faiss_store"):
        config = MODEL_CONFIGS[model_name]
        self.budget = TokenBudget(
            context_window=config["context_window"],
            output_tokens=config["recommended_output"],
        )

        # LLM
        self.llm = ChatOllama(
            model=model_name,
            temperature=0.3,
            max_tokens=self.budget.output_tokens,
        )

        # History (manual)
        self.history = SimpleHistory()

        # Vector store
        self.store = FaissVectorStore(persist_dir=persist_dir)
        self.store.load()

    def rewrite_query(self, query):
        """
        Use the LLM to rewrite a follow‑up question based on history
        so that it can be understood alone.
        """
        if not self.history.messages:
            return query

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Rewrite the question so it makes sense alone given the chat history."),
            MessagesPlaceholder("history"),
            ("human", "{input_query}")
        ])

        formatted = prompt.format(
            history=self.history.to_list(),
            input_query=query,
        )

        resp = self.llm.invoke([formatted])
        return resp.content

    def ask(self, query, top_k=3):
        # 1️⃣ Rewrite query with history
        standalone = self.rewrite_query(query)

        # 2️⃣ Retrieve docs
        docs = self.store.vectorstore.similarity_search(standalone, k=top_k)

        # 3️⃣ Build context + history
        context_text = "\n\n".join([d.page_content for d in docs])

        history_text = self.history.format_for_prompt()

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("system", "Here is conversation history:\n" + history_text),
            ("system", "Here are relevant documents:\n" + context_text),
            ("human", "{input_query}")
        ])

        formatted = prompt.format(input_query=query)

        # 4️⃣ LLM answer
        print(formatted)

        answer_resp = self.llm.invoke([formatted])
        answer = answer_resp.content

        # 5️⃣ Save history
        self.history.add_user(query)
        self.history.add_ai(answer)

        return {
            "answer": answer,
            "source_docs": [d.metadata for d in docs],
        }
