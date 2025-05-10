# CS-Hackathon-2025

Thought for a couple of seconds


# GIR Project – Global Israeli RAG Fact-Checker

Congratulations on reaching the finals of the CS Hackathon at the Technion! This repository contains **GIR** (Global Israeli RAG) – a lightweight demo that highlights factual statements on any Hebrew news site by comparing them against a Reference-Augmented Generation (RAG) dataset extracted from the Israeli Central Bureau of Statistics (CBS) website.

---

## 🚀 Overview

**GIR** is a browser-based “local fact-checker” prototype comprising:

1. **Flask Backend**

   * Hosts a REST endpoint (`/verify_facts`) that ingests Hebrew sentences, heuristically identifies “fact-like” clauses, translates them to English, and embeds them with SBERT.
   * Compares each mini-sentence against our RAG dataset (a JSONL export from the CBS site) via cosine similarity.
   * Returns a verdict per sentence:

     * **true** – found in RAG (GREEN)
     * **false** – fact-like but no match (RED)
     * **unknown** – not fact-like (YELLOW)

2. **Tampermonkey UserScript**

   * Splits each paragraph into per-sentence `<span>`s
   * Sends sentences to the Flask API
   * Overlays gentle highlights directly in the browser

---

## 📁 Repository Structure

```
/
├── README.md
├── app.py                   # Flask entrypoint
├── fact_matcher.py          # Core RAG-lookup logic
├── 08_25_120b_small.jsonl   # RAG dataset (exported from CBS)
├── banks/                   # (if you wish to split by subject)
│   └── … .json
└── userscript/
    └── gir.user.js          # Tampermonkey script
```

---

## 🔧 Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/Eddie-Cohanim/CS-Hackathon-2025
   cd gir-factchecker
   ```

2. **Create a virtual environment & install**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Flask server**

   ```bash
   python app.py
   ```

   The API will listen on `http://127.0.0.1:5000/verify_facts`.

4. **Install the UserScript**

   * In Chrome/Firefox, install Tampermonkey.
   * Create a new script and paste the contents of `userscript/gir.user.js`.
   * Reload any news site and watch sentences highlight.

---

## 🌐 Data Source

* We extracted and cleaned a **JSON-Lines** dump (`08_25_120b_small.jsonl`) directly from the Israeli Central Bureau of Statistics website (English + Hebrew bilingual fields).
* It contains **official national-accounts bulletins** (e.g., GDP, consumption, investments) for Q4 2024, 1995–2024 series.

---

## ⚙️ How It Works

1. **Sentence Splitting**
   Each paragraph is broken into clauses via punctuation and line breaks.

2. **Fact Heuristic**
   We flag “fact-like” sentences if they contain numbers, dates, monetary units, or named entities (via spaCy).

3. **Translation & Embedding**
   All Hebrew text is translated to English (Deep Translator) then embedded with a multilingual SBERT model.

4. **Similarity Matching**
   We compute cosine similarity between the sentence vector (or its mini-clauses) and our pre-embedded RAG facts.

   * ≥ 0.75 → **true**
   * < 0.75 → **false**

5. **Browser Highlighting**
   Client-side spans are coloured:

   * Green (✅) for “true”
   * Red (❌) for “false”
   * Yellow (⚠️) for “unknown”

---

## 🏆 Hackathon Recognition

This project placed **Finalist** at the **2025 Technion CS Hackathon**, in recognition of its:

* **Data-driven RAG** pipeline using official government data
* **Lightweight UX** with client-side highlighting
* **Multilingual** embedding that bridges Hebrew news with an English knowledge base

---

## 🤝 Contributing

We welcome improvements! Feel free to:

* Add more “fact banks” for other domains
* Enhance translation caching or support offline translation
* Tweak heuristics or threshold values
* Polish the browser UX (animations, themes)

Please submit PRs or open issues.

---

## 📄 License

This project is released under the **MIT License**.

---

> **GIR** – Bridging Hebrew news articles with official statistics via on-the-fly RAG fact-checking.
