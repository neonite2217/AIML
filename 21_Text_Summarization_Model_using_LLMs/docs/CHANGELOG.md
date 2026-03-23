# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Extractive summarization comparison
- ROUGE metric evaluation
- Web interface with Streamlit
- Map-reduce for long documents
- Domain-specific fine-tuning

---

## [1.0.0] - 2026-03-23

### Added
- Initial implementation of text summarization using T5 model
- Support for abstractive summarization with beam search
- Configurable generation parameters (length, beams, penalties)
- Comprehensive documentation (README, BUILD_LOG, SDLC)
- Project structure with docs folder
- Virtual environment setup instructions
- Troubleshooting guide in README

### Technical Details
- Model: t5-small (60M parameters)
- Framework: PyTorch 2.10.0 + Transformers 5.3.0
- Generation: Beam search with 4 beams
- Max input length: 512 tokens
- Output length: 40-150 tokens

### Documentation
- README.md with full setup and usage guide
- BUILD_LOG.md documenting entire build process
- docs/sdlc.md with complete SDLC tracking
- docs/architecture.md with system design
- docs/tech_stack.md with technology decisions
- docs/agent_log.md for agent session tracking

---

## [0.1.0] - Initial Development

### Added
- Basic text_summarization.py script
- requirements.txt with dependencies
- Project guide.txt from University curriculum

---

*Project: Text Summarization Model using LLMs*  
*Part of Super 30 AI Curriculum*
