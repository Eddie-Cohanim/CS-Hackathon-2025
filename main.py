import os, json, requests, spacy

# ⚡ Tiny, fast pipeline: just a rule-based sentencizer – no POS-tagger, parser, NER
nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")

API_KEY = os.getenv("OPENROUTER_API_KEY")        # put your key in the environment

def factual_sentences(text: str, model: str = "openai/gpt-4o"):
    """
    Return a list of sentences that *sound* like factual claims,
    using an OpenRouter-hosted LLM plus a JSON-only response format.
    """
    # 1) Local pre-processing – turn the blob into sentences
    sentences = [s.text.strip() for s in nlp(text).sents]

    # 2) Build a numbered prompt
    numbered = "\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences))
    prompt = (
        "Below is a list of sentences. Return a JSON object with an array "
        "called `facts` that contains ONLY the sentences that make verifiable "
        "factual claims (no re-writing or additions).\n\n"
        f"{numbered}"
    )

    # 3) Call OpenRouter
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},  # strict JSON out
        "temperature": 0.0,
        "max_tokens": 1024,
    }

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps(body),
        timeout=120,
    )
    r.raise_for_status()

    # 4) Parse and return the array
    content = r.json()["choices"][0]["message"]["content"]
    return json.loads(content)["facts"]


if __name__ == "__main__":
    sample = """
    John F. Kennedy was the 35th President of the United States.
    Many people say he was the most charismatic leader in modern history.
    The moon is about 384,400 km from Earth.
    I think chocolate ice-cream tastes the best.
    """
    print(factual_sentences(sample))
    # → ['John F. Kennedy was the 35th President of the United States.',
    #    'The moon is about 384,400 km from Earth.']
