# Lab Project: Building AI Agents with CrewAI
import os
import sys
import time
import warnings

sys.stdout.reconfigure(line_buffering=True)

MODEL_PATH = os.getenv(
    "MODEL_PATH", "/var/home/ansh/Projects/super_30/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
)
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "96"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
CONTEXT_LENGTH = int(os.getenv("CONTEXT_LENGTH", "1024"))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "1200"))
USE_REAL_CREWAI = os.getenv("USE_REAL_CREWAI", "0") == "1"
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "final_result.txt")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found at: {MODEL_PATH}\n"
        "Set MODEL_PATH to your GGUF model path and re-run."
    )

print(f"Loading model from {MODEL_PATH}...")
warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
)

from langchain_community.llms import CTransformers

llm = CTransformers(
    model=MODEL_PATH,
    model_type="llama",
    config={
        "max_new_tokens": MAX_NEW_TOKENS,
        "temperature": TEMPERATURE,
        "context_length": CONTEXT_LENGTH,
    },
)
print(
    f"Model loaded. Settings: max_new_tokens={MAX_NEW_TOKENS}, "
    f"temperature={TEMPERATURE}, context_length={CONTEXT_LENGTH}"
)


def truncate_context(text):
    if len(text) <= MAX_CONTEXT_CHARS:
        return text
    return text[:MAX_CONTEXT_CHARS] + "\n...[truncated for speed]..."


def make_prompt(role, goal, backstory, task_description, context):
    context = truncate_context(context)
    return (
        f"System: {backstory}\n"
        f"Role: {role}\n"
        f"Goal: {goal}\n"
        f"Task: {task_description}\n"
        "Output format: concise bullet points only.\n"
        f"Context:\n{context}\n"
        "Response:\n"
    )


def clean_response(text):
    text = str(text).strip()
    if not text:
        return text
    last_terminal = max(text.rfind("."), text.rfind("!"), text.rfind("?"))
    if last_terminal > 40:
        return text[: last_terminal + 1]
    return text


class LiteAgent:
    def __init__(self, role, goal, backstory, llm, verbose=True):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = llm
        self.verbose = verbose

    def execute_task(self, task_description, context=""):
        if self.verbose:
            print(f"\n[Agent: {self.role}] starting task...")
        prompt = make_prompt(self.role, self.goal, self.backstory, task_description, context)
        started = time.time()
        response = clean_response(self.llm.invoke(prompt))
        elapsed = time.time() - started
        if self.verbose:
            print(f"[Agent: {self.role}] completed task in {elapsed:.1f}s.")
        return response


class LiteTask:
    def __init__(self, description, agent, expected_output):
        self.description = description
        self.agent = agent
        self.expected_output = expected_output
        self.output = None


class LiteCrew:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    def kickoff(self):
        last_output = ""
        for i, task in enumerate(self.tasks):
            print(f"\n--- Executing Task {i + 1} ---")
            task.output = task.agent.execute_task(task.description, context=last_output)
            last_output = task.output
        return last_output


if USE_REAL_CREWAI:
    try:
        print("USE_REAL_CREWAI=1 set. Attempting real CrewAI import...")
        from crewai import Agent, Crew, Task

        agent_cls = Agent
        task_cls = Task
        crew_cls = Crew
        using_real_crewai = True
        print("Using REAL CrewAI.")
    except Exception as exc:
        print(f"Real CrewAI import failed: {type(exc).__name__}: {exc}")
        print("Falling back to Lite Crew shim.")
        agent_cls = LiteAgent
        task_cls = LiteTask
        crew_cls = LiteCrew
        using_real_crewai = False
else:
    print("Using Lite Crew shim (set USE_REAL_CREWAI=1 to try real CrewAI).")
    agent_cls = LiteAgent
    task_cls = LiteTask
    crew_cls = LiteCrew
    using_real_crewai = False


researcher = agent_cls(
    role="Senior Research Analyst",
    goal="Identify key AI trends in 2024",
    backstory="You are a data-driven analyst at a top tech firm.",
    llm=llm,
    verbose=True,
)

writer = agent_cls(
    role="Tech Content Strategist",
    goal="Summarize research into a blog post",
    backstory="You are an expert writer who specializes in tech blogging.",
    llm=llm,
    verbose=True,
)

task1 = task_cls(
    description=(
        "Analyze the top 3 AI trends of 2024 and provide short bullets with one-line impact for each."
    ),
    agent=researcher,
    expected_output="3 concise trend bullets.",
)

task2 = task_cls(
    description=(
        "Using the trend bullets, write a short blog post intro and closing paragraph for technical readers."
    ),
    agent=writer,
    expected_output="A concise blog intro and summary.",
)

print("\nStarting the Crew Kickoff...\n")
crew = crew_cls(agents=[researcher, writer], tasks=[task1, task2])
result = crew.kickoff()

print("\n########################")
print("## Final Result:")
print("########################\n")
print(result)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("Framework: " + ("CrewAI" if using_real_crewai else "LiteCrewShim") + "\n\n")
    f.write(result.strip() + "\n")
print(f"\nSaved final output to {OUTPUT_PATH}")
