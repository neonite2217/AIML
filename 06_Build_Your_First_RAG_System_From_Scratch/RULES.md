# RULES.md — Agent Operating Rules
> **Read this file completely before touching anything in this project.**
> This is the law for any AI agent, LLM, or automated tool working here.
> Violation of these rules will result in broken projects and lost work.

---

## PHASE 0 — ORIENTATION (before you write a single line of code)

### 0.1 — Discover the Repository
```bash
ls -la          # See root structure
cat README.md   # Understand what this project is
```
Identify the project type by scanning for these manifest files **in order**:

| Language | Files to look for |
|---|---|
| Python | `pyproject.toml` → `requirements.txt` → `setup.py` |
| Node/JS/TS | `package.json` |
| Go | `go.mod` |
| Rust | `Cargo.toml` |
| Java | `pom.xml` → `build.gradle(.kts)` |
| .NET / C# | `*.csproj` → `*.sln` |
| C / C++ | `CMakeLists.txt` → `Makefile` |
| Other | `Makefile`, `Dockerfile`, `docker-compose.yml` |

- Note the **dominant language** and use only its build tool for the entire session.
- If the project is polyglot, note all stacks before starting.

### 0.2 — Analyse the Codebase First
Before planning any work:
- Read the existing source files in `src/` or root.
- Understand the data flow, entry points, and module structure.
- Check for existing patterns (naming, error handling, logging) and **match them**.
- Never introduce a new pattern without documenting why in `docs/agent_log.md`.

### 0.3 — Find the Smoke Test
Locate the command that proves the project currently works:

| Stack | Command |
|---|---|
| Python | `python -m pytest` or `python main.py` |
| Node | `npm test` or `node index.js` |
| Go | `go test ./...` or `go run .` |
| Rust | `cargo test` or `cargo run` |
| Java | `mvn test` or `gradle test` |
| Web | Open in browser / `npm run dev` |

**If you cannot find it → ask the user before proceeding. Do not guess.**

### 0.4 — Check for Existing Tracking Files
Look for these in order:
- `docs/tasks.md` → your **source of truth** for what needs doing. Read it fully.
- `docs/agent_log.md` → read the last 5 entries to understand recent context.
- `CHANGELOG.md` or `docs/CHANGELOG.md` → understand version history.
- `README.md` → understand the project's stated purpose and setup.

If none of these exist → **create them** under `docs/` before starting work (see Phase 3).

### 0.5 — Backup Before Risk
Before modifying **any** existing file (especially configs, build files, core logic):
```bash
cp path/to/file path/to/file.$(date +%Y%m%d_%H%M%S).bak
```
- Store all backups under `backups/YYYY-MM-DD/`.
- Add the backup path to `docs/agent_log.md`.
- `backups/` must be listed in `.gitignore`.

---

## PHASE 1 — PLANNING (do not code yet)

### 1.1 — State the Task Clearly
Write this sentence before starting, and log it as the first line of your session entry:
> "I will **[action]** **[target]** so that **[outcome]**."

Example: *"I will add input validation to the API endpoint so that malformed requests return a 400 instead of crashing."*

### 1.2 — List Files to Touch
- Identify the **exact files** you will create or modify.
- If creating **more than 2 new files** → ask for user approval first.
- Every new file must have a direct functional purpose. No decorative or placeholder files.

### 1.3 — Define Success Criteria
Answer these three questions before writing code:
1. What command proves it works? (from 0.3)
2. What specific behaviour will change?
3. What must **NOT** change? (your regression guard)

### 1.4 — Document Your Approach
- Will you modify existing code or create new modules?
- If you change approach mid-task (e.g., sync → async, REST → GraphQL), stop and document **why** in `docs/agent_log.md` before continuing.

---

## PHASE 2 — DEPENDENCY MANAGEMENT

### 2.1 — Detect Missing Dependencies
- Run the smoke test first. If it fails with "module not found":
  - Note the exact package name from the error.
  - Confirm it is absent from the manifest before adding it.
  - Never add a dependency from memory — verify the package name and version.

### 2.2 — Update the Manifest
- Add **only** the missing package with a minimum version pin:
  - ✅ `package>=1.2.0`
  - ❌ `package==1.2.0` (avoid pinning exact versions unless required)
- Never dump transitive dependencies into the manifest.
- Never install packages globally on the host system.

### 2.3 — Setup Script
If no setup script exists, create both:
- `scripts/setup.sh` (POSIX/Linux/macOS)
- `scripts/setup.ps1` (Windows PowerShell)

Scripts must be:
- **Idempotent** — safe to run multiple times without side effects.
- **Idiomatic** — uses the ecosystem's standard package manager.
- **Verbose** — prints what it is doing at each step.
- **Self-verifying** — runs a post-install check at the end.

---

## PHASE 3 — DOCUMENTATION REQUIREMENTS

