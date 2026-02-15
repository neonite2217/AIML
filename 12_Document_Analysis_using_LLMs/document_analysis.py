"""
Document Analysis V2 - Parent-Child Architecture with GPU-aware fallback
Uses PyMuPDF for extraction and ChromaDB for vector storage
"""

import os
import logging
import hashlib
import random
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field

import torch
import fitz  # PyMuPDF
from transformers import (
    T5Tokenizer, T5ForConditionalGeneration
)

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("ChromaDB not available. Install with: pip install chromadb")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProcessingConfig:
    """Configuration for document processing"""
    device: str
    parent_chunk_size: int = 1024
    child_chunk_size: int = 256
    child_overlap: int = 50
    cpu_chunk_size: int = 512
    cpu_overlap: int = 100


class HardwareDetector:
    """Detects available hardware and configures processing accordingly"""
    
    @staticmethod
    def detect() -> ProcessingConfig:
        """Detect GPU availability and return optimal config"""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if device == "cuda":
            gpu_name = torch.cuda.get_device_name(0)
            vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            logger.info(f"GPU detected: {gpu_name} with {vram:.2f}GB VRAM")
            logger.info("Using Parent-Child chunking strategy")
        else:
            logger.info("No GPU detected. Using CPU with standard chunking")
        
        return ProcessingConfig(device=device)


