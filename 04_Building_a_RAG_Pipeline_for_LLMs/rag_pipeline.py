# Enhanced RAG Pipeline for LLMs
# Implements: Hybrid Search (BM25 + Dense), Cross-Encoder Reranking, Query Transformation

import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi
import os
import re
from typing import List, Tuple, Dict
import warnings
warnings.filterwarnings('ignore')


class EnhancedRAGPipeline:
    """
    Enhanced RAG Pipeline with:
    - Hybrid Search (BM25 + FAISS Dense Retrieval)
    - Cross-Encoder Reranking
    - Advanced Chunking with Overlap
    - Query Transformation
    """

    def __init__(self,
                 embedding_model: str = 'all-MiniLM-L6-v2',
                 cross_encoder_model: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2',
                 qa_model: str = 'distilbert-base-cased-distilled-squad',
                 chunk_size: int = 100,
                 chunk_overlap: int = 20,
                 top_k_retrieval: int = 5,
                 top_k_rerank: int = 3):
        """
        Initialize the Enhanced RAG Pipeline.

        Args:
            embedding_model: Sentence transformer model for dense embeddings
            cross_encoder_model: Cross-encoder model for reranking
            qa_model: Question answering model
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between consecutive chunks
            top_k_retrieval: Number of documents to retrieve initially
            top_k_rerank: Number of documents to keep after reranking
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k_retrieval = top_k_retrieval
        self.top_k_rerank = top_k_rerank

        # Initialize models
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer(embedding_model)

        print("Loading cross-encoder reranker...")
        self.reranker = CrossEncoder(cross_encoder_model)

        print("Loading QA model...")
        self.qa_pipeline = pipeline("question-answering", model=qa_model)

        # Storage
        self.chunks = []
        self.chunk_embeddings = None
        self.faiss_index = None
        self.bm25_index = None
        self.tokenized_chunks = []

    def create_comprehensive_knowledge_base(self) -> str:
        """Create a more comprehensive knowledge base with multiple topics."""
        knowledge = """
        France is a country in Western Europe. The capital of France is Paris, which is known for the Eiffel Tower and the Louvre Museum.
        French is the official language spoken by the majority of the population. France is famous for its wine, cheese, and cuisine.

        The United States of America is located in North America. Washington D.C. is the capital of the United States.
        The country has 50 states and is the third largest country by total area. English is the primary language spoken.

        Japan is an island nation in East Asia. Tokyo is the capital of Japan and the largest metropolitan area in the world.
        The currency of Japan is the Japanese Yen. Japan is known for its technology, anime, and traditional culture including tea ceremonies.

        The Apollo 11 mission was the first crewed mission to land on the Moon. Neil Armstrong was the first person to walk on the moon on July 20, 1969.
        Buzz Aldrin also walked on the moon during this mission while Michael Collins remained in orbit. The famous quote was "That's one small step for man, one giant leap for mankind."

        Python is a high-level programming language created by Guido van Rossum and released in 1991.
        It emphasizes code readability with its use of significant whitespace. Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.

        Machine Learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.
        Deep Learning is a subset of machine learning based on artificial neural networks with representation learning. It has been applied to computer vision, speech recognition, and natural language processing.

        The Great Wall of China is a series of fortifications built across the northern borders of ancient Chinese states.
        It was built to protect Chinese states against raids and invasions. The wall is over 13,000 miles long and is one of the Seven Wonders of the World.

        Leonardo da Vinci was an Italian polymath of the Renaissance era. He painted the Mona Lisa and The Last Supper.
        He was also an engineer, scientist, and inventor who conceptualized flying machines, tanks, and solar power centuries before they were realized.
        """
        return knowledge.strip()

    def advanced_chunking(self, text: str) -> List[str]:
        """
        Chunk text into overlapping segments with sentence-aware splitting.

        Args:
            text: Input text to chunk

        Returns:
            List of text chunks
        """
        # Split into sentences first
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence.split())

            if current_length + sentence_length <= self.chunk_size:
                current_chunk.append(sentence)
                current_length += sentence_length
            else:
                # Save current chunk
                if current_chunk:
                    chunks.append(' '.join(current_chunk))

                # Start new chunk with overlap
                if self.chunk_overlap > 0 and current_chunk:
                    # Keep last sentences for overlap
                    overlap_sentences = []
                    overlap_length = 0
                    for s in reversed(current_chunk):
                        if overlap_length + len(s.split()) <= self.chunk_overlap:
                            overlap_sentences.insert(0, s)
                            overlap_length += len(s.split())
                        else:
                            break
                    current_chunk = overlap_sentences + [sentence]
                    current_length = overlap_length + sentence_length
                else:
                    current_chunk = [sentence]
                    current_length = sentence_length

        # Don't forget the last chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def build_indices(self, chunks: List[str]):
        """
        Build both FAISS (dense) and BM25 (sparse) indices.

        Args:
            chunks: List of text chunks to index
        """
        self.chunks = chunks

        # 1. Build FAISS Dense Index
        print("Building FAISS dense index...")
        self.chunk_embeddings = self.embedding_model.encode(chunks)
        dimension = self.chunk_embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(np.array(self.chunk_embeddings).astype('float32'))

        # 2. Build BM25 Sparse Index
        print("Building BM25 sparse index...")
        self.tokenized_chunks = [chunk.lower().split() for chunk in chunks]
        self.bm25_index = BM25Okapi(self.tokenized_chunks)

        print(f"Indexed {len(chunks)} chunks")

    def hybrid_search(self, query: str, alpha: float = 0.5) -> List[Tuple[int, float]]:
        """
        Perform hybrid search combining BM25 and dense retrieval.

        Args:
            query: Search query
            alpha: Weight for combining scores (0=BM25 only, 1=Dense only)

        Returns:
            List of (chunk_index, combined_score) tuples
        """
        query_lower = query.lower()

        # BM25 scores
        bm25_scores = self.bm25_index.get_scores(query_lower.split())
        bm25_max = np.max(bm25_scores) if np.max(bm25_scores) > 0 else 1
        bm25_normalized = bm25_scores / bm25_max

        # Dense scores (convert distances to similarities)
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.faiss_index.search(query_embedding, len(self.chunks))
        dense_scores = np.zeros(len(self.chunks))
        for i, idx in enumerate(indices[0]):
            # Convert L2 distance to similarity score
            dense_scores[idx] = 1 / (1 + distances[0][i])

        # Combine scores
        combined_scores = alpha * dense_scores + (1 - alpha) * bm25_normalized

        # Get top-k
        top_indices = np.argsort(combined_scores)[::-1][:self.top_k_retrieval]
        results = [(idx, combined_scores[idx]) for idx in top_indices]

        return results

    def rerank(self, query: str, candidates: List[Tuple[int, float]]) -> List[Tuple[int, float]]:
        """
        Rerank candidates using cross-encoder.

        Args:
            query: Original query
            candidates: List of (chunk_index, score) tuples

        Returns:
            Reranked list of (chunk_index, score) tuples
        """
        # Prepare pairs for cross-encoder
        pairs = [[query, self.chunks[idx]] for idx, _ in candidates]

        # Get cross-encoder scores
        scores = self.reranker.predict(pairs)

        # Combine with original order and sort
        reranked = [(candidates[i][0], float(scores[i])) for i in range(len(candidates))]
        reranked.sort(key=lambda x: x[1], reverse=True)

        return reranked[:self.top_k_rerank]

    def transform_query(self, query: str) -> List[str]:
        """
        Transform query into multiple variations for better retrieval.

        Args:
            query: Original query

        Returns:
            List of query variations
        """
        variations = [query]

        # Simple transformations
        query_lower = query.lower()

        # Remove question words
        if query_lower.startswith('what is '):
            variations.append(query[8:])
        if query_lower.startswith('who is '):
            variations.append(query[7:])
        if query_lower.startswith('where is '):
            variations.append(query[9:])
        if query_lower.startswith('when did '):
            variations.append(query[9:])

        # Add variations
        if 'capital' in query_lower:
            variations.append(query_lower.replace('capital', 'city'))
        if 'currency' in query_lower:
            variations.append(query_lower.replace('currency', 'money'))

        return list(set(variations))

    def retrieve(self, query: str, use_hybrid: bool = True, use_reranking: bool = True) -> List[str]:
        """
        Retrieve relevant chunks for a query.

        Args:
            query: Search query
            use_hybrid: Whether to use hybrid search
            use_reranking: Whether to apply cross-encoder reranking

        Returns:
            List of retrieved text chunks
        """
        # Query transformation
        query_variations = self.transform_query(query)

        # Aggregate results from all query variations
        all_candidates = {}
        for q in query_variations:
            if use_hybrid:
                candidates = self.hybrid_search(q)
            else:
                # Dense only
                query_embedding = self.embedding_model.encode([q])
                distances, indices = self.faiss_index.search(query_embedding, self.top_k_retrieval)
                candidates = [(indices[0][i], 1/(1+distances[0][i])) for i in range(len(indices[0]))]

            for idx, score in candidates:
                if idx not in all_candidates:
                    all_candidates[idx] = score
                else:
                    all_candidates[idx] = max(all_candidates[idx], score)

        # Convert to list and sort
        candidates = sorted(all_candidates.items(), key=lambda x: x[1], reverse=True)
        candidates = candidates[:self.top_k_retrieval]

        # Rerank if enabled
        if use_reranking and candidates:
            candidates = self.rerank(query, candidates)

        # Return chunks
        return [self.chunks[idx] for idx, _ in candidates]

    def generate_answer(self, query: str, contexts: List[str]) -> Dict:
        """
        Generate answer using retrieved contexts.

        Args:
            query: User query
            contexts: Retrieved context chunks

        Returns:
            Dictionary with answer and metadata
        """
        # Combine contexts
        combined_context = " ".join(contexts)

        # Truncate if too long
        max_context_length = 512
        words = combined_context.split()
        if len(words) > max_context_length:
            combined_context = ' '.join(words[:max_context_length])

        # Generate answer
        result = self.qa_pipeline(question=query, context=combined_context)

        return {
            'answer': result['answer'],
            'confidence': result['score'],
            'contexts': contexts,
            'combined_context': combined_context
        }

    def query(self, query: str, use_hybrid: bool = True, use_reranking: bool = True) -> Dict:
        """
        Complete RAG pipeline: retrieve and generate answer.

        Args:
            query: User query
            use_hybrid: Whether to use hybrid search
            use_reranking: Whether to apply reranking

        Returns:
            Dictionary with answer and metadata
        """
        # Retrieve relevant chunks
        retrieved_contexts = self.retrieve(query, use_hybrid=use_hybrid, use_reranking=use_reranking)

        # Generate answer
        result = self.generate_answer(query, retrieved_contexts)
        result['query'] = query
        result['retrieval_method'] = 'Hybrid + Reranking' if use_hybrid and use_reranking else 'Dense'

        return result


def save_knowledge_base(text: str, filename: str = "knowledge.txt"):
    """Save knowledge base to file."""
    with open(filename, "w") as f:
        f.write(text)


def main():
    """Main execution function."""
    print("=" * 60)
    print("Enhanced RAG Pipeline Demonstration")
    print("=" * 60)

    # Initialize pipeline
    rag = EnhancedRAGPipeline(
        chunk_size=50,
        chunk_overlap=10,
        top_k_retrieval=5,
        top_k_rerank=3
    )

    # Create and save knowledge base
    knowledge_text = rag.create_comprehensive_knowledge_base()
    save_knowledge_base(knowledge_text)

    # Build indices
    chunks = rag.advanced_chunking(knowledge_text)
    rag.build_indices(chunks)

    print("\n" + "=" * 60)
    print("Testing RAG Pipeline with Multiple Queries")
    print("=" * 60)

    # Test queries
    queries = [
        "What is the capital of France?",
        "Who was the first person to walk on the moon?",
        "What is the currency of Japan?",
        "Who created Python programming language?",
        "What is machine learning?",
        "Tell me about the Great Wall of China",
        "Who painted the Mona Lisa?",
    ]

    results = []

    for i, query in enumerate(queries, 1):
        print(f"\n{'-' * 60}")
        print(f"Query {i}: {query}")
        print('-' * 60)

        # Run pipeline
        result = rag.query(query, use_hybrid=True, use_reranking=True)

        print(f"Retrieval Method: {result['retrieval_method']}")
        print(f"\nRetrieved Contexts ({len(result['contexts'])}):")
        for j, ctx in enumerate(result['contexts'], 1):
            print(f"  {j}. {ctx[:100]}...")

        print(f"\nAnswer: {result['answer']}")
        print(f"Confidence: {result['confidence']:.4f}")

        results.append(result)

    # Save output
    print("\n" + "=" * 60)
    print("Saving results to output.txt")
    print("=" * 60)

    with open("output.txt", "w") as f:
        for result in results:
            f.write(f"Query: {result['query']}\n")
            f.write(f"Retrieval Method: {result['retrieval_method']}\n")
            f.write(f"Retrieved Contexts:\n")
            for ctx in result['contexts']:
                f.write(f"  - {ctx}\n")
            f.write(f"Answer: {result['answer']}\n")
            f.write(f"Confidence: {result['confidence']:.4f}\n")
            f.write("\n" + "=" * 50 + "\n\n")

    print("Done! Results saved to output.txt")
    print(f"Total queries processed: {len(queries)}")


if __name__ == "__main__":
    main()
