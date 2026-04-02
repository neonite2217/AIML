# Lab Project: Build a Multi-Agent System With LangGraph

# You may need to install these packages first:
# pip install langchain langchain_community langchain_core langgraph
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict
from langgraph.graph import StateGraph, END

# This script assumes the Ollama server is running.
try:
    llm = OllamaLLM(model="qwen3.5:latest")
    llm.invoke("Hi")
    print("Ollama connection successful.")
except Exception as e:
    print(f"Failed to connect to Ollama: {e}")
    llm = None

if llm:
    # 1. Define shared state
    class AgentState(TypedDict):
        topic: str
        research_notes: str
        final_output: str

    # 2. Implement Researcher node
    def researcher_node(state: AgentState):
        print("--- Researcher Node ---")
        prompt = PromptTemplate.from_template("Give me a brief overview of the topic: {topic}")
        chain = prompt | llm | StrOutputParser()
        research_notes = chain.invoke({"topic": state['topic']})
        print(f"Research Notes: {research_notes[:100]}...")
        return {"research_notes": research_notes}

    # 3. Implement Writer node
    def writer_node(state: AgentState):
        print("--- Writer Node ---")
        prompt = PromptTemplate.from_template(
            "Based on these notes, write a short blog post:\n\n{research_notes}"
        )
        chain = prompt | llm | StrOutputParser()
        final_output = chain.invoke({"research_notes": state['research_notes']})
        print("Blog post generated.")
        return {"final_output": final_output}

    # 4. Build StateGraph
    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)

    # Define edges
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)

    # 5. Compile graph and invoke
    app = workflow.compile()
    initial_state = {"topic": "The latest advancements in AI"}
    
    print("\nInvoking the multi-agent system...")
    try:
        final_state = app.invoke(initial_state)
        print("\n--- Final Output ---")
        print(final_state['final_output'])
    except Exception as e:
        print(f"Graph invocation failed. Error: {e}")

else:
    print("Skipping LangGraph execution because Ollama is not available.")
