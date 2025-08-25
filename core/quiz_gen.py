import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def generate_questions(summary, num_questions=3):
    print("[+] Generating questions from summary...")
    
    # Tokenize the summary into sentences
    sentences = sent_tokenize(summary)
    if not sentences:
        print("Quiz generation failed: No sentences found in the summary.")
        return []

    # Select up to num_questions sentences
    selected_sentences = random.sample(sentences, min(num_questions, len(sentences)))
    
    # Build a global pool of potential distractors
    all_words = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        all_words.extend(words)
    stop_words = set(stopwords.words('english'))
    potential_distractors = list(set(
        word for word in all_words
        if word.isalpha() and word.lower() not in stop_words and len(word) > 2
    ))

    questions = []
    for i, sentence in enumerate(selected_sentences):
        words = word_tokenize(sentence)
        keywords = [word for word in words if word.isalpha() and word.lower() not in stop_words and len(word) > 2]

        if not keywords:
            print(f"Skipping sentence {i+1}: No keywords found.")
            continue

        # Choose an answer
        answer = random.choice(keywords)
        question = sentence.replace(answer, "_____")

        # Select distractors from the global pool
        available_distractors = [word for word in potential_distractors if word != answer]
        num_distractors = min(3, len(available_distractors)) if available_distractors else 0
        distractors = random.sample(available_distractors, num_distractors) if num_distractors > 0 else []

        # Require at least 1 distractor to create a multiple-choice question
        if num_distractors < 1:
            print(f"Skipping question {i+1}: Not enough distractors available.")
            continue

        questions.append({
            "question": f"Q{i+1}. {question}",
            "answer": answer,
            "options": [answer] + distractors
        })

    if not questions:
        print("Quiz generation failed: Could not generate any questions with sufficient distractors.")
    elif len(questions) < num_questions:
        print(f"Generated only {len(questions)} out of {num_questions} requested questions due to limited keywords or distractors.")
    
    return questions
