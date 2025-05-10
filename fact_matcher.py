# fact_matcher.py ────────────────────────────────────────────────────
"""
• read *one* RAG file called  `08_25_120b_small.jsonl`  in the same folder
  (each line = JSON object with at least a `"text"` field **or** a raw string)
• translate Hebrew → English internally so all embeddings share a language
• return the original Hebrew sentence with a label:
      "true"   (green)   – similarity ≥ 0.75
      "false"  (red)     – similarity < 0.75
      "unknown" (yellow) – sentence did not look factual
"""

from __future__ import annotations
import functools, json, pathlib, re
from typing import Tuple, List

import numpy as np
import spacy
from deep_translator import GoogleTranslator
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ───────────────────────── one-time set-up ──────────────────────────
MODEL = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
NLP   = spacy.load("en_core_web_sm")

RAG_PATH      = pathlib.Path(__file__).with_name("08_25_120b_small.jsonl")   # <── file here
SIM_THRESHOLD = 0.56

FACT_NE = {"PERSON","ORG","GPE","LOC","DATE","TIME",
           "MONEY","PERCENT","QUANTITY","CARDINAL", "INVESTMENT", "EXPENSE", "%"}

@functools.lru_cache(maxsize=4096)
def _to_en(txt: str) -> str:
    """Translate (cached).  Falls back to original on any error."""
    try:
        return GoogleTranslator(source="auto", target="en").translate(txt)
    except Exception:
        return txt

# ───────────────────── load & embed the RAG once ────────────────────
def _load_rag() -> Tuple[List[str], np.ndarray]:
    if not RAG_PATH.exists():
        print(f"[fact-matcher] RAG file not found: {RAG_PATH}")
        return [], np.empty((0,384))

    he_facts: list[str] = []
    with RAG_PATH.open(encoding="utf8") as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln:
                continue
            try:                           # JSON object/array line?
                obj = json.loads(ln)
                if isinstance(obj, str):
                    he_facts.append(obj)
                else:
                    he_facts.append(obj["text"])
            except json.JSONDecodeError:   # raw string line
                he_facts.append(ln)

    en_facts = [_to_en(f) for f in he_facts]
    emb      = MODEL.encode(
        en_facts, batch_size=128, convert_to_numpy=True,
        show_progress_bar=len(en_facts) > 128
    )
    return he_facts, emb

HE_FACTS, EMB_BANK = _load_rag()
print(f"[fact-matcher] loaded {len(HE_FACTS):,} facts from {RAG_PATH.name}")

# ───────────────────── helpers for the Flask route ──────────────────
_HE_NUM_RE = re.compile(r"\d+[%₪€$£]|[0-9]{4}")

def is_fact_like(sentence_he: str) -> bool:
    """Quick heuristic – avoids heavy SBERT on obvious non-facts."""
    if _HE_NUM_RE.search(sentence_he):
        return True

    sent_en = _to_en(sentence_he)
    doc     = NLP(sent_en)
    if any(ent.label_ in FACT_NE for ent in doc.ents):
        return True
    if re.search(r"\b\d{4}\b|\d+[%$£€₪]|\d{1,3}(?:,\d{3})+", sent_en):
        return True
    return False
##return false


@functools.lru_cache(maxsize=4096)
def check_sentence(sentence_he: str) -> Tuple[str, float]:
    """
    Returns (“true” | “false” | “unknown”, similarity float 0-1).
    • all heavy work is cached per unique Hebrew sentence
    • always returns the **original Hebrew** to the caller (Flask app)
    """
    if not is_fact_like(sentence_he):
        return "unknown", 0.0

    if EMB_BANK.size == 0:                # empty RAG – nothing to compare
        return "unknown", 0.0

    sent_en = _to_en(sentence_he)
    emb     = MODEL.encode([sent_en])
    sim     = float(np.max(cosine_similarity(emb, EMB_BANK)))

    return ("true" if sim >= SIM_THRESHOLD else "false"), sim
