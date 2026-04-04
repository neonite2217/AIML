# Lab Project: Build an AI Agent to Automate Your Research
# v0.2 — Local Mistral LLM Integration for Abstractive Summarization

import os
import logging
from bs4 import BeautifulSoup
import requests
from sentence_transformers import SentenceTransformer, util
import torch
from ctransformers import AutoModelForCausalLM

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

MODEL_PATH = os.environ.get(
    "MISTRAL_MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "..", "mistral-7b-instruct-v0.1.Q4_K_M.gguf"),
)
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", "200"))
TOP_K = int(os.environ.get("TOP_K", "3"))
LLM_MAX_TOKENS = int(os.environ.get("LLM_MAX_TOKENS", "256"))
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0.3"))
LLM_CONTEXT_WINDOW = int(os.environ.get("LLM_CONTEXT_WINDOW", "2048"))
MAX_PASSAGE_CHARS = int(os.environ.get("MAX_PASSAGE_CHARS", "500"))


def search_web(query):
    """Return a list of URLs relevant to the query.

    Currently returns mock URLs for reproducible results.
    Replace the body with a real DuckDuckGo / SerpAPI call for production use.
    """
    logger.info("Searching the web for: '%s'", query)
    return [
        "https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)",
        "https://huggingface.co/docs/transformers/index",
    ]


def fetch_and_clean(url):
    """Download a web page and extract its plain-text body."""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.extract()
        text = soup.get_text(separator=" ", strip=True)
        logger.info("Scraped %d chars from %s", len(text), url)
        return text
    except Exception as e:
        logger.warning("Failed to fetch %s: %s", url, e)
        return ""


def chunk_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Split *text* into overlapping chunks using a sliding window."""
    step = max(chunk_size - chunk_overlap, 1)
    return [text[i : i + chunk_size] for i in range(0, len(text), step)]


def load_embedding_model():
    """Load the sentence-transformer model used for semantic ranking."""
    logger.info("Loading sentence-transformer model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("Embedding model loaded.")
    return model


def load_llm(model_path=MODEL_PATH):
    """Load the local Mistral GGUF model via ctransformers.

    Falls back to a graceful placeholder if the model file is missing.
    """
    resolved = os.path.abspath(model_path)
    if not os.path.isfile(resolved):
        logger.warning("Mistral model not found at %s — summarization will use fallback.", resolved)
        return None
    logger.info("Loading Mistral model from %s (this may take a moment) ...", resolved)
    llm = AutoModelForCausalLM.from_pretrained(
        resolved,
        model_type="mistral",
        gpu_layers=0,
        context_length=LLM_CONTEXT_WINDOW,
    )
    logger.info("Mistral model loaded successfully.")
    return llm


def summarize_with_llm(llm, query, passages):
    """Generate an abstractive summary from the retrieved passages using the local Mistral model.

    Passages are truncated to MAX_PASSAGE_CHARS each to keep the total prompt within
    the model's context window.
    """
    truncated = [p[:MAX_PASSAGE_CHARS] for p in passages]
    context = "\n\n---\n\n".join(truncated)
    prompt = (
        "[INST] You are a research assistant. Based ONLY on the context below, "
        "write a concise, well-structured summary that answers the user's question.\n\n"
        f"Question: {query}\n\n"
        f"Context:\n{context}\n\n"
        "Summary: [/INST]"
    )
    # Ensure the prompt itself does not exceed the context window minus room for output
    prompt_tokens = llm.tokenize(prompt)
    max_prompt = LLM_CONTEXT_WINDOW - LLM_MAX_TOKENS
    if len(prompt_tokens) > max_prompt:
        prompt_tokens = prompt_tokens[:max_prompt]
        prompt = llm.detokenize(prompt_tokens)
        logger.info("Prompt truncated to %d tokens to fit context window.", max_prompt)
    logger.info("Generating abstractive summary with Mistral (%d tokens max)...", LLM_MAX_TOKENS)
    summary = llm(prompt, max_new_tokens=LLM_MAX_TOKENS, temperature=LLM_TEMPERATURE)
    return summary.strip()


def summarize_fallback(query, passages):
    """Return a concatenation-based fallback when no LLM is available."""
    logger.info("Using fallback concatenation summarization.")
    joined = "\n\n".join(passages)
    return (
        f"Based on the retrieved passages, here is a combined overview for '{query}':\n\n{joined}"
    )


def run_research_agent(query):
    """Execute the full research pipeline end-to-end."""
    logger.info("=" * 60)
    logger.info("AI Research Agent — v0.2 (Mistral LLM)")
    logger.info("=" * 60)

    # ── Stage 1: Search ──────────────────────────────────────────────
    urls = search_web(query)
    logger.info("Found %d source URL(s).", len(urls))

    # ── Stage 2: Scrape & Clean ──────────────────────────────────────
    all_chunks = []
    for url in urls:
        content = fetch_and_clean(url)
        if content:
            all_chunks.extend(chunk_text(content))
    logger.info("Total text chunks created: %d", len(all_chunks))

    if not all_chunks:
        logger.error("No content could be retrieved. Aborting.")
        return

    # ── Stage 3: Chunk & Embed ───────────────────────────────────────
    embedding_model = load_embedding_model()
    chunk_embeddings = embedding_model.encode(all_chunks, convert_to_tensor=True)

    # ── Stage 4: Rank (Cosine Similarity) ────────────────────────────
    query_embedding = embedding_model.encode(query, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(query_embedding, chunk_embeddings)[0]
    top_results = torch.topk(cosine_scores, k=min(TOP_K, len(all_chunks)))
    top_passages = [all_chunks[i] for i in top_results.indices]

    logger.info("Top-%d relevant passages selected (scores: %s).",
                TOP_K, [f"{cosine_scores[i]:.4f}" for i in top_results.indices])

    print("\n--- Top Relevant Passages ---")
    for idx, (passage, score) in enumerate(
        zip(top_passages, [cosine_scores[i] for i in top_results.indices]), 1
    ):
        print(f"\n[Passage {idx} | Score: {score:.4f}]")
        print(passage[:500] + ("..." if len(passage) > 500 else ""))

    # ── Stage 5: Summarize with Mistral LLM ──────────────────────────
    print("\n--- Abstractive Summary (Mistral 7B Instruct) ---")
    llm = load_llm()
    if llm is not None:
        summary = summarize_with_llm(llm, query, top_passages)
    else:
        summary = summarize_fallback(query, top_passages)

    print(summary)
    logger.info("Pipeline complete.")
    return summary


# ── Entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    query = "What is a Transformer model in machine learning?"
    run_research_agent(query)
