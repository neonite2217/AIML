# Project 29: Building AI Agents with CrewAI

Multi-agent research-and-writing workflow powered by a local GGUF model.

## Overview

This project runs two collaborating agents:
1. `Senior Research Analyst`
2. `Tech Content Strategist`

The default runtime uses a lightweight Crew shim for reliability on Python 3.14 while keeping a switch to attempt real CrewAI.

## Requirements

- Python 3.10+
- Local GGUF model file (default):
  `/var/home/ansh/Projects/super_30/mistral-7b-instruct-v0.1.Q4_K_M.gguf`
- Python packages from `requirements.txt`

Install:

```bash
pip install -r requirements.txt
```

## Run

```bash
python -u crewai_agents.py
```

Default behavior:
- uses Lite Crew shim (`USE_REAL_CREWAI=0`)
- runs 2 sequential tasks
- writes final output to `final_result.txt`

## Optional Environment Variables

- `MODEL_PATH` (GGUF path override)
- `USE_REAL_CREWAI` (`1` to try real CrewAI import)
- `MAX_NEW_TOKENS` (default `96`)
- `TEMPERATURE` (default `0.2`)
- `CONTEXT_LENGTH` (default `1024`)
- `MAX_CONTEXT_CHARS` (default `1200`)
- `OUTPUT_PATH` (default `final_result.txt`)

Example:

```bash
MAX_NEW_TOKENS=128 OUTPUT_PATH=run1.txt python -u crewai_agents.py
```

## Verification Checklist

A successful run should:
- print model load confirmation
- execute Task 1 and Task 2 with completion logs
- print a final result block
- create `final_result.txt`

## Notes

- Real CrewAI may fail import on Python 3.14 in some dependency combinations.
- The Lite shim is the recommended default path in this environment.