All documentation lives under `docs/`. Create the folder if it does not exist.

### 3.1 — Mandatory Files

| File | Purpose | Create if missing? |
|---|---|---|
| `README.md` | Root-level: setup, usage, architecture overview | ✅ Yes |
| `docs/agent_log.md` | Chronological log of all agent sessions | ✅ Yes |
| `docs/CHANGELOG.md` | All notable changes, versioned | ✅ Yes |
| `docs/tasks.md` | Active task list and backlog | ✅ Yes |
| `docs/architecture.md` | System structure, components, data flow | ✅ Yes |
| `docs/tech_stack.md` | Languages, frameworks, tools, and rationale | ✅ Yes |
| `docs/api.md` | API endpoints, methods, request/response formats | ✅ If project has an API |
| `docs/sdlc.md` | Full SDLC plan: requirements → design → test → deploy | ✅ Yes |

### 3.2 — README.md Requirements
Every project README must contain these sections **in this order**:

```markdown
# Project Name
> One-line description

## Tech Stack
## Prerequisites
## Installation
## Usage
## Project Structure
## Architecture Overview
## Environment Variables
## Running Tests
## SDLC Status
## Contributing
## License
```

- **Installation** must be copy-pasteable, step-by-step, and tested.
- **Project Structure** must include an annotated directory tree.
- **Environment Variables** must be a table: `NAME | Required | Description | Default`.
- **SDLC Status** must link to `docs/sdlc.md` and show current phase.

### 3.3 — Agent Log Format (`docs/agent_log.md`)

Every session must produce one entry in this exact format:

```markdown
---
## [YYYY-MM-DD HH:MM] — Session Title

**Agent:** <!-- name or model -->
**Task:** I will [action] [target] so that [outcome].
**Status:** `IN_PROGRESS` | `COMPLETED` | `BLOCKED` | `ABANDONED`

### Changes Made
- Modified `path/to/file` — reason

### Decisions
- Why approach X was chosen over Y

### Backups Created
- `backups/YYYY-MM-DD/filename.bak` — original path

### Test Results
- Smoke test: PASS / FAIL
- Unit tests: X passed, Y failed

### Next Steps
- What remains to be done

### Blockers
- Describe any blocker and what information is needed to unblock
---
```

- Entries are **prepended** (newest first).
- Never delete old entries. Append only.

### 3.4 — CHANGELOG Format (`docs/CHANGELOG.md`)
Follow [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/):

```markdown
# Changelog

## [Unreleased]
### Added
### Changed
### Fixed
### Removed

## [1.0.0] - YYYY-MM-DD
### Added
- Initial release
```

### 3.5 — SDLC Document (`docs/sdlc.md`)
Must track the full software development lifecycle for this project:

```markdown
# SDLC — [Project Name]

## 1. Requirements
- [ ] Functional requirements listed
- [ ] Non-functional requirements listed (performance, security, scalability)
- [ ] User personas / target audience defined

## 2. Design
- [ ] Architecture diagram created (docs/architecture.md)
- [ ] Tech stack finalised (docs/tech_stack.md)
- [ ] API contracts defined (docs/api.md)
- [ ] Database schema documented
- [ ] UI/UX wireframes (if applicable)

## 3. Development
- [ ] Coding standards followed (see RULES.md Phase 4)
- [ ] Feature branches used
- [ ] Code reviewed before merge

## 4. Testing
- [ ] Unit tests written (>70% coverage)
- [ ] Integration tests written
- [ ] Smoke test passes
- [ ] Edge cases tested

## 5. Deployment
- [ ] Environment variables documented (.env.example)
- [ ] Deployment guide written
- [ ] Rollback plan documented
- [ ] CI/CD pipeline configured

## 6. Maintenance
- [ ] Changelog kept up to date
- [ ] Known issues tracked in docs/tasks.md
- [ ] Agent log maintained
```

### 3.6 — Tasks File (`docs/tasks.md`)
Use MoSCoW prioritisation:

```markdown
# Tasks — [Project Name]

## Must Have
- [ ] Task description

## Should Have
- [ ] Task description

## Could Have
- [ ] Task description

## Won't Have (this release)
- [ ] Task description

## Done
- [x] Completed task — YYYY-MM-DD
```

### 3.7 — Architecture Document (`docs/architecture.md`)
Must include:
- **System Overview** — what the project does in plain English (2–3 sentences)
- **Component Diagram** — ASCII or Mermaid.js diagram
- **Data Flow** — how data enters, moves through, and exits the system
- **Key Design Decisions** — with rationale for each
- **External Dependencies** — third-party services, APIs, databases, cloud services

---

## PHASE 4 — CODING STANDARDS

### 4.1 — General Rules
- Follow the language's official style guide: PEP 8 (Python), `gofmt` (Go), `rustfmt` (Rust), Prettier (JS/TS).
- Max line length: **120 characters**.
- Every function/method must have a docstring or comment explaining **why**, not what.
- No magic numbers — use named constants.
- No commented-out code committed to the repo. Delete it or track it in `tasks.md`.
- No `print`/`console.log` debug statements left in committed code. Use a logger.

