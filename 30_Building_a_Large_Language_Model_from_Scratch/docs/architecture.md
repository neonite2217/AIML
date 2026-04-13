# Architecture Documentation

## Building a Large Language Model from Scratch

---

## 1. System Overview

This project implements a GPT-style decoder-only transformer language model from scratch using PyTorch. The system follows a complete ML pipeline: data preprocessing → model training → text generation.

### High-Level Data Flow

```
Raw Text Input
    │
    ▼
┌─────────────────┐
│  Tokenization   │  Character-level encoding
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Embeddings    │  Token + Position embeddings
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Transformer     │  N layers of self-attention + FFN
│    Blocks       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Output       │  Logits → Cross-Entropy → Loss
└─────────────────┘
```

---

## 2. Component Architecture

### 2.1 Tokenization Module

**Purpose**: Convert raw text to numerical token IDs and back

**Implementation**:
- Character-level vocabulary built from input text
- Sorted character set for deterministic mapping
- Encode function: `str → List[int]`
- Decode function: `List[int] → str`

**Data Flow**:
```
Input: "The quick brown fox"
  │
  ▼
Vocabulary: {'T', 'h', 'e', ' ', ...}
  │
  ▼
Output: [45, 12, 3, 0, 38, ...]
```

### 2.2 Embedding Module

**Purpose**: Map token IDs to dense vector representations with positional information

**Components**:

| Component | Shape | Description |
|-----------|-------|-------------|
| TokenEmbedding | [vocab_size, n_embd] | Learnable token vectors |
| PositionEmbedding | [block_size, n_embd] | Learnable position vectors |

**Combining Strategy**:
```python
token_embeddings = token_embedding_table(idx)  # [B, T, n_embd]
position_embeddings = position_embedding_table(positions)  # [T, n_embd]
combined = token_embeddings + position_embeddings  # Broadcasting
```

### 2.3 Self-Attention Module

**Purpose**: Allow each token to attend to all previous tokens in the sequence

**Architecture**:
```
Input: [B, T, C]
  │
  ├─► Key projection: Linear(C → head_size)
  ├─► Query projection: Linear(C → head_size)
  └─► Value projection: Linear(C → head_size)
  │
  ▼
Scaled Dot-Product: (Q @ K^T) / sqrt(head_size)
  │
  ▼
Causal Mask: Mask future tokens with -inf
  │
  ▼
Softmax: Attention weights (sum to 1)
  │
  ▼
Weighted Sum: Attention weights @ Values
  │
  ▼
Output: [B, T, head_size]
```

**Key Formulas**:
- Attention scores: `wei = (Q @ K.transpose(-2,-1)) * C**-0.5`
- Masked attention: `wei = wei.masked_fill(tril == 0, float('-inf'))`
- Output: `out = F.softmax(wei, dim=-1) @ V`

### 2.4 Multi-Head Attention Module

**Purpose**: Run multiple attention heads in parallel for richer representations

**Architecture**:
```
Input: [B, T, n_embd]
  │
  ▼
┌────────────────────────────┐
│    Head 1  │  Head 2  │ ...│  Parallel execution
│   [B,T,h]  │  [B,T,h] │     │
└────────────────────────────┘
  │
  ▼
Concatenate: [B, T, n_head * head_size]
  │
  ▼
Linear Projection: [B, T, n_embd]
  │
  ▼
Dropout regularization
```

### 2.5 Feed-Forward Module

**Purpose**: Transform attention outputs with non-linear capacity

**Architecture**:
```
Input: [B, T, n_embd]
  │
  ▼
Linear: n_embd → 4 * n_embd
  │
  ▼
ReLU activation
  │
  ▼
Linear: 4 * n_embd → n_embd
  │
  ▼
Dropout
  │
  ▼
Output: [B, T, n_embd]
```

### 2.6 Transformer Block

**Purpose**: Combine attention and feed-forward with residual connections

**Architecture (Pre-norm)**:
```
Input: x
  │
  ▼
LayerNorm(x) ──► Self-Attention ──► + x (residual)
  │
  ▼
LayerNorm(x) ──► Feed-Forward ──► + x (residual)
  │
  ▼
Output
```

### 2.7 Language Model Head

**Purpose**: Project final embeddings to vocabulary for token prediction

**Architecture**:
```
Transformer Output: [B, T, n_embd]
  │
  ▼
LayerNorm (final)
  │
  ▼
Linear: n_embd → vocab_size
  │
  ▼
Output: [B, T, vocab_size] (logits)
```

---

## 3. Training Pipeline

### 3.1 Data Pipeline

```
Raw Text
  │
  ▼
Encode: str → tensor of token IDs
  │
  ▼
Split: 90% train / 10% validation
  │
  ▼
Batch Sampling: Random windows of size block_size
  │
  ▼
Input (x): tokens 0 to T-1
Target (y): tokens 1 to T
```

### 3.2 Forward Pass

```
Input Batch [B, T]
  │
  ▼
1. Embeddings (tok + pos)
  │
  ▼
2. Stack of Transformer Blocks (×4)
  │
  ▼
3. Final LayerNorm
  │
  ▼
4. Linear projection to vocab
  │
  ▼
Logits [B, T, vocab_size]
```

### 3.3 Loss Computation

```
Logits: [B, T, vocab_size]
  │
  ▼
Reshape: [B*T, vocab_size]
  │
  ▼
Targets: [B*T]
  │
  ▼
Cross-Entropy Loss
  │
  ▼
Scalar loss
```

### 3.4 Backward Pass

```
Loss
  │
  ▼
Backpropagate through all layers
  │
  ▼
Compute gradients for all parameters
  │
  ▼
Update with AdamW optimizer
```

---

## 4. Inference Pipeline

### 4.1 Text Generation

```
Initial: [1, 1] tensor of zeros (start token)
  │
  ▼
Loop max_new_tokens times:
  │
  ├─► Truncate to last block_size tokens
  │
  ├─► Forward pass
  │
  ├─► Get logits for last position
  │
  ├─► Convert to probabilities (softmax)
  │
  ├─► Sample next token (multinomial)
  │
  └─► Append to sequence
  │
  ▼
Final sequence: [1, 1 + max_new_tokens]
  │
  ▼
Decode: tensor → string
```

---

## 5. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Character-level tokenization | Simple, no external dependencies |
| Pre-norm layer normalization | More stable training |
| Causal (triangular) mask | Enforces autoregressive property |
| Scaled dot-product attention | Standard, well-tested |
| AdamW optimizer | Default choice for transformers |

---

## 6. Model Parameters

| Layer | Parameters |
|-------|------------|
| Token Embedding | vocab_size × n_embd |
| Position Embedding | block_size × n_embd |
| Attention (per head) | 3 × (n_embd × head_size) |
| FFN (per block) | 2 × (n_embd × 4n_embd) |
| Output Head | n_embd × vocab_size |
| **Total** | ~52K parameters |

---

*Architecture Document - Project #30*  
*Last Updated: 2026-03-25*