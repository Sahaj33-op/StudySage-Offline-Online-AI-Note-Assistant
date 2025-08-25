# core/quiz_gen.py
import random
import nltk

# Self-heal: ensure tokenizer/stopwords exist (no crashes on fresh envs)
def _ensure_nltk():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        # some envs split models; ignore if not present
        pass
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)

_ensure_nltk()

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

STOP = set(stopwords.words("english"))

def _keywords(text: str, k: int = 10):
    words = [w.lower() for w in word_tokenize(text) if w.isalpha()]
    words = [w for w in words if w not in STOP and len(w) > 2]
    freq = {}
    for w in words: freq[w] = freq.get(w, 0) + 1
    top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:max(3, k)]
    return [w for w, _ in top]

def generate_questions(summary: str, num_questions: int = 5):
    """
    Returns a list of {question, options[list], answer}.
    Simple keyword & sentence-based MCQs; deterministic but decent for study sets.
    """
    sents = [s.strip() for s in sent_tokenize(summary) if s.strip()]
    if not sents:
        return []

    keys = _keywords(summary, k=min(12, max(6, num_questions * 3)))
    qs = []
    rng = random.Random(1337)  # stable order for tests

    for i in range(min(num_questions, len(sents))):
        sent = sents[i % len(sents)]
        # pick a keyword present in the sentence; else any keyword
        target = next((kw for kw in keys if kw.lower() in sent.lower()), (keys[i % len(keys)] if keys else "concept"))
        q = sent.replace(target, "_____") if target.lower() in sent.lower() else f"In the context, what best fills the blank: _____ ? ({sent})"

        # distractors
        distractors = [k for k in keys if k != target]
        rng.shuffle(distractors)
        options = [target] + distractors[:3]
        rng.shuffle(options)

        qs.append({
            "question": q,
            "options": options,
            "answer": target
        })

    return qs
