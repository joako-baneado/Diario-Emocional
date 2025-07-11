"""
Módulo de Generación de Respuestas Empáticas para la Aplicación de Diario Emocional

Este módulo contiene la funcionalidad principal para generar respuestas empáticas y contextualizadas
basadas en el análisis de texto emocional. Utiliza técnicas de procesamiento de lenguaje natural
para comprender el contexto, intensidad emocional y generar respuestas apropiadas.

Dependencias:
    - re: Para expresiones regulares y procesamiento de texto
    - random: Para selección aleatoria de patrones de respuesta
    - typing: Para anotaciones de tipo
    - nltk: Para procesamiento de lenguaje natural
    - collections: Para contadores y estructuras de datos

Funcionalidades principales:
    - Análisis de contexto emocional en texto
    - Detección de intensidad emocional
    - Generación de respuestas empáticas personalizadas
    - Mapeo de emociones a categorías
    - Conversión de perspectiva (primera a segunda persona)

Clases:
    - EmpatheticResponseGenerator: Generador principal de respuestas empáticas
"""

import re
import random
from typing import Dict, List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import string

# Función para descargar recursos necesarios de NLTK
def download_nltk_resources():
    """
    Descarga automáticamente los recursos necesarios de NLTK si no están disponibles.
    
    Recursos descargados:
        - punkt: Para tokenización de oraciones
        - stopwords: Para filtrar palabras comunes
        - wordnet: Para lematización
        - omw-1.4: Base de datos multilingüe de WordNet
    
    Esta función verifica primero si cada recurso existe antes de descargarlo,
    evitando descargas innecesarias en ejecuciones posteriores.
    """
    resources = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']
    for resource in resources:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(resource)

download_nltk_resources()