class RecursiveTextSplitter:
    """Recursive character-based text splitter"""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", " ", ""]
    
    def split_text(self, text: str) -> List[str]:
        """Split text recursively using multiple separators"""
        chunks = self._split_text_recursive(text, self.separators)
        return self._merge_chunks(chunks)
    
    def _split_text_recursive(self, text: str, separators: List[str]) -> List[str]:
        """Recursively split text"""
        if not text:
            return []
        
        if len(text) <= self.chunk_size:
            return [text]
        
        separator = separators[0] if separators else ""
        
        if separator:
            splits = text.split(separator)
        else:
            splits = list(text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for split in splits:
            split_len = len(split)
            
            if current_length + split_len <= self.chunk_size:
                current_chunk.append(split)
                current_length += split_len + len(separator)
            else:
                if current_chunk:
                    chunk_text = separator.join(current_chunk)
                    chunks.append(chunk_text)
                
                if split_len > self.chunk_size and len(separators) > 1:
                    sub_chunks = self._split_text_recursive(split, separators[1:])
                    chunks.extend(sub_chunks)
                    current_chunk = []
                    current_length = 0
                else:
                    current_chunk = [split]
                    current_length = split_len
        
        if current_chunk:
            chunks.append(separator.join(current_chunk))
        
        return chunks
    
    def _merge_chunks(self, chunks: List[str]) -> List[str]:
        """Merge chunks with overlap"""
        if not chunks:
            return []
        
        merged = [chunks[0]]
        
        for i in range(1, len(chunks)):
            if self.chunk_overlap > 0 and len(merged[-1]) > self.chunk_overlap:
                overlap_text = merged[-1][-self.chunk_overlap:]
                merged.append(overlap_text + chunks[i])
            else:
                merged.append(chunks[i])
        
        return merged


class DocumentExtractor:
    """Extract text from various document formats"""
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from file based on extension"""
        logger.info(f"Extracting text from: {file_path}")
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == ".pdf":
                doc = fitz.open(file_path)
                full_text = []
                for page in doc:
                    full_text.append(page.get_text("text"))
                doc.close()
                result = "\n\n".join(full_text)
            elif ext in [".txt", ".md"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    result = f.read()
            else:
                raise ValueError(f"Unsupported file format: {ext}")
                
            logger.info(f"Extracted {len(result)} characters")
            return result
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise


class ParentChildChunker:
    """Creates parent-child chunk relationships"""
    
    def __init__(self, config: ProcessingConfig):
        self.config = config
        self.parent_splitter = RecursiveTextSplitter(
            chunk_size=config.parent_chunk_size,
            chunk_overlap=0
        )
        self.child_splitter = RecursiveTextSplitter(
            chunk_size=config.child_chunk_size,
            chunk_overlap=config.child_overlap
        )
    
    def create_chunks(self, text: str) -> List[Dict[str, Any]]:
        """Create parent-child chunk structure"""
        logger.info("Creating parent-child chunks...")
        
        parents = self.parent_splitter.split_text(text)
        final_chunks = []
        
        for i, parent in enumerate(parents):
            children = self.child_splitter.split_text(parent)
            
            for j, child in enumerate(children):
                final_chunks.append({
                    "content": child,
                    "parent_id": f"parent_{i}",
                    "child_id": f"parent_{i}_child_{j}",
                    "parent_context": parent
                })
        
        logger.info(f"Created {len(final_chunks)} child chunks from {len(parents)} parents")
        return final_chunks


class StandardChunker:
    """Standard recursive chunking for CPU fallback"""
    
    def __init__(self, config: ProcessingConfig):
        self.splitter = RecursiveTextSplitter(
            chunk_size=config.cpu_chunk_size,
            chunk_overlap=config.cpu_overlap
        )
    
    def create_chunks(self, text: str) -> List[str]:
        """Create standard chunks"""
        logger.info("Creating standard chunks...")
        chunks = self.splitter.split_text(text)
        logger.info(f"Created {len(chunks)} chunks")
        return chunks


class VectorStore:
    """Manages ChromaDB vector storage"""
    
    def __init__(self, collection_name: str = "documents", persist_dir: str = "./chroma_db"):
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB not installed")

        # Disable anonymous telemetry to avoid noisy retry logs in offline/restricted environments.
        try:
            self.client = chromadb.PersistentClient(
                path=persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )
        except TypeError:
            # Fallback for Chroma versions with different PersistentClient signatures.
            self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        logger.info(f"Initialized ChromaDB at {persist_dir}")
    
    def add_parent_child_chunks(self, chunks: List[Dict[str, Any]]):
        """Add parent-child chunks to vector store"""
        logger.info(f"Adding {len(chunks)} chunks to vector store...")
        
        ids = [chunk["child_id"] for chunk in chunks]
        documents = [chunk["content"] for chunk in chunks]
        metadatas = [
            {
                "parent_id": chunk["parent_id"],
                "parent_context": chunk["parent_context"]
            }
            for chunk in chunks
        ]
        
        self.collection.add(ids=ids, documents=documents, metadatas=metadatas)
        logger.info("Chunks added successfully")
    
    def add_standard_chunks(self, chunks: List[str]):
        """Add standard chunks to vector store"""
        logger.info(f"Adding {len(chunks)} chunks to vector store...")
        
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        documents = chunks
        metadatas = [{"chunk_id": i} for i in range(len(chunks))]
        
        self.collection.add(ids=ids, documents=documents, metadatas=metadatas)
        logger.info("Chunks added successfully")
    
    def query(self, query_text: str, n_results: int = 3) -> Dict[str, Any]:
        """Query vector store and return results"""
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        return results
    
    def clear(self):
        """Clear all data from collection"""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(name=self.collection.name)
        logger.info("Vector store cleared")


class Generator:
    """Generates answers using FLAN-T5 model"""
    
    def __init__(self, model_name: str = "google/flan-t5-large", device: str = "cpu"):
        logger.info(f"Initializing Generator with model: {model_name} on {device}")
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)
        self.device = device

    def generate_answer(self, question: str, context: str) -> Tuple[str, float]:
        """Generate answer from question and context"""
        # Enhance short questions to prevent echoing and encourage detail
        enhanced_q = question
        if len(question.strip().split()) <= 3:
            enhanced_q = f"Provide a comprehensive summary of what the document states about '{question}'."
            
        prompt = f"System: You are an expert document analyst. Answer the user question based ONLY on the provided context.\n\nContext: {context}\n\nUser Question: {enhanced_q}\n\nProfessional Answer:"
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                num_beams=4,
                length_penalty=1.5,
                no_repeat_ngram_size=3,
                early_stopping=True,
                return_dict_in_generate=True,
                output_scores=True
            )
        
        answer = self.tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
        
        # Calculate confidence from sequence score
        confidence = 0.85
        if hasattr(outputs, 'sequences_scores'):
            confidence = torch.exp(outputs.sequences_scores[0]).item()
            
        return answer, confidence


class DocumentAnalysisV2:
    """Main system orchestrator with hardware-aware processing"""
    
    def __init__(self):
        self.config = HardwareDetector.detect()
        self.extractor = DocumentExtractor()
        self.vector_store = None
        self.generator = None
        self.current_text = None
        
        if CHROMADB_AVAILABLE:
            self.vector_store = VectorStore()
            
        self.generator = Generator(device=self.config.device)
    
    def process_document(self, pdf_path: str) -> Dict[str, Any]:
        """Process document with hardware-appropriate strategy"""
        logger.info(f"=== Processing document: {pdf_path} ===")
        
        # Extract text
        text = self.extractor.extract_text(pdf_path)
        self.current_text = text
        
        # Choose chunking strategy based on hardware
        if self.config.device == "cuda":
            chunker = ParentChildChunker(self.config)
            chunks = chunker.create_chunks(text)
            
            if self.vector_store:
                self.vector_store.clear() # Clear old data
                self.vector_store.add_parent_child_chunks(chunks)
            
            return {
                "strategy": "parent-child",
                "device": "GPU",
                "num_chunks": len(chunks),
                "num_parents": len(set(c["parent_id"] for c in chunks)),
                "chunks": chunks
            }
        else:
            chunker = StandardChunker(self.config)
            chunks = chunker.create_chunks(text)
            
            if self.vector_store:
                self.vector_store.clear() # Clear old data
                self.vector_store.add_standard_chunks(chunks)
            
            return {
                "strategy": "standard",
                "device": "CPU",
                "num_chunks": len(chunks),
                "chunks": chunks
            }
    
    def query(self, question: str, n_results: int = 3) -> Dict[str, Any]:
        """Query the document and generate answer"""
        if not self.vector_store:
            raise RuntimeError("Vector store not available")
        
        results = self.vector_store.query(question, n_results)
        
        # Extract context from metadata (preferred) or direct documents
        if results['metadatas'][0] and 'parent_context' in results['metadatas'][0][0]:
            unique_parents = []
            seen = set()
            for m in results['metadatas'][0]:
                pc = m['parent_context']
                if pc not in seen:
                    unique_parents.append(pc)
                    seen.add(pc)
            context = "\n---\n".join(unique_parents)
            source_type = "Parent Context"
        else:
            context = "\n---\n".join(results['documents'][0])
            source_type = "Direct Chunks"
        
        # Generate answer
        answer, confidence = self.generator.generate_answer(question, context)
        
        return {
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "context": context,
            "source_type": source_type,
            "num_results": len(results['documents'][0]),
            "results": results
        }

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter as page_size

def create_dummy_pdf():
    """Create a randomized sample PDF for testing."""
    # Always overwrite for randomization
    c = canvas.Canvas("sample_document.pdf", pagesize=page_size)

    # Randomize document type
    doc_types = [
        ("Terms of Service", ["Privacy Policy", "User Conduct", "Acceptance", "Termination"]),
        ("Employment Agreement", ["Compensation", "Confidentiality", "Term", "Benefits"]),
        ("Rental Agreement", ["Lease Term", "Security Deposit", "Maintenance", "Rules"]),
        ("Consulting Contract", ["Scope of Work", "Payment", "Ownership", "Independent Contractor"])
    ]
    
    title, sections = random.choice(doc_types)
    companies = ["TechNova Solutions", "Global Synergy Corp", "Apex Industries", "Quantum Systems"]
    company = random.choice(companies)
    date = f"{random.randint(1,28)} {random.choice(['Jan', 'Feb', 'Mar', 'Apr'])} 202{random.randint(4,6)}"

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 800, f"{title} - {company}")

    c.setFont("Helvetica", 12)
    y = 760

    paragraphs = [
        f"This {title} is established on {date} between {company} and the User.",
        ""
    ]
    
    for i, section in enumerate(sections):
        paragraphs.append(f"{i+1}. {section.upper()}")
        paragraphs.append(f"This section details the specific requirements and obligations regarding {section.lower()}.")
        paragraphs.append(f"The parties agree to abide by all clauses mentioned in the {section.lower()} documentation.")
        paragraphs.append("")

    paragraphs.extend([
        "5. CONTACT INFORMATION",
        f"For questions, contact {company} at: support@{company.lower().replace(' ', '')}.com",
        "Office Location: 123 Business Way, Silicon Valley, CA 94025"
    ])

    for para in paragraphs:
        c.drawString(72, y, para)
        y -= 20
        if y < 50:
            c.showPage()
            y = 800

    c.save()
    logger.info(f"Created randomized sample_document.pdf ({title})")
