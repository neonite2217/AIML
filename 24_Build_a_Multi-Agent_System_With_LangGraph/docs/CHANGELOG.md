# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.0.0] - 2026-03-23

### Added
- Complete multi-agent workflow implementation using LangGraph
- Researcher agent node for generating research notes
- Writer agent node for generating blog posts
- TypedDict-based state management
- Comprehensive README.md with installation and troubleshooting
- SDLC documentation (docs/sdlc.md)
- Agent log (docs/agent_log.md)
- Task tracking (docs/tasks.md)
- Architecture documentation (docs/architecture.md)

### Changed
- Updated default LLM model from `llama2` to `qwen3.5:latest` for compatibility

### Fixed
- Resolved ModuleNotFoundError for langgraph and langchain-ollama
- Updated import to use modern langchain-ollama library

### Removed
- None

---

## [0.1.0] - 2026-01-30

### Added
- Initial project structure
- guide.txt with step-by-step implementation
- requirements.txt with dependencies
- ENGINEERING_DECISIONS.md with architectural rationale
- BUILD_ANALYSIS_LOG.md with build analysis

### Changed
- None

### Fixed
- None

### Removed
- None

---

*Follows Semantic Versioning and Keep a Changelog format.*
*Last updated: 2026-03-23*