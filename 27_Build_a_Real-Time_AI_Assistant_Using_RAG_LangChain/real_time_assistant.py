# Lab Project: Build a Real-Time AI Assistant Using RAG + LangChain

# You may need to install these packages first:
# pip install langchain langchain_community langchain_core duckduckgo-search
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import DuckDuckGoSearchRun
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_output.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 1. Pull and run a local LLM with Ollama
# Using Qwen3.5 model (available in Ollama)
# This script assumes the Ollama server is running.
try:
    llm = ChatOllama(model="qwen3.5:latest", temperature=0.7)
    # Ping the model to see if it's alive
    llm.invoke("Hi")
    logger.info("Ollama connection successful with Qwen3.5 model.")
except Exception as e:
    logger.error(f"Failed to connect to Ollama: {e}")
    print("Please ensure Ollama is installed, running, and you have pulled a model (e.g., `ollama pull qwen3.5`).")
    llm = None

if llm:
    # 2. Create a search tool component
    search = DuckDuckGoSearchRun()

    # 3. Design prompt template
    template = """
    You are a helpful AI assistant with real-time web search capabilities.
    Use the following search results to answer the question at the end.
    If the search results don't contain enough information, use your general knowledge but mention that the search results were limited.
    Be concise and factual in your response.
    
    Search Results:
    {context}
    
    Question: {question}
    
    Helpful Answer:
    """
    prompt = PromptTemplate.from_template(template)

    # 4. Build LCEL chain
    # The chain will first run the search, then pass the search results and the original question
    # to the prompt, which then goes to the LLM.
    chain = (
        {"context": (lambda x: search.run(x["question"])), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 5. Wrap in a loop for interactive Q&A
    def run_assistant():
        logger.info("\n=== Starting the Real-Time AI Assistant ===")
        print("\nStarting the Real-Time AI Assistant...")
        print("Try asking: 'What were the main announcements at the last Apple event?'")
        logger.info("Assistant ready for queries. Example: 'What were the main announcements at the last Apple event?'")
        
        while True:
            query = input("\nEnter your question (or 'exit' to quit): ")
            if query.lower() == 'exit':
                logger.info("User exited the assistant.")
                break
            if not query.strip():
                continue

            logger.info(f"\n--- User Query: {query} ---")
            print("\nThinking...")
            logger.info("Executing RAG pipeline: search -> prompt -> LLM generation")
            
            # Streaming the output for a better user experience
            try:
                full_response = ""
                logger.info("Streaming response from LLM:")
                for chunk in chain.stream({"question": query}):
                    print(chunk, end="", flush=True)
                    full_response += chunk
                logger.info(f"Response complete. Total length: {len(full_response)} characters")
            except Exception as e:
                logger.error(f"Error during response generation: {e}")
                print(f"\nAn error occurred: {e}")
            print("\n")


    # Uncomment the line below to run the interactive loop
    # run_assistant()

    # For non-interactive demonstration:
    logger.info("\n=== Running Non-Interactive Demonstration ===")
    print("\n--- Running Non-Interactive Demonstration ---")
    
    demo_questions = [
        "What is the latest news about OpenAI?",
        "What are the recent developments in quantum computing?",
        "What were the main announcements at the last Apple event?"
    ]
    
    for demo_question in demo_questions:
        logger.info(f"\n{'='*60}")
        logger.info(f"Demonstration Query: {demo_question}")
        print(f"\nDemonstration query: {demo_question}")
        
        try:
            # First, show the search results
            logger.info("Step 1: Performing web search...")
            search_results = search.run(demo_question)
            logger.info(f"Search Results Retrieved (length: {len(search_results)} chars)")
            logger.info(f"Search Results Preview: {search_results[:300]}...")
            
            # Then, generate the answer
            logger.info("Step 2: Generating answer with LLM...")
            print("\nSearching and generating response...")
            response = chain.invoke({"question": demo_question})
            
            logger.info(f"Step 3: Final Response Generated (length: {len(response)} chars)")
            logger.info(f"Response: {response}")
            print("\nResponse:")
            print(response)
            logger.info(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"Chain invocation failed: {e}")
            print(f"\nChain invocation failed. This might be due to Ollama not running. Error: {e}")
            logger.info(f"{'='*60}\n")
    
    logger.info("\n=== Demonstration Complete ===")
    print("\n=== Demonstration Complete ===")
    print(f"Output logs saved to: rag_output.log")


else:
    logger.error("Skipping LangChain execution because Ollama is not available.")
    print("\nSkipping LangChain execution because Ollama is not available.")
