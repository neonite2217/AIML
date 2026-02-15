#!/usr/bin/env python3
"""
CLI tool to test the new Document Analysis V2 system
"""

import argparse
import sys
from document_analysis import DocumentAnalysisV2, CHROMADB_AVAILABLE, create_dummy_pdf


def main():
    parser = argparse.ArgumentParser(description="Document Analysis V2 CLI Tool")
    parser.add_argument("command", choices=["process", "query", "info", "create-sample"],
                       help="Command to execute")
    parser.add_argument("--pdf", type=str, help="Path to PDF file")
    parser.add_argument("--question", type=str, help="Question to ask")
    parser.add_argument("--results", type=int, default=3, help="Number of results to return")
    
    args = parser.parse_args()
    
    if args.command == "create-sample":
        print("Creating sample PDF...")
        create_dummy_pdf()
        print("✓ Sample PDF created: sample_document.pdf")
        return
    
    if args.command == "info":
        print("\n=== System Information ===")
        system = DocumentAnalysisV2()
        print(f"Device: {system.config.device}")
        print(f"ChromaDB Available: {CHROMADB_AVAILABLE}")
        
        if system.config.device == "cuda":
            print(f"Strategy: Parent-Child")
            print(f"Parent Chunk Size: {system.config.parent_chunk_size}")
            print(f"Child Chunk Size: {system.config.child_chunk_size}")
            print(f"Child Overlap: {system.config.child_overlap}")
        else:
            print(f"Strategy: Standard Recursive")
            print(f"Chunk Size: {system.config.cpu_chunk_size}")
            print(f"Overlap: {system.config.cpu_overlap}")
        return
    
    if args.command == "process":
        if not args.pdf:
            print("Error: --pdf argument required for process command")
            sys.exit(1)
        
        print(f"\n=== Processing Document ===")
        print(f"File: {args.pdf}")
        
        system = DocumentAnalysisV2()
        result = system.process_document(args.pdf)
        
        print(f"\n✓ Processing Complete!")
        print(f"Strategy: {result['strategy']}")
        print(f"Device: {result['device']}")
        print(f"Total Chunks: {result['num_chunks']}")
        
        if result['strategy'] == 'parent-child':
            print(f"Parent Chunks: {result['num_parents']}")
        
        print("\nSample chunks:")
        for i, chunk in enumerate(result['chunks'][:3]):
            if isinstance(chunk, dict):
                print(f"\n[Child {i+1}] (Parent: {chunk['parent_id']})")
                print(f"Content: {chunk['content'][:100]}...")
            else:
                print(f"\n[Chunk {i+1}]")
                print(f"Content: {chunk[:100]}...")
        
        return
    
    if args.command == "query":
        if not args.pdf:
            print("Error: --pdf argument required for query command")
            sys.exit(1)
        if not args.question:
            print("Error: --question argument required for query command")
            sys.exit(1)
        
        print(f"\n=== Processing and Querying Document ===")
        print(f"File: {args.pdf}")
        print(f"Question: {args.question}")
        
        system = DocumentAnalysisV2()
        
        # Process document
        print("\nProcessing document...")
        process_result = system.process_document(args.pdf)
        print(f"✓ Processed {process_result['num_chunks']} chunks using {process_result['device']}")
        
        # Query
        print("\nQuerying...")
        query_result = system.query(args.question, args.results)
        
        print(f"\n=== Query Results ===")
        print(f"Question: {query_result['question']}")
        print(f"Retrieved {query_result['num_results']} relevant chunks")
        print(f"\nContext:")
        print("-" * 80)
        print(query_result['context'])
        print("-" * 80)
        
        return


if __name__ == "__main__":
    main()
