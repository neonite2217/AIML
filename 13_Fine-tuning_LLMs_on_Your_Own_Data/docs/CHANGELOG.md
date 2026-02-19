# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Future enhancements placeholder

## [1.0.0] - 2026-03-17

### Added
- Initial implementation of PEFT/LoRA fine-tuning script
- IMDb sentiment classification with DistilBERT
- Offline-safe dataset loading with synthetic fallback
- Offline-safe model loading with random initialization fallback
- LoRA configuration (rank=8, alpha=16, dropout=0.1)
- Training with Hugging Face Trainer API
- Evaluation metrics: accuracy, precision, recall, F1
- Sample inference demonstration
- Comprehensive README.md with installation and usage
- Complete documentation suite (SDLC, architecture, tech stack)
- Build log and agent log
- Requirements.txt with all dependencies

### Changed
- Migrated from AG News to IMDb dataset for binary classification
- Updated from basic fine-tuning to PEFT/LoRA approach
- Enhanced error handling with fallback mechanisms

### Fixed
- Fixed TrainingArguments parameter compatibility (`eval_strategy` vs `evaluation_strategy`)
- Fixed Trainer parameter (`processing_class` vs deprecated `tokenizer`)

### Technical Details
- Model: distilbert-base-uncased
- Dataset: IMDb (200 train, 50 test samples)
- Trainable parameters: 739,586 (1.09% of total)
- Training time: ~2.5 seconds on GPU
- Evaluation accuracy: 58%

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2026-03-17 | Initial release with PEFT/LoRA implementation |

## Future Enhancements

- [ ] Add support for QLoRA (quantized LoRA)
- [ ] Implement instruction tuning format
- [ ] Add post-training quantization
- [ ] Create FastAPI deployment wrapper
- [ ] Add more comprehensive test suite
- [ ] Support for custom datasets via CLI
- [ ] Add Weights & Biases integration
- [ ] Implement gradient checkpointing for larger models