class EmpatheticResponseGenerator:
    """
    Generador de Respuestas Empáticas
    
    Esta clase es el núcleo del sistema de generación de respuestas empáticas.
    Analiza texto emocional, identifica contextos, mide intensidad emocional
    y genera respuestas apropiadas y empáticas.
    
    Atributos:
        lemmatizer: Lematizador de WordNet para normalización de palabras
        stop_words: Conjunto de palabras comunes en inglés para filtrar
        intensity_words: Diccionario de palabras categorizadas por intensidad
        emotion_mapping: Mapeo de emociones específicas a categorías generales
        empathetic_patterns: Patrones de respuesta para cada emoción
        follow_up_phrases: Frases de seguimiento según intensidad emocional
        context_keywords: Palabras clave para identificación de contexto
    
    Métodos principales:
        - identify_context(): Identifica el contexto temático del texto
        - generate_context_summary(): Genera resumen contextual
        - calculate_emotional_intensity(): Calcula la intensidad emocional
        - convert_to_second_person(): Convierte texto de primera a segunda persona
        - generate_empathetic_response(): Genera la respuesta empática final
    """
    
    def __init__(self):
        """
        Inicializa el generador de respuestas empáticas con todas las configuraciones
        y diccionarios necesarios para el análisis y generación de respuestas.
        """
        # Herramientas de procesamiento de lenguaje natural
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))


        # Diccionario de palabras de intensidad emocional
        # Clasifica palabras según su nivel de intensidad para medir el estado emocional
        self.intensity_words = {
            'high': ['extremely', 'absolutely', 'completely', 'totally', 'really', 'very', 'so', 
                     'incredibly', 'devastated', 'furious', 'ecstatic', 'terrified', 'overwhelmed'],
            'medium': ['quite', 'rather', 'pretty', 'fairly', 'somewhat', 'moderately'],
            'low': ['a bit', 'slightly', 'kind of', 'sort of', 'a little']
        }

        # Mapeo de emociones específicas a categorías generales
        # Facilita el manejo de emociones variadas agrupándolas en categorías principales
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

        # Patrones de respuesta empática para cada emoción
        # Cada emoción tiene múltiples patrones para variety y naturalidad en las respuestas
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

        # Frases de seguimiento basadas en intensidad emocional
        # Proporcionan continuidad apropiada según el nivel de emoción detectado
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

        # Palabras clave para identificación de contexto temático
        # Agrupa palabras relacionadas por categorías para mejor clasificación contextual
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
        """
        Identifica el contexto temático principal del texto analizado.
        
        Analiza el texto buscando palabras clave específicas para determinar
        el contexto principal (trabajo, relaciones, salud, escuela, etc.).
        
        Args:
            text (str): Texto a analizar para identificación de contexto
            
        Returns:
            str: Categoría de contexto identificada ('work', 'relationship', 'health', etc.)
                 o 'general' si no se identifica un contexto específico
                 
        Proceso:
            1. Convierte el texto a minúsculas para análisis
            2. Busca palabras clave de cada categoría
            3. Asigna puntuaciones según coincidencias
            4. Retorna la categoría con mayor puntuación
        """
        text_lower = text.lower()
        context_scores = {}
        for context, keywords in self.context_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            score += sum(2 for keyword in keywords if f' {keyword} ' in f' {text_lower} ')
            if score > 0:
                context_scores[context] = score
        return max(context_scores, key=context_scores.get) if context_scores else 'general'

    def generate_context_summary(self, text: str) -> str:
        """
        Genera un resumen contextual del texto para usar en respuestas empáticas.
        
        Crea un resumen contextualizado que puede ser insertado en los patrones
        de respuesta empática, convirtiendo el texto de primera a segunda persona.
        
        Args:
            text (str): Texto original del usuario
            
        Returns:
            str: Resumen contextual en segunda persona para usar en respuestas
            
        Proceso:
            1. Identifica el tipo de contexto
            2. Extrae la oración más informativa
            3. Convierte de primera a segunda persona
            4. Retorna un resumen apropiado para respuestas empáticas
        """
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
            # Convertir de primera a segunda persona
            simplified = self.convert_to_second_person(main_sentence)
            return simplified
        return random.choice(context_phrases.get(context_type, ["what you're going through"]))

    def calculate_emotional_intensity(self, text: str) -> str:
        """
        Calcula la intensidad emocional del texto basándose en múltiples indicadores.
        
        Analiza varios aspectos del texto para determinar el nivel de intensidad
        emocional y seleccionar respuestas apropiadas.
        
        Args:
            text (str): Texto a analizar para intensidad emocional
            
        Returns:
            str: Nivel de intensidad ('high_intensity', 'medium_intensity', 'low_intensity')
            
        Indicadores analizados:
            - Signos de exclamación (peso: 2)
            - Signos de interrogación (peso: 1)
            - Palabras en mayúsculas (peso: 1)
            - Palabras de alta intensidad (peso: 3)
            - Palabras de intensidad media (peso: 1)
            - Letras repetidas (peso: 2)
        """
        text_lower = text.lower()
        exclamation_count = text.count('!')
        question_count = text.count('?')
        caps_words = len([word for word in text.split() if word.isupper() and len(word) > 1])
        high_score = sum(1 for word in self.intensity_words['high'] if word in text_lower)
        medium_score = sum(1 for word in self.intensity_words['medium'] if word in text_lower)
        repeated_letters = len(re.findall(r'(.)\1{2,}', text_lower))
        total = exclamation_count * 2 + question_count + caps_words + high_score * 3 + medium_score + repeated_letters * 2
        return 'high_intensity' if total > 4 else 'medium_intensity' if total > 1 else 'low_intensity'
    
    def convert_to_second_person(self, text: str) -> str:
        """
        Convierte texto de primera persona a segunda persona para respuestas empáticas.
        
        Transforma pronombres y formas verbales de primera persona a segunda persona
        para crear respuestas más directas y empáticas.
        
        Args:
            text (str): Texto en primera persona
            
        Returns:
            str: Texto convertido a segunda persona
            
        Conversiones realizadas:
            - "I am" → "you are"
            - "I feel" → "you feel"
            - "my" → "your"
            - "me" → "you"
            - Y muchas otras formas verbales y pronominales
            
        Características:
            - Preserva la capitalización original
            - Usa expresiones regulares para coincidencias exactas
            - Maneja contracciones y formas verbales complejas
        """
        # Diccionario de conversiones
        conversions = {
            r'\bI am\b': 'you are',
            r'\bI\'m\b': 'you\'re',
            r'\bI was\b': 'you were',
            r'\bI have\b': 'you have',
            r'\bI\'ve\b': 'you\'ve',
            r'\bI had\b': 'you had',
            r'\bI\'d\b': 'you\'d',
            r'\bI will\b': 'you will',
            r'\bI\'ll\b': 'you\'ll',
            r'\bI can\b': 'you can',
            r'\bI can\'t\b': 'you can\'t',
            r'\bI cannot\b': 'you cannot',
            r'\bI do\b': 'you do',
            r'\bI don\'t\b': 'you don\'t',
            r'\bI did\b': 'you did',
            r'\bI didn\'t\b': 'you didn\'t',
            r'\bI feel\b': 'you feel',
            r'\bI think\b': 'you think',
            r'\bI know\b': 'you know',
            r'\bI want\b': 'you want',
            r'\bI need\b': 'you need',
            r'\bI like\b': 'you like',
            r'\bI love\b': 'you love',
            r'\bI hate\b': 'you hate',
            r'\bI get\b': 'you get',
            r'\bI got\b': 'you got',
            r'\bI went\b': 'you went',
            r'\bI go\b': 'you go',
            r'\bI see\b': 'you see',
            r'\bI saw\b': 'you saw',
            r'\bI hear\b': 'you hear',
            r'\bI heard\b': 'you heard',
            r'\bI\b': 'you',
            r'\bme\b': 'you',
            r'\bmy\b': 'your',
            r'\bmine\b': 'yours',
            r'\bmyself\b': 'yourself'
        }
        
        result = text
        for pattern, replacement in conversions.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Ajustar la capitalización si es necesario
        if result and result[0].islower() and text[0].isupper():
            result = result[0].upper() + result[1:]
            
        return result
    
    def generate_empathetic_response(self, text: str, emotion: str) -> str:
        """
        Genera una respuesta empática completa basada en el texto y emoción detectados.
        
        Método principal que coordina todo el proceso de análisis y generación
        de respuestas empáticas personalizadas.
        
        Args:
            text (str): Texto original del usuario
            emotion (str): Emoción detectada en el texto
            
        Returns:
            str: Respuesta empática completa con contexto y seguimiento
            
        Proceso de generación:
            1. Normaliza la emoción recibida
            2. Mapea emociones desconocidas a categorías principales
            3. Genera contexto personalizado del texto
            4. Selecciona patrón de respuesta apropiado
            5. Calcula intensidad emocional
            6. Añade frase de seguimiento apropiada
            7. Combina todo en una respuesta coherente
            
        Características:
            - Respuestas contextualizadas y personalizadas
            - Manejo robusto de emociones no reconocidas
            - Intensidad emocional adaptativa
            - Frases de seguimiento apropiadas
        """
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
        print("CONTEXT:", context)  # Debugging line to check context generation
        pattern = random.choice(self.empathetic_patterns.get(emotion, self.empathetic_patterns['neutral']))
        main_response = pattern.format(context=context)
        follow_up = random.choice(self.follow_up_phrases[self.calculate_emotional_intensity(text)])
        return f"{main_response} {follow_up}"

# ==================== SECCIÓN DE PRUEBAS ====================
# Ejecución de casos de prueba para validar el funcionamiento del generador

if __name__ == "__main__":
    """
    Sección de pruebas para validar el funcionamiento del generador de respuestas empáticas.
    
    Incluye casos de prueba para diferentes emociones y contextos:
    - Anger (ira): Frustración laboral
    - Sadness (tristeza): Pérdida personal
    - Fear (miedo): Ansiedad por presentación
    - Joy (alegría): Promoción laboral
    - Surprise (sorpresa): Noticia inesperada
    - Embarrassment (vergüenza): Situación incómoda
    - Disappointment (decepción): Planes cancelados
    
    Cada caso muestra:
    - Texto original del usuario
    - Emoción detectada
    - Respuesta empática generada
    """
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
