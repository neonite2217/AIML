#!/usr/bin/env python3
"""
Single-file Multi-Document RAG web app.

Features:
- Minimal black-and-white web interface
- Upload up to 10 PDF documents
- Uploaded files stored in an isolated runtime folder
- Runtime folder is wiped on every server start
- Interactive question answering over uploaded documents
"""

from __future__ import annotations

import base64
import json
import os
import re
import shutil
import threading
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import numpy as np
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


MAX_DOCS = 10
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024
SENTENCE_WINDOW = 3
SENTENCE_OVERLAP = 1
CHUNK_CHAR_LIMIT = 520
TOP_K = 4
MIN_CONFIDENCE = 0.05
STRICT_MIN_CONFIDENCE = 0.12
MAX_ANSWER_CHARS = 280
MAX_SELECTED_SENTENCES = 2

RUNTIME_DIR = Path("runtime")
UPLOAD_DIR = RUNTIME_DIR / "user_uploads"


def sanitize_filename(filename: str) -> str:
    base = Path(filename).name
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", base).strip("._")
    if not sanitized:
        sanitized = "document.pdf"
    if not sanitized.lower().endswith(".pdf"):
        sanitized = f"{sanitized}.pdf"
    return sanitized


def split_sentences(text: str) -> list[str]:
    normalized = text.replace("\r", "\n")
    normalized = re.sub(
        r"\b(OBJECTIVE|EDUCATION|EXPERIENCE|SKILLS|PROJECTS|CERTIFICATIONS|CONTACT|SUMMARY)\b",
        r". \1",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(r"[ \t]+", " ", normalized).strip()
    if not normalized:
        return []
    parts = re.split(r"(?<=[.!?])\s+|(?<=:)\s+|\n+|\s+\|\s+|\s+•\s+", normalized)
    return [s.strip() for s in parts if s.strip()]


def _trim_to_readable_span(text: str, query_terms: set[str], max_chars: int = 220) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if len(clean) <= max_chars:
        return clean

    lowered = clean.lower()
    idx = -1
    for term in sorted(query_terms, key=len, reverse=True):
        pos = lowered.find(term)
        if pos != -1:
            idx = pos
            break

    if idx == -1:
        snippet = clean[:max_chars].rstrip()
        return f"{snippet}..."

    start = max(0, idx - max_chars // 3)
    end = min(len(clean), start + max_chars)
    snippet = clean[start:end].strip()
    if start > 0:
        snippet = f"...{snippet}"
    if end < len(clean):
        snippet = f"{snippet}..."
    return snippet


def _tokenize_words(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9+#.-]+", text.lower())
        if len(token) > 1
    }


def _infer_intent_terms(question: str) -> set[str]:
    lower_q = question.lower()
    terms = _tokenize_words(question)
    intent_map = {
        "project": {"project", "projects", "built", "developed", "implemented"},
        "skill": {"skill", "skills", "stack", "language", "languages", "tools"},
        "python": {"python", "pandas", "numpy", "flask", "django", "fastapi"},
        "docker": {"docker", "container", "compose", "image", "kubernetes"},
        "java": {"java", "spring", "maven"},
        "c++": {"c++", "cpp", "c"},
        "experience": {"experience", "worked", "intern", "employment", "role"},
        "education": {"education", "college", "degree", "university", "school", "cgpa"},
    }

    for key, expansions in intent_map.items():
        if key in lower_q or any(alias in lower_q for alias in expansions):
            terms.update(expansions)

    return terms


@dataclass
class Chunk:
    source: str
    text: str
    page: int | None = None


class RAGEngine:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.documents: list[str] = []
        self.chunks: list[Chunk] = []
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix: Any = None

    def startup_reset(self) -> None:
        with self._lock:
            if RUNTIME_DIR.exists():
                shutil.rmtree(RUNTIME_DIR, ignore_errors=True)
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            self._reset_index()

    def clear_all(self) -> None:
        with self._lock:
            if UPLOAD_DIR.exists():
                shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            self._reset_index()

    def _reset_index(self) -> None:
        self.documents = []
        self.chunks = []
        self.vectorizer = None
        self.matrix = None

    def _extract_pdf_pages(self, file_path: Path) -> list[tuple[int, str]]:
        reader = PdfReader(str(file_path))
        pages: list[tuple[int, str]] = []
        for idx, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            if page_text.strip():
                pages.append((idx, page_text))
        return pages

    def _chunk_text(self, text: str) -> list[str]:
        normalized = text.replace("\r", "\n")
        blocks = [part.strip() for part in re.split(r"\n{2,}", normalized) if part.strip()]
        if not blocks:
            return []

        sentences: list[str] = []
        for block in blocks:
            sentences.extend(split_sentences(block))

        if not sentences:
            return []

        chunks: list[str] = []
        step = max(1, SENTENCE_WINDOW - SENTENCE_OVERLAP)
        i = 0
        while i < len(sentences):
            window = " ".join(sentences[i : i + SENTENCE_WINDOW]).strip()
            if window:
                if len(window) > CHUNK_CHAR_LIMIT:
                    window = window[:CHUNK_CHAR_LIMIT].rstrip() + "..."
                chunks.append(window)
            if i + SENTENCE_WINDOW >= len(sentences):
                break
            i += step
        return chunks

    def _rebuild_index(self) -> None:
        if not self.chunks:
            self.vectorizer = None
            self.matrix = None
            return

        texts = [chunk.text for chunk in self.chunks]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(texts)

    def add_files(self, files: list[dict[str, Any]]) -> dict[str, Any]:
        with self._lock:
            if len(self.documents) + len(files) > MAX_DOCS:
                raise ValueError(
                    f"Uploading {len(files)} file(s) exceeds the {MAX_DOCS}-document limit "
                    f"(currently stored: {len(self.documents)})."
                )

            accepted: list[str] = []
            rejected: list[dict[str, str]] = []
            pending_chunks: list[Chunk] = []

            for file_obj in files:
                original_name = str(file_obj.get("name", "")).strip()
                payload = str(file_obj.get("content_base64", "")).strip()

                if not original_name or not payload:
                    rejected.append({"name": original_name or "unknown", "reason": "Missing name or content."})
                    continue

                safe_name = sanitize_filename(original_name)
                if not safe_name.lower().endswith(".pdf"):
                    rejected.append({"name": original_name, "reason": "Only PDF files are supported."})
                    continue

                try:
                    raw = base64.b64decode(payload, validate=True)
                except Exception:
                    rejected.append({"name": original_name, "reason": "Invalid base64 data."})
                    continue

                if len(raw) == 0:
                    rejected.append({"name": original_name, "reason": "Empty file."})
                    continue

                if len(raw) > MAX_FILE_SIZE_BYTES:
                    rejected.append(
                        {
                            "name": original_name,
                            "reason": f"File too large (max {MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB).",
                        }
                    )
                    continue

                unique_name = self._next_filename(safe_name)
                target_path = UPLOAD_DIR / unique_name
                target_path.write_bytes(raw)

                try:
                    extracted_pages = self._extract_pdf_pages(target_path)
                except Exception as exc:
                    target_path.unlink(missing_ok=True)
                    rejected.append({"name": original_name, "reason": f"Unreadable PDF: {exc}"})
                    continue

                if not extracted_pages:
                    target_path.unlink(missing_ok=True)
                    rejected.append({"name": original_name, "reason": "No extractable text found."})
                    continue

                chunks_added = 0
                for page_num, page_text in extracted_pages:
                    page_chunks = self._chunk_text(page_text)
                    for chunk_text in page_chunks:
                        pending_chunks.append(Chunk(source=unique_name, text=chunk_text, page=page_num))
                        chunks_added += 1

                if chunks_added == 0:
                    target_path.unlink(missing_ok=True)
                    rejected.append({"name": original_name, "reason": "No usable text chunks generated."})
                    continue

                accepted.append(unique_name)

            if not accepted:
                raise ValueError("No valid PDF documents were uploaded.")

            self.documents.extend(accepted)
            self.chunks.extend(pending_chunks)
            self._rebuild_index()

            return {
                "accepted": accepted,
                "rejected": rejected,
                "document_count": len(self.documents),
                "chunk_count": len(self.chunks),
            }

    def _next_filename(self, file_name: str) -> str:
        candidate = file_name
        stem = Path(file_name).stem
        suffix = Path(file_name).suffix
        idx = 1
        while (UPLOAD_DIR / candidate).exists():
            candidate = f"{stem}_{idx}{suffix}"
            idx += 1
        return candidate

    def ask(self, question: str, include_evidence: bool = False) -> dict[str, Any]:
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("Question cannot be empty.")

        with self._lock:
            if not self.documents or not self.chunks or self.vectorizer is None or self.matrix is None:
                raise ValueError("Upload at least one PDF before asking questions.")

            query_vec = self.vectorizer.transform([normalized_question])
            sims = cosine_similarity(query_vec, self.matrix)[0]
            top_indices = np.argsort(sims)[::-1][:TOP_K]

            ranked = [
                {
                    "score": float(sims[i]),
                    "chunk": self.chunks[i],
                }
                for i in top_indices
                if float(sims[i]) > 0
            ]

        search_summary = self._search_summary(normalized_question, ranked)

        if not ranked:
            empty = {
                "answer": "I don't have enough information in the uploaded documents to answer that.",
                "sources": [],
                "confidence": 0.0,
                "search": search_summary,
            }
            if include_evidence:
                empty["evidence"] = []
            return empty

        direct = self._extract_direct_fact_answer(normalized_question, ranked)
        if direct is not None:
            sources = list(dict.fromkeys(item["chunk"].source for item in ranked))
            confidence = round(float(ranked[0]["score"]), 4)
            response = {
                "answer": direct,
                "sources": sources,
                "confidence": confidence,
                "search": search_summary,
            }
            if include_evidence:
                response["evidence"] = self._evidence_from_ranked(
                    ranked,
                    query_terms=_tokenize_words(normalized_question),
                    limit=2,
                )
            return response

        if float(ranked[0]["score"]) < STRICT_MIN_CONFIDENCE:
            low = {
                "answer": "I don't have enough information in the uploaded documents to answer that.",
                "sources": [],
                "confidence": round(float(ranked[0]["score"]), 4),
                "search": search_summary,
            }
            if include_evidence:
                low["evidence"] = []
            return low

        answer_data = self._build_extractive_answer(normalized_question, ranked)
        sources = list(dict.fromkeys(item["chunk"].source for item in ranked))
        confidence = round(float(ranked[0]["score"]), 4)

        response = {
            "answer": answer_data["answer"],
            "sources": sources,
            "confidence": confidence,
            "search": search_summary,
        }
        if include_evidence:
            response["evidence"] = answer_data["evidence"]
        return response

    def _search_summary(self, question: str, ranked: list[dict[str, Any]]) -> dict[str, Any]:
        docs = list(dict.fromkeys(item["chunk"].source for item in ranked))
        pages = {(item["chunk"].source, item["chunk"].page) for item in ranked if item["chunk"].page is not None}
        return {
            "query": question,
            "indexed_passages": len(self.chunks),
            "matched_passages": len(ranked),
            "matched_documents": len(docs),
            "matched_pages": len(pages),
        }

    def _extract_direct_fact_answer(self, question: str, ranked: list[dict[str, Any]]) -> str | None:
        lower_q = question.lower()
        joined = " ".join(item["chunk"].text for item in ranked)

        if any(token in lower_q for token in ["email", "mail id", "e-mail"]):
            emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", joined)
            if emails:
                return f"Email: {emails[0]}"

        if any(token in lower_q for token in ["phone", "mobile", "contact number", "telephone"]):
            phones = re.findall(r"(?:\+?\d[\d\-\s()]{7,}\d)", joined)
            if phones:
                phone = re.sub(r"\s+", " ", phones[0]).strip()
                return f"Phone: {phone}"

        if "name" in lower_q and any(token in lower_q for token in ["developer", "candidate", "person", "applicant"]):
            top_text = " ".join(item["chunk"].text for item in ranked)
            name = self._extract_name_candidate(top_text)
            if name:
                return f"Name: {name}"

        return None

    def _extract_name_candidate(self, text: str) -> str | None:
        cleaned = re.sub(r"\s+", " ", text).strip()
        if not cleaned:
            return None

        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", cleaned)
        if emails:
            before_email = cleaned[: cleaned.find(emails[0])].strip()
            start_match = re.match(r"\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})", before_email)
            if start_match:
                candidate = start_match.group(1).strip()
                if candidate not in {"India", "Bhubaneswar", "Odisha"}:
                    return candidate
            near = before_email[-100:]
            nearby_names = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b", near)
            blocked_near = {"India", "Bhubaneswar", "Odisha"}
            for candidate in nearby_names:
                if candidate not in blocked_near:
                    return candidate

        candidates = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b", cleaned)
        if candidates:
            return candidates[0]

        single_names = re.findall(r"\b([A-Z][a-z]{2,})\b", cleaned[:120])
        blocked = {
            "Objective",
            "Education",
            "Experience",
            "Projects",
            "Skills",
            "Summary",
            "Contact",
            "Email",
            "Phone",
            "India",
        }
        for token in single_names:
            if token not in blocked:
                return token

        uppercase_candidates = re.findall(r"\b([A-Z]{3,}(?:\s+[A-Z]{3,}){1,3})\b", cleaned)
        if uppercase_candidates:
            return uppercase_candidates[0].title()

        return None

    def _evidence_from_ranked(
        self, ranked: list[dict[str, Any]], query_terms: set[str], limit: int = 2
    ) -> list[dict[str, Any]]:
        evidence: list[dict[str, Any]] = []
        for item in ranked[:limit]:
            snippet = _trim_to_readable_span(item["chunk"].text, query_terms, max_chars=180)
            page = item["chunk"].page
            source_label = item["chunk"].source if page is None else f"{item['chunk'].source} (p.{page})"
            evidence.append(
                {
                    "source": source_label,
                    "snippet": snippet,
                    "score": round(float(item["score"]), 4),
                }
            )
        return evidence

    def _naturalize_sentence(self, sentence: str, intent_terms: set[str]) -> str:
        cleaned = re.sub(r"\s+", " ", sentence).strip()
        cleaned = re.sub(
            r"^(PROJECTS?|SKILLS?|EXPERIENCE|EDUCATION|SUMMARY|OBJECTIVE|CERTIFICATIONS?|CONTACT)\s*[:\-]?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
        cleaned = cleaned.strip(" -|")
        if not cleaned:
            return ""
        if cleaned and cleaned[-1] not in ".!?":
            cleaned = cleaned + "."

        if any(t in intent_terms for t in {"project", "projects"}):
            return f"Relevant project detail: {cleaned}"
        if any(t in intent_terms for t in {"skill", "skills", "stack"}):
            return f"Relevant skills/detail: {cleaned}"
        if any(t in intent_terms for t in {"experience", "role", "worked"}):
            return f"Relevant experience detail: {cleaned}"
        return cleaned

    def _build_extractive_answer(self, question: str, ranked: list[dict[str, Any]]) -> dict[str, Any]:
        query_terms = _tokenize_words(question)
        intent_terms = _infer_intent_terms(question)

        sentence_scores: list[tuple[float, str, str, int | None]] = []
        for item in ranked:
            chunk_score = item["score"]
            sentences = split_sentences(item["chunk"].text)
            for sentence in sentences:
                words = _tokenize_words(sentence)
                overlap = len(query_terms & words)
                intent_hits = len(intent_terms & words)
                if overlap == 0 and intent_hits == 0 and chunk_score < MIN_CONFIDENCE:
                    continue
                if intent_terms and intent_hits == 0 and overlap < 2:
                    continue
                score = chunk_score * 2.0 + (overlap * 1.4) + (intent_hits * 1.8)
                sentence_scores.append((score, sentence, item["chunk"].source, item["chunk"].page))

        if not sentence_scores:
            top_text = ranked[0]["chunk"].text
            fallback = _trim_to_readable_span(top_text, query_terms, max_chars=MAX_ANSWER_CHARS)
            answer = fallback or "I don't have enough information in the uploaded documents to answer that."
            return {
                "answer": answer,
                "evidence": self._evidence_from_ranked(ranked, query_terms, limit=2),
            }

        sentence_scores.sort(key=lambda x: x[0], reverse=True)
        selected: list[str] = []
        selected_evidence: list[dict[str, Any]] = []
        seen: set[str] = set()
        top_score = sentence_scores[0][0]

        for score, sentence, source, page in sentence_scores:
            short = _trim_to_readable_span(sentence, query_terms, max_chars=170)
            polished = self._naturalize_sentence(short, intent_terms)
            if not polished:
                continue
            key = polished.lower()
            if key in seen:
                continue
            if selected and score < (top_score * 0.65):
                continue
            selected.append(polished)
            seen.add(key)
            source_label = source if page is None else f"{source} (p.{page})"
            selected_evidence.append(
                {
                    "source": source_label,
                    "snippet": short,
                    "score": round(float(score), 4),
                }
            )
            if len(selected) == MAX_SELECTED_SENTENCES:
                break

        if len(selected) > 1:
            selected[1] = selected[1].replace("Relevant project detail:", "Additional project detail:", 1)
            selected[1] = selected[1].replace("Relevant skills/detail:", "Additional skills/detail:", 1)
            selected[1] = selected[1].replace("Relevant experience detail:", "Additional experience detail:", 1)

        answer = " ".join(selected).strip()
        if ranked[0]["score"] < MIN_CONFIDENCE:
            return {
                "answer": "I don't have enough information in the uploaded documents to answer that.",
                "evidence": [],
            }
        if answer:
            answer = f"I searched the uploaded documents and found: {answer}"
        if len(answer) > MAX_ANSWER_CHARS:
            answer = answer[:MAX_ANSWER_CHARS].rstrip() + "..."
        final_answer = answer or "I don't have enough information in the uploaded documents to answer that."
        return {
            "answer": final_answer,
            "evidence": selected_evidence[:2],
        }

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "document_count": len(self.documents),
                "chunk_count": len(self.chunks),
                "documents": list(self.documents),
                "upload_dir": str(UPLOAD_DIR),
            }


ENGINE = RAGEngine()


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    data = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


INDEX_HTML = """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>RAG Server</title>
  <style>
    :root {
      --bg: #fff;
      --fg: #000;
      --muted: #555;
      --border: #000;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--fg);
      font-family: "Courier New", Courier, monospace;
      line-height: 1.45;
    }
    .container {
      max-width: 920px;
      margin: 0 auto;
      padding: 20px;
    }
    h1 {
      margin: 0 0 14px;
      font-size: 24px;
      letter-spacing: 0.5px;
    }
    .panel {
      border: 1px solid var(--border);
      padding: 14px;
      margin-bottom: 14px;
    }
    .panel-title {
      font-weight: 700;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 10px;
    }
    .row { display: flex; gap: 8px; flex-wrap: wrap; }
    input[type=\"file\"], input[type=\"text\"] {
      width: 100%;
      border: 1px solid var(--border);
      background: #fff;
      color: #000;
      padding: 10px;
      font: inherit;
    }
    button {
      border: 1px solid var(--border);
      background: #fff;
      color: #000;
      padding: 10px 14px;
      cursor: pointer;
      font: inherit;
    }
    button:hover { background: #000; color: #fff; }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    .muted { color: var(--muted); font-size: 13px; }
    .stack { margin-top: 10px; display: grid; gap: 8px; }
    .doc-list {
      border: 1px solid var(--border);
      padding: 8px;
      max-height: 120px;
      overflow: auto;
      font-size: 13px;
      background: #fff;
    }
    .doc-item {
      padding: 4px 0;
      border-bottom: 1px dashed #bbb;
    }
    .doc-item:last-child { border-bottom: 0; }
    .log {
      border: 1px solid var(--border);
      min-height: 220px;
      padding: 10px;
      overflow: auto;
      white-space: pre-wrap;
      word-wrap: break-word;
      background: #fff;
    }
    .line {
      margin: 0 0 8px;
      border-left: 2px solid #000;
      padding-left: 8px;
    }
    .line.you { border-left-style: dashed; }
    .line.sys { border-left-style: dotted; }
    .tiny { font-size: 12px; color: #555; }
  </style>
</head>
<body>
  <main class=\"container\">
    <h1>Single-File RAG Server</h1>

    <section class=\"panel\">
      <div class=\"panel-title\">
        <strong>Upload PDFs</strong>
        <span class=\"muted\">Limit: 10 docs</span>
      </div>
      <p class=\"muted\">Max 10 PDFs total. Runtime upload folder is cleared on every server restart.</p>
      <input id=\"fileInput\" type=\"file\" accept=\".pdf,application/pdf\" multiple />
      <div class=\"row\" style=\"margin-top:10px\">
        <button id=\"uploadBtn\">Upload</button>
        <button id=\"resetBtn\" type=\"button\">Reset Documents</button>
      </div>
      <div class=\"stack\">
        <p id=\"status\" class=\"muted\" style=\"margin:0\">Status: idle</p>
        <div id=\"docsList\" class=\"doc-list muted\">No documents uploaded.</div>
      </div>
    </section>

    <section class=\"panel\">
      <strong>Ask a Question</strong>
      <div class=\"row\" style=\"margin-top:10px\">
        <input id=\"questionInput\" type=\"text\" placeholder=\"Ask something from your uploaded documents...\" />
        <button id=\"askBtn\">Ask</button>
      </div>
      <div class=\"row\" style=\"margin-top:8px\">
        <label class=\"muted\" for=\"evidenceToggle\">
          <input id=\"evidenceToggle\" type=\"checkbox\" />
          Show evidence
        </label>
      </div>
      <div id=\"chat\" class=\"log\" style=\"margin-top:10px\"></div>
    </section>
  </main>

<script>
  const statusEl = document.getElementById('status');
  const chatEl = document.getElementById('chat');
  const docsEl = document.getElementById('docsList');
  const uploadBtn = document.getElementById('uploadBtn');
  const askBtn = document.getElementById('askBtn');
  const resetBtn = document.getElementById('resetBtn');
  const evidenceToggle = document.getElementById('evidenceToggle');

  function logLine(text, kind = 'rag') {
    const line = document.createElement('div');
    line.className = `line ${kind}`;
    line.textContent = text;
    chatEl.appendChild(line);
    chatEl.scrollTop = chatEl.scrollHeight;
  }

  function setStatus(text) {
    statusEl.textContent = `Status: ${text}`;
  }

  async function refreshStatus() {
    try {
      const res = await fetch('/health');
      const data = await res.json();
      setStatus(`${data.document_count} doc(s), ${data.chunk_count} chunk(s)`);
      renderDocs(data.documents || []);
    } catch (e) {
      setStatus('server not reachable');
    }
  }

  function renderDocs(documents) {
    if (!documents.length) {
      docsEl.textContent = 'No documents uploaded.';
      return;
    }
    docsEl.innerHTML = '';
    for (const name of documents) {
      const row = document.createElement('div');
      row.className = 'doc-item';
      row.textContent = name;
      docsEl.appendChild(row);
    }
  }

  function readFileAsBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const str = String(reader.result || '');
        const idx = str.indexOf(',');
        resolve(idx >= 0 ? str.slice(idx + 1) : str);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  uploadBtn.addEventListener('click', async () => {
    const input = document.getElementById('fileInput');
    const files = Array.from(input.files || []);
    if (!files.length) {
      setStatus('pick at least one PDF');
      return;
    }

    setStatus('uploading...');
    uploadBtn.disabled = true;
    resetBtn.disabled = true;
    try {
      const payloadFiles = await Promise.all(files.map(async (f) => ({
        name: f.name,
        content_base64: await readFileAsBase64(f)
      })));

      const res = await fetch('/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ files: payloadFiles })
      });

      const data = await res.json();
      if (!res.ok) {
        setStatus(data.error || 'upload failed');
        return;
      }

      const accepted = (data.accepted || []).join(', ') || 'none';
      logLine(`[upload] accepted: ${accepted}`, 'sys');
      if (data.rejected && data.rejected.length) {
        for (const item of data.rejected) {
          logLine(`[upload] rejected ${item.name}: ${item.reason}`, 'sys');
        }
      }

      input.value = '';
      await refreshStatus();
    } catch (e) {
      setStatus(`upload error: ${e}`);
    } finally {
      uploadBtn.disabled = false;
      resetBtn.disabled = false;
    }
  });

  async function askQuestion() {
    const qEl = document.getElementById('questionInput');
    const question = qEl.value.trim();
    if (!question) {
      return;
    }

    logLine(`[you] ${question}`, 'you');
    logLine('[search] searching relevant passages...', 'sys');
    qEl.value = '';
    askBtn.disabled = true;

    try {
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, include_evidence: evidenceToggle.checked })
      });
      const data = await res.json();
      if (!res.ok) {
        logLine(`[rag] ${data.error || 'request failed'}`, 'rag');
        return;
      }

      if (data.search) {
        logLine(
          `[search] matched ${data.search.matched_passages}/${data.search.indexed_passages} passages across ${data.search.matched_documents} document(s) and ${data.search.matched_pages} page(s)`,
          'sys'
        );
      }

      const src = (data.sources || []).join(', ') || 'none';
      logLine(`[rag] ${data.answer}`, 'rag');
      logLine(`[sources] ${src} | confidence=${data.confidence}`, 'sys');
      if (evidenceToggle.checked && Array.isArray(data.evidence) && data.evidence.length) {
        for (const item of data.evidence) {
          logLine(`[evidence] ${item.source}: ${item.snippet}`, 'sys');
        }
      }
      await refreshStatus();
    } catch (e) {
      logLine(`[rag] request error: ${e}`, 'rag');
    } finally {
      askBtn.disabled = false;
    }
  }

  askBtn.addEventListener('click', askQuestion);
  document.getElementById('questionInput').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      askQuestion();
    }
  });

  resetBtn.addEventListener('click', async () => {
    resetBtn.disabled = true;
    try {
      const res = await fetch('/reset', { method: 'POST' });
      const data = await res.json();
      if (!res.ok) {
        setStatus(data.error || 'reset failed');
        return;
      }
      logLine('[system] documents reset', 'sys');
      await refreshStatus();
    } catch (e) {
      setStatus(`reset error: ${e}`);
    } finally {
      resetBtn.disabled = false;
    }
  });

  refreshStatus();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _read_json(self) -> dict[str, Any]:
        length_str = self.headers.get("Content-Length", "0")
        try:
            length = int(length_str)
        except ValueError:
            raise ValueError("Invalid Content-Length header.")

        raw = self.rfile.read(length) if length > 0 else b""
        if not raw:
            return {}

        try:
            return json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise ValueError(f"Invalid JSON body: {exc}") from exc

    def _send_html(self, html: str) -> None:
        data = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/":
            self._send_html(INDEX_HTML)
            return

        if self.path == "/health":
            json_response(self, HTTPStatus.OK, ENGINE.snapshot())
            return

        json_response(self, HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/upload":
            try:
                payload = self._read_json()
                files = payload.get("files", [])
                if not isinstance(files, list):
                    raise ValueError("`files` must be a list.")
                if not files:
                    raise ValueError("No files provided.")
                if len(files) > MAX_DOCS:
                    raise ValueError(f"Upload at most {MAX_DOCS} files at a time.")

                result = ENGINE.add_files(files)
                json_response(self, HTTPStatus.OK, result)
            except ValueError as exc:
                json_response(self, HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            except Exception as exc:
                json_response(self, HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return

        if self.path == "/ask":
            try:
                payload = self._read_json()
                question = str(payload.get("question", ""))
                include_evidence = bool(payload.get("include_evidence", False))
                result = ENGINE.ask(question, include_evidence=include_evidence)
                json_response(self, HTTPStatus.OK, result)
            except ValueError as exc:
                json_response(self, HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            except Exception as exc:
                json_response(self, HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return

        if self.path == "/reset":
            try:
                ENGINE.clear_all()
                json_response(self, HTTPStatus.OK, ENGINE.snapshot())
            except Exception as exc:
                json_response(self, HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return

        json_response(self, HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[{self.address_string()}] {fmt % args}")


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    ENGINE.startup_reset()
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"RAG server running at http://{host}:{port}")
    print(f"Upload dir (auto-cleared on restart): {UPLOAD_DIR}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    run_server(host=host, port=port)
