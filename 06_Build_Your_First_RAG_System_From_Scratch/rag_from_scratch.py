#!/usr/bin/env python3
"""
RAG System From Scratch - Enhanced Version
Implements a complete Retrieval-Augmented Generation pipeline with:
- Text chunking with overlap
- Persistent FAISS index
- Source citations
- Confidence scoring
- Interactive Q&A
"""

import numpy as np
import faiss
import pickle
import os
from transformers import pipeline
from sentence_transformers import SentenceTransformer

class RAGSystem:
    def __init__(self, knowledge_file="my_knowledge.txt", index_file="faiss_index.pkl"):
        self.knowledge_file = knowledge_file
        self.index_file = index_file
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_pipeline = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')
        self.chunks = []
        self.index = None

    def chunk_text(self, text, chunk_size=100, overlap=20):
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())
        return chunks

    def load_knowledge_base(self):
        """Load and chunk the knowledge base"""
        if not os.path.exists(self.knowledge_file):
            # Create sample data
            with open(self.knowledge_file, "w") as f:
                f.write("The Gemini model series was created by Google AI. ")
                f.write("It is a multimodal model, capable of understanding text, images, and audio. ")
                f.write("The first version of Gemini was released in December 2023. ")
                f.write("Gemini Pro is optimized for complex reasoning tasks. ")
                f.write("Gemini Ultra is the most capable model in the series.")

        with open(self.knowledge_file, "r") as f:
            text = f.read()

        self.chunks = self.chunk_text(text)
        return self.chunks

    def build_index(self):
        """Create or load FAISS index"""
        if os.path.exists(self.index_file):
            with open(self.index_file, 'rb') as f:
                data = pickle.load(f)
                self.index = data['index']
                self.chunks = data['chunks']
            print(f"Loaded existing index with {len(self.chunks)} chunks")
        else:
            self.load_knowledge_base()
            embeddings = self.embedding_model.encode(self.chunks)
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)

            # Save index
            with open(self.index_file, 'wb') as f:
                pickle.dump({'index': self.index, 'chunks': self.chunks}, f)
            print(f"Built new index with {len(self.chunks)} chunks")

    def retrieve(self, query, k=3):
        """Retrieve top-k relevant chunks"""
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            confidence = 1 / (1 + dist)  # Convert distance to confidence
            results.append({
                'chunk': self.chunks[idx],
                'confidence': confidence,
                'rank': i + 1
            })
        return results

    def answer_question(self, query):
        """Generate answer with source citations"""
        retrieved = self.retrieve(query)

        # Check if we have confident results
        if not retrieved or retrieved[0]['confidence'] < 0.3:
            return {
                'answer': "I don't have enough information to answer this question confidently.",
                'sources': [],
                'confidence': 0.0
            }

        # Use best chunk for QA
        best_chunk = retrieved[0]['chunk']
        result = self.qa_pipeline(question=query, context=best_chunk)

        return {
            'answer': result['answer'],
            'sources': retrieved,
            'confidence': result['score'] * retrieved[0]['confidence']
        }

    def interactive_mode(self):
        """Interactive Q&A session"""
        print("\n=== RAG System Interactive Mode ===")
        print("Ask questions about the knowledge base. Type 'quit' to exit.\n")

        while True:
            query = input("Question: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break

            if not query:
                continue

            result = self.answer_question(query)

            print(f"\nAnswer: {result['answer']}")
            print(f"Confidence: {result['confidence']:.2f}")

            if result['sources']:
                print("\nSources:")
                for i, source in enumerate(result['sources'][:2], 1):
                    print(f"{i}. {source['chunk'][:100]}... (confidence: {source['confidence']:.2f})")
            print("-" * 50)

def main():
    # Initialize RAG system
    rag = RAGSystem()
    rag.build_index()

    # Demo queries
    demo_queries = [
        "Who created the Gemini model?",
        "What capabilities does Gemini have?",
        "When was Gemini released?",
        "What is the weather like today?"  # Should return "I don't know"
    ]

    print("=== RAG System Demo ===\n")
    for query in demo_queries:
        result = rag.answer_question(query)
        print(f"Q: {query}")
        print(f"A: {result['answer']}")
        print(f"Confidence: {result['confidence']:.2f}")
        if result['sources']:
            print(f"Source: {result['sources'][0]['chunk'][:80]}...")
        print()

    # Interactive mode
    rag.interactive_mode()

if __name__ == "__main__":
    main()
