# quiz_gen.py — robust to NLTK 3.9+ (punkt_tab) and tagger name changes
import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# ---------- NLTK self-heal ----------
def _dl(name: str):
    try:
        nltk.download(name, quiet=True)
    except Exception:
        pass

# Ensure tokenizers (NLTK 3.9 added 'punkt_tab')
for res, path in [
    ("punkt", "tokenizers/punkt"),
    ("punkt_tab", "tokenizers/punkt_tab"),
]:
    try:
        nltk.data.find(path)
    except LookupError:
        _dl(res)

# Ensure stopwords
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    _dl("stopwords")

# Ensure POS tagger (name differs across versions)
_TAGGER_READY = False
def _ensure_tagger():
    global _TAGGER_READY
    if _TAGGER_READY:
        return
    for name, path in [
        ("averaged_perceptron_tagger", "taggers/averaged_perceptron_tagger"),
        ("averaged_perceptron_tagger_eng", "taggers/averaged_perceptron_tagger_eng"),
    ]:
        try:
            nltk.data.find(path)
            _TAGGER_READY = True
            return
        except LookupError:
            _dl(name)
    # If neither is found after attempting download, we’ll fall back.
    _TAGGER_READY = False

_ensure_tagger()

# Safe POS tag wrapper: fall back to heuristic if tagger is truly unavailable
def _safe_pos_tag(tokens):
    try:
        from nltk import pos_tag
        if not _TAGGER_READY:
            raise LookupError("Tagger not available")
        return pos_tag(tokens)
    except Exception:
        # Heuristic fallback: treat capitalized words or len>=5 as content nouns
        return [(w, "NN" if (w[:1].isupper() or len(w) >= 5) else "O") for w in tokens]

# ---------- Question generation ----------
def generate_questions(summary: str, num_questions: int = 5, progress_callback=None):
    """
    Returns list of {question, answer, options}
    Calls progress_callback(stage:str, step:int, total:int) if provided.
    """
    if not summary or not isinstance(summary, str):
        return []

    sentences = [s.strip() for s in sent_tokenize(summary) if len(s.strip().split()) >= 5]
    if not sentences:
        return []

    sw = set(stopwords.words("english"))
    questions = []
    tries = 0
    max_tries = max(10, num_questions * 4)

    # Build a pool of distractor candidates from the whole text once
    all_tokens = []
    for s in sentences:
        all_tokens.extend(word_tokenize(s))
    global_tagged = _safe_pos_tag(all_tokens)
    global_candidates = [
        w for (w, tag) in global_tagged
        if tag.startswith(("NN", "VB", "JJ"))
        and w.isalpha()
        and w.lower() not in sw
        and len(w) > 3
    ]
    # Keep unique while preserving order
    seen = set()
    global_candidates = [w for w in global_candidates if not (w.lower() in seen or seen.add(w.lower()))]

    while len(questions) < num_questions and tries < max_tries:
        tries += 1
        # notify progress on attempts vs target
        if progress_callback:
            progress_callback("Generating questions (attempts)", tries, max_tries)

        sent = random.choice(sentences)
        tokens = word_tokenize(sent)
        tagged = _safe_pos_tag(tokens)

        # Extract possible answers from this sentence
        candidates = [
            w for (w, tag) in tagged
            if tag.startswith(("NN", "VB", "JJ"))
            and w.isalpha()
            and w.lower() not in sw
            and len(w) > 3
        ]
        # Deduplicate, keep order
        seen_local = set()
        candidates = [w for w in candidates if not (w.lower() in seen_local or seen_local.add(w.lower()))]

        if not candidates:
            continue

        answer = random.choice(candidates)

        # Build distractors: prioritize global pool excluding the answer
        distractors_pool = [w for w in global_candidates if w.lower() != answer.lower()]
        # As a backup, harvest from other sentences
        if len(distractors_pool) < 10:
            for other in sentences:
                if other == sent:
                    continue
                ot = word_tokenize(other)
                ot_tagged = _safe_pos_tag(ot)
                for w, tag in ot_tagged:
                    if (
                        tag.startswith(("NN", "VB", "JJ"))
                        and w.isalpha()
                        and w.lower() not in sw
                        and len(w) > 3
                        and w.lower() != answer.lower()
                    ):
                        distractors_pool.append(w)

        # Finalize distractors (unique, not equal to answer)
        seen_d = set()
        distractors_pool = [w for w in distractors_pool if not (w.lower() in seen_d or seen_d.add(w.lower()))]

        if len(distractors_pool) < 3:
            # Not enough plausible distractors; skip this sentence
            continue

        distractors = random.sample(distractors_pool, 3)
        options = [answer] + distractors
        random.shuffle(options)

        # Create cloze-style question
        # Replace an exact match of 'answer' (case-sensitive); if not present, append a blank version.
        if answer in sent:
            q_text = sent.replace(answer, "_____")
        else:
            q_text = f"{sent}\n\nFill in the blank: _____"

        # Avoid near-duplicate questions (by question stem)
        if any(q["question"] == q_text for q in questions):
            continue

        questions.append({
            "question": q_text,
            "answer": answer,
            "options": options
        })
        if len(questions) < num_questions:
            # notify when a new question is added
            if progress_callback:
                progress_callback("Questions generated", len(questions), num_questions)

    return questions
