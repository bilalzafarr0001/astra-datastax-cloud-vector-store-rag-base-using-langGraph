"""The whole RAG project in one file.

Run:  uv run rag.py

The 4 steps, in order (each step is one LangGraph "node"):
  1. read_pdf       read the PDF and cut its text into small chunks
  2. save_to_astra  turn each chunk into numbers (embedding) and save it in Astra DB
  3. search_astra   turn your question into numbers and find the 3 closest chunks
  4. ask_ai         send your question + those chunks to the Groq AI to write the answer
"""

import os
from typing import TypedDict

from astrapy import DataAPIClient
from dotenv import load_dotenv
from fastembed import TextEmbedding
from groq import Groq
from langgraph.graph import END, START, StateGraph
from pypdf import PdfReader

# ----- Setup: load the keys and connect to the services -----

load_dotenv()  # reads your keys from the .env file

embedding_model = TextEmbedding("BAAI/bge-small-en-v1.5")  # free; turns text into 384 numbers
ai = Groq()  # the AI that writes the answer (uses GROQ_API_KEY)

database = DataAPIClient().get_database(  # your practice_db database
    os.environ["ASTRA_DB_API_ENDPOINT"],
    token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
)
collection = database.create_collection(  # a "table" inside practice_db for our chunks
    "rag_documents",
    definition={"vector": {"dimension": 384, "metric": "cosine"}},
)


# ----- State: the "box" of data that LangGraph passes from step to step -----

class State(TypedDict):
    question: str  # your question
    chunks: list[str]  # small pieces of the PDF text
    found: list[str]  # the chunks Astra DB found for your question
    answer: str  # the AI's answer


# ----- The 4 steps -----

def read_pdf(state: State):
    reader = PdfReader("data/company_handbook.pdf")
    words = " ".join(page.extract_text() for page in reader.pages).split()
    # 120 words per chunk; each chunk repeats the last 20 words of the previous one
    chunks = [" ".join(words[i : i + 120]) for i in range(0, len(words), 100)]
    print(f"1. read_pdf:      cut the PDF into {len(chunks)} chunks")
    return {"chunks": chunks}


def save_to_astra(state: State):
    vectors = embedding_model.embed(state["chunks"])
    collection.delete_many({})  # remove the old chunks so we don't save duplicates
    collection.insert_many(
        [{"text": chunk, "$vector": vector.tolist()} for chunk, vector in zip(state["chunks"], vectors)]
    )
    print(f"2. save_to_astra: saved {len(state['chunks'])} chunks with their embeddings")
    return {}


def search_astra(state: State):
    question_vector = list(embedding_model.embed([state["question"]]))[0].tolist()
    results = collection.find(sort={"$vector": question_vector}, limit=3)
    found = [doc["text"] for doc in results]
    print(f"3. search_astra:  found the {len(found)} closest chunks")
    return {"found": found}


def ask_ai(state: State):
    text = "\n\n".join(state["found"])
    response = ai.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "Answer using only this text. If the answer is not in it, say you don't know.\n\n" + text,
            },
            {"role": "user", "content": state["question"]},
        ],
    )
    print("4. ask_ai:        got the answer")
    return {"answer": response.choices[0].message.content}


# ----- Connect the steps in order with LangGraph -----

graph = StateGraph(State)
graph.add_node("read_pdf", read_pdf)
graph.add_node("save_to_astra", save_to_astra)
graph.add_node("search_astra", search_astra)
graph.add_node("ask_ai", ask_ai)

graph.add_edge(START, "read_pdf")
graph.add_edge("read_pdf", "save_to_astra")
graph.add_edge("save_to_astra", "search_astra")
graph.add_edge("search_astra", "ask_ai")
graph.add_edge("ask_ai", END)

app = graph.compile()


# ----- Run it -----

question = input("Ask a question about the PDF: ")
result = app.invoke({"question": question})
print("\nAnswer:", result["answer"])
