import re
import random
from typing import Dict, List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import string

# Descargar recursos necesarios de NLTK
def download_nltk_resources():
    resources = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']
    for resource in resources:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(resource)

download_nltk_resources()

class EmpatheticResponseGenerator:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

        self.intensity_words = {
            'high': ['extremely', 'absolutely', 'completely', 'totally', 'really', 'very', 'so', 
                     'incredibly', 'devastated', 'furious', 'ecstatic', 'terrified', 'overwhelmed'],
            'medium': ['quite', 'rather', 'pretty', 'fairly', 'somewhat', 'moderately'],
            'low': ['a bit', 'slightly', 'kind of', 'sort of', 'a little']
        }

        self.emotion_mapping = {
            'admiration': 'positive', 'amusement': 'positive', 'approval': 'positive',
            'caring': 'positive', 'curiosity': 'positive', 'desire': 'positive',
            'excitement': 'positive', 'gratitude': 'positive', 'joy': 'positive',
            'love': 'positive', 'optimism': 'positive', 'pride': 'positive',
            'realization': 'positive', 'relief': 'positive',

            'anger': 'negative', 'annoyance': 'negative', 'disappointment': 'negative',
            'disapproval': 'negative', 'disgust': 'negative', 'embarrassment': 'negative',
            'fear': 'negative', 'grief': 'negative', 'nervousness': 'negative',
            'remorse': 'negative', 'sadness': 'negative',

            'confusion': 'neutral', 'surprise': 'neutral', 'neutral': 'neutral'
        }

        self.empathetic_patterns = {
            'anger': [
                "I can sense the frustration in your words. It's completely understandable to feel angry when dealing with {context}.",
                "Your anger is valid. When facing {context}, it's natural to feel this way.",
                "I hear how upset you are about {context}. That sounds really challenging.",
                "It's clear this situation has really gotten to you. Feeling angry about {context} makes perfect sense.",
                "I can feel your frustration about {context}. That must be incredibly difficult to deal with."
            ],
            'sadness': [
                "I'm sorry you're going through this difficult time. {context} sounds really hard to deal with.",
                "Your sadness comes through in your words. {context} must be weighing heavily on you.",
                "I can feel the pain in what you're sharing. {context} sounds incredibly difficult.",
                "It takes courage to express these feelings. {context} would be hard for anyone to handle.",
                "I hear the heaviness in your heart about {context}. That's such a painful experience."
            ],
            'fear': [
                "I can understand why {context} would feel scary. Your concerns are completely valid.",
                "Fear about {context} is a natural response. You're not alone in feeling this way.",
                "It's okay to feel afraid when facing {context}. Your feelings are important.",
                "I hear the worry in your words about {context}. That uncertainty can be really overwhelming.",
                "Your fear about {context} makes complete sense. That sounds really unsettling."
            ],
            'joy': [
                "I can feel the happiness in your words! {context} sounds wonderful.",
                "Your joy is contagious! It's beautiful to hear how {context} has affected you.",
                "I'm so glad you're experiencing this positivity with {context}.",
                "The excitement in your message is wonderful. {context} sounds amazing!",
                "Your happiness about {context} really shines through. That's fantastic!"
            ],
            'surprise': [
                "That does sound unexpected! {context} must have caught you off guard.",
                "I can imagine how surprising {context} must have been for you.",
                "What an unexpected turn of events with {context}! How are you processing this?",
                "That's quite a surprise! {context} sounds like it really changed things for you.",
                "I can see how {context} would be completely unexpected. That's quite shocking!"
            ],
            'disgust': [
                "I can understand why {context} would be off-putting. That sounds unpleasant.",
                "Your reaction to {context} is completely understandable. That does sound disturbing.",
                "I can see why {context} would bother you. That's a natural response.",
                "It's clear that {context} has really affected you negatively. Your feelings are valid.",
                "I hear how repulsed you are by {context}. That sounds really uncomfortable."
            ],
            'disappointment': [
                "I can hear the disappointment in your words about {context}. That must be really disheartening.",
                "It's clear that {context} didn't meet your expectations. That's such a letdown.",
                "Your disappointment about {context} is completely understandable. That sounds frustrating.",
                "I can feel how let down you are by {context}. That's really disappointing.",
                "It sounds like {context} was a real disappointment for you. That's tough to handle."
            ],
            'embarrassment': [
                "I can sense how uncomfortable {context} made you feel. That's really embarrassing.",
                "Your embarrassment about {context} is completely natural. We've all been there.",
                "I understand why {context} would make you feel self-conscious. That's tough.",
                "It's clear that {context} was mortifying for you. That's such an awkward situation.",
                "I can feel how embarrassed you are about {context}. That sounds really uncomfortable."
            ],
            'neutral': [
                "Thank you for sharing your thoughts about {context}. I'm here to listen.",
                "I appreciate you taking the time to express how you feel about {context}.",
                "Your perspective on {context} is valuable. How can I best support you?",
                "I'm glad you felt comfortable sharing your experience with {context}.",
                "I hear what you're saying about {context}. That's an important point."
            ]
        }

        self.follow_up_phrases = {
            'high_intensity': [
                "Would you like to talk more about this?",
                "How are you coping with everything?",
                "Is there anything specific that might help right now?",
                "Would it help to explore this further?",
                "What kind of support would be most helpful?"
            ],
            'medium_intensity': [
                "How are you feeling about everything?",
                "Would you like to share more about your experience?",
                "What's been on your mind lately?",
                "How can I best support you through this?",
                "What would help you feel better about this?"
            ],
            'low_intensity': [
                "Thanks for sharing this with me.",
                "I'm here if you need to talk more.",
                "How has your day been overall?",
                "What else is on your mind?",
                "How are you doing with everything else?"
            ]
        }

        self.context_keywords = {
            'work': ['job', 'work', 'boss', 'colleague', 'office', 'meeting', 'project', 'deadline', 
                     'career', 'workplace', 'coworker', 'manager', 'employee', 'salary', 'promotion'],
            'relationship': ['partner', 'friend', 'family', 'relationship', 'love', 'breakup', 'dating',
                             'boyfriend', 'girlfriend', 'husband', 'wife', 'marriage', 'divorce'],
            'health': ['sick', 'doctor', 'hospital', 'pain', 'health', 'medicine', 'treatment',
                       'illness', 'medical', 'diagnosis', 'surgery', 'therapy'],
            'school': ['school', 'teacher', 'student', 'exam', 'grade', 'homework', 'class',
                       'university', 'college', 'study', 'education', 'degree'],
            'financial': ['money', 'financial', 'budget', 'debt', 'bills', 'expense', 'income',
                          'savings', 'loan', 'credit', 'payment'],
            'personal': ['myself', 'personal', 'identity', 'self', 'confidence', 'growth',
                         'anxiety', 'depression', 'stress', 'mental']
        }

    def identify_context(self, text: str) -> str:
        text_lower = text.lower()
        context_scores = {}
        for context, keywords in self.context_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            score += sum(2 for keyword in keywords if f' {keyword} ' in f' {text_lower} ')
            if score > 0:
                context_scores[context] = score
        return max(context_scores, key=context_scores.get) if context_scores else 'general'

    def generate_context_summary(self, text: str) -> str:
        context_type = self.identify_context(text)
        context_phrases = {
            'work': ['your job situation', 'work challenges', 'workplace issues'],
            'relationship': ['your relationship', 'this personal situation', 'what happened'],
            'health': ['your health concerns', 'what you\'re going through', 'this medical situation'],
            'school': ['your studies', 'school pressures', 'academic challenges'],
            'financial': ['your financial situation', 'money worries', 'financial stress'],
            'personal': ['what you\'re experiencing', 'your personal journey', 'these feelings']
        }
        sentences = re.split(r'[.!?]\s+', text)
        informative_sentences = [s for s in sentences if len(s.split()) > 3]
        if informative_sentences:
            main_sentence = max(informative_sentences, key=len)
            simplified = re.sub(r'^(I|I\'m|I am|My|Me)\s+', '', main_sentence, flags=re.IGNORECASE)
            simplified = simplified.lower().strip()
            return simplified[:50] + ('...' if len(simplified) > 50 else '')
        return random.choice(context_phrases.get(context_type, ["what you're going through"]))

    def calculate_emotional_intensity(self, text: str) -> str:
        text_lower = text.lower()
        exclamation_count = text.count('!')
        question_count = text.count('?')
        caps_words = len([word for word in text.split() if word.isupper() and len(word) > 1])
        high_score = sum(1 for word in self.intensity_words['high'] if word in text_lower)
        medium_score = sum(1 for word in self.intensity_words['medium'] if word in text_lower)
        repeated_letters = len(re.findall(r'(.)\1{2,}', text_lower))
        total = exclamation_count * 2 + question_count + caps_words + high_score * 3 + medium_score + repeated_letters * 2
        return 'high_intensity' if total > 4 else 'medium_intensity' if total > 1 else 'low_intensity'

    def generate_empathetic_response(self, text: str, emotion: str) -> str:
        emotion = emotion.lower()
        if emotion not in self.empathetic_patterns:
            emotion_category = self.emotion_mapping.get(emotion, 'neutral')
            if emotion_category == 'positive':
                emotion = 'joy'
            elif emotion_category == 'negative':
                if any(word in text.lower() for word in ['angry', 'mad', 'frustrated']): emotion = 'anger'
                elif any(word in text.lower() for word in ['sad', 'depressed', 'upset']): emotion = 'sadness'
                elif any(word in text.lower() for word in ['scared', 'afraid', 'worried']): emotion = 'fear'
                elif any(word in text.lower() for word in ['disappointed', 'let down']): emotion = 'disappointment'
                elif any(word in text.lower() for word in ['embarrassed', 'ashamed']): emotion = 'embarrassment'
                else: emotion = 'sadness'
            else:
                emotion = 'neutral'
        context = self.generate_context_summary(text)
        pattern = random.choice(self.empathetic_patterns.get(emotion, self.empathetic_patterns['neutral']))
        main_response = pattern.format(context=context)
        follow_up = random.choice(self.follow_up_phrases[self.calculate_emotional_intensity(text)])
        return f"{main_response} {follow_up}"

# Ejecución de prueba
if __name__ == "__main__":
    generator = EmpatheticResponseGenerator()
    test_cases = [
        ("I'm so frustrated with my job. My boss keeps giving me impossible deadlines and I can't keep up.", "anger"),
        ("I just lost my grandmother and I don't know how to cope with this loss.", "sadness"),
        ("I'm worried about my upcoming presentation. What if I mess up in front of everyone?", "fear"),
        ("I got promoted today! I can't believe it actually happened.", "joy"),
        ("My friend just told me something that completely shocked me.", "surprise"),
        ("I feel so embarrassed about what happened at the meeting today.", "embarrassment"),
        ("I'm really disappointed that my vacation got cancelled.", "disappointment")
    ]

    print("=== Generador de Respuestas Empáticas ===\n")
    for text, emotion in test_cases:
        print(f"Texto: {text}")
        print(f"Emoción: {emotion}")
        response = generator.generate_empathetic_response(text, emotion)
        print(f"Respuesta: {response}")
        print("-" * 80)
