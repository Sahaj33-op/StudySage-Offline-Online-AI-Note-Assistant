import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def generate_questions(summary, num_questions=3):
    sentences = sent_tokenize(summary)
    if not sentences:
        return []
    
    stop_words = set(stopwords.words('english'))
    questions = []
    attempts = 0
    max_attempts = num_questions * 3
    
    while len(questions) < num_questions and attempts < max_attempts:
        sentence = random.choice(sentences)
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        
        potential_answers = [word for word, tag in tagged_words if tag.startswith(('NN', 'VB', 'JJ')) and
                            word.lower() not in stop_words and len(word) > 3]
        
        if not potential_answers:
            attempts += 1
            continue
            
        answer = random.choice(potential_answers)
        question = sentence.replace(answer, "_____")
        
        distractors = []
        for other_sentence in sentences:
            if other_sentence != sentence:
                other_words = word_tokenize(other_sentence)
                other_tagged = pos_tag(other_words)
                for word, tag in other_tagged:
                    if (tag.startswith(('NN', 'VB', 'JJ')) and word.lower() not in stop_words and
                        len(word) > 3 and word != answer and word not in distractors):
                        distractors.append(word)
        
        if len(distractors) >= 3:
            distractors = random.sample(distractors, 3)
            questions.append({
                "question": question,
                "answer": answer,
                "options": [answer] + distractors
            })
        
        attempts += 1
    
    return questions
