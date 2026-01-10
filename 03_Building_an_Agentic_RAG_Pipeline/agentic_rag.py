# Lab Project: Building an Agentic RAG Pipeline
# Models: sentence-transformers/all-MiniLM-L6-v2 (embeddings), google/flan-t5-base (LLM)
# No paid APIs — fully local/free.

import os
import warnings
warnings.filterwarnings("ignore")

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch


def create_dummy_pdf(pdf_path="agentic_rag_doc.pdf"):
    if not os.path.exists(pdf_path):
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        c = canvas.Canvas(pdf_path, pagesize=letter)
        lines = [
            "The capital of France is Paris.",
            "Paris is famous for the Eiffel Tower and the Louvre Museum.",
            "France is a country in Western Europe with a population of about 68 million.",
            "The French Revolution began in 1789 and transformed French society.",
        ]
        y = 800
        for line in lines:
            c.drawString(72, y, line)
            y -= 20
        c.save()
        print(f"Created dummy PDF: {pdf_path}")
    return pdf_path


def build_vectorstore(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vs = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
    print(f"Indexed {len(chunks)} chunks into Chroma.")
    return vs


def build_llm():
    print("Loading google/flan-t5-base...")
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
    model.eval()
    print("LLM ready.")
    return tokenizer, model


def generate(prompt: str, tokenizer, model, max_new_tokens=100) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


def query_router(query: str) -> str:
    """Keyword-based router: 'rag' if query needs document knowledge, else 'direct'."""
    rag_keywords = ["capital", "france", "paris", "eiffel", "louvre", "population",
                    "europe", "revolution", "french", "museum"]
    if any(kw in query.lower() for kw in rag_keywords):
        return "rag"
    return "direct"


def rag_answer(query: str, vectorstore, tokenizer, model) -> str:
    docs = vectorstore.similarity_search(query, k=2)
    context = " ".join(d.page_content for d in docs)
    prompt = f"Answer based on context.\nContext: {context}\nQuestion: {query}\nAnswer:"
    return generate(prompt, tokenizer, model)


def direct_answer(query: str, tokenizer, model) -> str:
    return generate(query, tokenizer, model)


def main():
    pdf_path = create_dummy_pdf()
    vectorstore = build_vectorstore(pdf_path)
    tokenizer, model = build_llm()

    queries = [
        "What is 2 + 2?",
        "What is the capital of France?",
        "Tell me about the Eiffel Tower.",
        "What color is the sky?",
        "When did the French Revolution begin?",
    ]

    print("\n" + "=" * 60)
    print("AGENTIC RAG PIPELINE — QUERY ROUTING DEMO")
    print("=" * 60)

    for query in queries:
        route = query_router(query)
        print(f"\nQuery  : {query}")
        print(f"Route  : {route.upper()}")
        try:
            if route == "rag":
                answer = rag_answer(query, vectorstore, tokenizer, model)
            else:
                answer = direct_answer(query, tokenizer, model)
        except Exception as e:
            answer = f"[Error: {e}]"
        print(f"Answer : {answer}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