### 4.2 — Naming Conventions

| Element | Python/Rust/Go | JS/TS | Java/C# |
|---|---|---|---|
| Files | `snake_case` | `camelCase` or `kebab-case` | `PascalCase` |
| Classes | `PascalCase` | `PascalCase` | `PascalCase` |
| Functions | `snake_case` | `camelCase` | `camelCase` |
| Constants | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` |
| Env vars | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` |

### 4.3 — Standard Folder Structure
```
project-root/
├── src/                  # All source code
├── tests/                # Unit and integration tests (mirrors src/)
├── scripts/              # setup.sh, deploy.sh, migrate.sh etc.
├── docs/                 # All documentation
│   ├── agent_log.md      # Agent session log
│   ├── architecture.md   # System architecture
│   ├── api.md            # API reference
│   ├── CHANGELOG.md      # Version history
│   ├── sdlc.md           # SDLC tracking
│   ├── tasks.md          # Task backlog
│   └── tech_stack.md     # Stack decisions
├── backups/              # Timestamped file backups (git-ignored)
├── .env.example          # Env var template — NEVER commit .env
├── .gitignore
├── README.md
└── RULES.md              # This file
```

### 4.4 — Git Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short imperative description>

[optional body — explain WHY not WHAT]

[optional footer — closes #issue, breaking changes]
```

| Type | When to use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code restructure, no behaviour change |
| `test` | Adding or fixing tests |
| `chore` | Build process, tooling, deps |
| `perf` | Performance improvement |

---

## PHASE 5 — TESTING REQUIREMENTS

### 5.1 — Coverage Targets
- Minimum **70% code coverage** for all new code.
- Every bug fix **must** include a regression test.
- Every public function/method **must** have at least one unit test.

### 5.2 — Test File Naming
- Place tests in `tests/` mirroring the `src/` structure.
- `test_<module>.py` (Python), `<module>.test.ts` (TS), `<module>_test.go` (Go).

### 5.3 — Required Test Types

| Test Type | When Required |
|---|---|
| Unit | All new functions and methods |
| Integration | All DB, API, and external service interactions |
| Smoke test | Must pass before any commit is considered complete |
| Regression | Must be added for every bug fix |

---

## PHASE 6 — QUALITY GATE (before marking any task DONE)

The agent must verify **all** of the following before closing a task:

```
[ ] Smoke test passes
[ ] New/modified code has tests written
[ ] No new lint or type errors introduced
[ ] No hardcoded secrets, API keys, or passwords in any file
[ ] .env.example updated if new environment variables were added
[ ] docs/agent_log.md updated with complete session entry
[ ] docs/CHANGELOG.md updated with what changed
[ ] docs/tasks.md updated (task moved to Done with date)
[ ] docs/sdlc.md phase statuses updated
[ ] README.md still accurate (update if setup steps changed)
[ ] backups/ folder cleaned up if no longer needed
```

---

## PHASE 7 — ABSOLUTE PROHIBITIONS

| ❌ Never | Why |
|---|---|
| Commit `.env`, secrets, API keys, passwords | Security — use `.env.example` instead |
| Delete files without creating a backup first | Data loss risk |
| Modify `RULES.md` without explicit user instruction | Integrity of workflow |
| Skip Phase 0 and 1 and jump straight to coding | Leads to regressions and wasted work |
| Install packages globally on the host system | Breaks other projects |
| Run destructive commands without explicit confirmation | Irreversible |
| Push directly to `main` or `master` | Always use a feature branch |
| Silently swallow errors | Errors must be logged in `docs/agent_log.md` |
| Leave `TODO` comments without a `docs/tasks.md` entry | TODOs get forgotten |
| Introduce a new architectural pattern without documenting the decision | Future agents won't understand why |

---

## QUICK REFERENCE — Session Start Checklist

```
[ ] Read RULES.md fully
[ ] Run ls -la — identify project type and stack
[ ] Find and run the smoke test — confirm it passes
[ ] Read docs/tasks.md — find assigned task
[ ] Read last 5 entries of docs/agent_log.md
[ ] Write task statement: "I will X so that Y"
[ ] List files to touch (get approval if >2 new files)
[ ] Back up files before modifying them
[ ] Implement
[ ] Run smoke test again — must pass
[ ] Run linter / type checker — no new errors
[ ] Update docs/agent_log.md
[ ] Update docs/CHANGELOG.md
[ ] Update docs/tasks.md
[ ] Update docs/sdlc.md
[ ] Update README.md if needed
[ ] Confirm all Quality Gate checkboxes
```

---

*Owner: Ansh | Last updated: 2026-03-14 | Do not modify without owner approval.*
