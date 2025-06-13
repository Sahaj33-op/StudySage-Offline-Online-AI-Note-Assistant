import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

def generate_questions(summary, num_questions=3):
    try:
        # Tokenize the summary into sentences
        sentences = sent_tokenize(summary)
        if not sentences:
            print("Quiz generation failed: No sentences found in the summary.")
            return []

        # Check for minimum content
        if len(sentences) < 2:
            print("Quiz generation failed: Summary has fewer than 2 sentences.")
            return []

        # Tokenize all words in the summary to build a pool of potential distractors
        all_words = []
        for sentence in sentences:
            words = word_tokenize(sentence)
            all_words.extend(words)
        tagged_words = pos_tag(all_words)
        stop_words = set(stopwords.words('english'))

        # Collect all potential distractors from the entire summary
        potential_distractors = [
            word for word, tag in tagged_words
            if tag.startswith(('NN', 'VB', 'JJ')) and word.lower() not in stop_words and len(word) > 3
        ]

        if len(potential_distractors) < 3:
            print("Quiz generation failed: Not enough unique words to create distractors.")
            return []

        questions = []
        attempts = 0
        max_attempts = num_questions * 5  # Increased attempts to allow more tries

        while len(questions) < num_questions and attempts < max_attempts:
            # Choose a sentence to base the question on
            sentence = random.choice(sentences)
            words = word_tokenize(sentence)
            tagged_words = pos_tag(words)

            # Find potential answers in the chosen sentence
            potential_answers = [
                word for word, tag in tagged_words
                if tag.startswith(('NN', 'VB', 'JJ')) and word.lower() not in stop_words and len(word) > 3
            ]

            if not potential_answers:
                attempts += 1
                continue

            # Choose an answer
            answer = random.choice(potential_answers)
            question = sentence.replace(answer, "_____")

            # Select distractors from the entire summary's word pool
            available_distractors = [word for word in potential_distractors if word != answer]
            if len(available_distractors) < 2:  # Reduced requirement to 2 distractors
                attempts += 1
                continue

            # Sample distractors (aim for 3, but accept 2 if that's all we have)
            num_distractors = min(3, len(available_distractors))
            distractors = random.sample(available_distractors, num_distractors)

            questions.append({
                "question": question,
                "answer": answer,
                "options": [answer] + distractors
            })

            attempts += 1

        if not questions:
            print("Quiz generation failed: Could not generate any questions within the allowed attempts.")
        
        return questions

    except Exception as e:
        print(f"Error generating quiz questions: {str(e)}")
        return []
