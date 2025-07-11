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

        # Patrones de respuesta empática mejorados para cada emoción
        # Cada emoción tiene múltiples patrones más naturales y contextualizados
        self.empathetic_patterns = {
            'anger': [
                "I can really sense the frustration in your words about {context}. That level of anger is completely understandable given what you're dealing with.",
                "Your anger comes through clearly when you talk about {context}. It's natural to feel this heated when facing such challenges.",
                "I hear how infuriated you are by {context}. That sounds like an incredibly maddening situation to be in.",
                "The frustration you're feeling about {context} is so valid. Anyone would be upset dealing with something like that.",
                "I can feel how much {context} has gotten under your skin. That kind of anger shows how much this matters to you.",
                "It's clear that {context} has really pushed you to your limit. Your anger is a completely normal response to such treatment."
            ],
            'sadness': [
                "I can feel the deep sadness in your words about {context}. That kind of pain must be so heavy to carry.",
                "The grief you're experiencing with {context} comes through so clearly. I'm sorry you're going through something this difficult.",
                "Your sadness about {context} is palpable. It takes real strength to share something this painful.",
                "I hear the heartbreak in what you're saying about {context}. That level of sorrow would be overwhelming for anyone.",
                "The pain you're feeling from {context} is so evident. You're dealing with something truly heart-wrenching.",
                "I can sense how much {context} is weighing on your heart. That depth of sadness shows how deeply you care."
            ],
            'fear': [
                "I can hear the real fear in your voice about {context}. Those concerns feel very legitimate and understandable.",
                "The anxiety you're experiencing around {context} makes complete sense. That uncertainty would be frightening for anyone.",
                "Your worry about {context} comes through so clearly. It's natural to feel scared when facing something unknown like this.",
                "I can feel how much {context} is causing you to worry. That kind of fear shows you're really thinking about what matters.",
                "The apprehension you have about {context} is completely valid. Anyone would feel nervous in your situation.",
                "I understand why {context} feels so threatening. Your fear is a normal response to such uncertainty."
            ],
            'joy': [
                "The happiness radiating from your words about {context} is absolutely infectious! I can feel your joy through every sentence.",
                "Your excitement about {context} is so wonderful to hear. It's beautiful when life brings us these bright moments.",
                "I love the enthusiasm in your voice when you talk about {context}. That kind of joy is truly special.",
                "The delight you're feeling about {context} really shines through. It's amazing how happiness can transform everything.",
                "Your pure joy regarding {context} is so heartwarming. These are the moments that make everything worthwhile.",
                "I can practically feel you glowing when you describe {context}. That level of happiness is absolutely magical."
            ],
            'surprise': [
                "What a shocking turn of events with {context}! I can only imagine how that must have caught you completely off guard.",
                "The surprise you experienced with {context} really comes through. That must have been such an unexpected moment.",
                "I can hear how absolutely stunned you were by {context}. Life certainly has a way of throwing us curveballs.",
                "That revelation about {context} sounds like it completely changed your perspective. What an unexpected development!",
                "The astonishment in your words about {context} is so clear. Sometimes life surprises us in the most unexpected ways.",
                "I can feel how bewildered you must be by {context}. That kind of surprise can really shake up everything we thought we knew."
            ],
            'disgust': [
                "I can understand why {context} would be so off-putting to you. That kind of revulsion is a completely natural response.",
                "Your strong reaction to {context} makes perfect sense. Some things are just genuinely disturbing and wrong.",
                "The repulsion you feel toward {context} is completely justified. That sounds truly unpleasant to deal with.",
                "I hear how much {context} bothers you on a fundamental level. That kind of disgust shows your strong moral compass.",
                "Your aversion to {context} is completely understandable. Some situations are just inherently repulsive.",
                "I can feel how much {context} goes against your core values. That level of disgust shows you know what's right."
            ],
            'disappointment': [
                "The disappointment in your words about {context} is so palpable. That kind of letdown cuts really deep.",
                "I can hear how much {context} fell short of your hopes. That disappointment must sting so much.",
                "Your sense of being let down by {context} comes through clearly. Unmet expectations can be so crushing.",
                "The disillusionment you're feeling about {context} is completely understandable. That's such a hard pill to swallow.",
                "I can feel how deflated you are by {context}. When our hopes are dashed, it leaves such an empty feeling.",
                "Your disappointment about {context} is so valid. It hurts when reality doesn't match what we were hoping for."
            ],
            'embarrassment': [
                "I can sense how mortified you feel about {context}. That kind of embarrassment is so uncomfortable and overwhelming.",
                "The self-consciousness you're experiencing from {context} is completely understandable. We've all been in those cringe-worthy moments.",
                "Your embarrassment about {context} comes through so clearly. Those moments when we feel exposed are truly awful.",
                "I hear how much {context} made you want to disappear. That level of embarrassment is genuinely painful.",
                "The shame you're feeling about {context} is so relatable. Sometimes we just want the ground to swallow us up.",
                "I can feel how much {context} is making you second-guess yourself. Embarrassment has a way of making everything feel magnified."
            ],
            'neutral': [
                "Thank you for sharing your thoughts about {context}. I can hear that this is important to you, and I'm here to listen.",
                "I appreciate you opening up about {context}. Your perspective on this situation is really valuable.",
                "What you're sharing about {context} gives me insight into what you're experiencing. I'm glad you felt comfortable expressing this.",
                "I hear what you're saying about {context}. It's clear you've been thinking deeply about this situation.",
                "Your reflection on {context} shows a lot of thoughtfulness. I'm honored that you're sharing this with me.",
                "I can see that {context} has been on your mind. Thank you for trusting me with these thoughts."
            ]
        }

        # Frases de seguimiento mejoradas basadas en intensidad emocional
        # Proporcionan continuidad apropiada y más natural según el nivel de emoción detectado
        self.follow_up_phrases = {
            'high_intensity': [
                "Would you like to talk more about this?",
                "How are you coping with everything right now?",
                "Is there anything specific that might help you feel better?",
                "Would it help to explore this situation further?",
                "What kind of support would be most helpful for you?",
                "Do you have people around you who understand what you're going through?",
                "How long have you been dealing with feelings this intense?",
                "What usually helps you when things feel this overwhelming?"
            ],
            'medium_intensity': [
                "How are you feeling about everything overall?",
                "Would you like to share more about your experience?",
                "What's been on your mind lately about this?",
                "How can I best support you through this situation?",
                "What would help you feel better about this?",
                "Have you been able to process these feelings with anyone?",
                "What aspects of this situation feel most challenging?",
                "How has this been affecting your daily life?"
            ],
            'low_intensity': [
                "Thanks for sharing this with me.",
                "I'm here if you need to talk more about it.",
                "How has your day been overall?",
                "What else has been on your mind?",
                "How are you doing with everything else in your life?",
                "Is there anything else you'd like to explore?",
                "What other thoughts or feelings have come up for you?",
                "How do you usually handle situations like this?"
            ]
        }

        # Palabras clave expandidas para identificación de contexto temático más precisa
        # Agrupa palabras relacionadas por categorías para mejor clasificación contextual
        self.context_keywords = {
            'work': ['job', 'work', 'boss', 'colleague', 'office', 'meeting', 'project', 'deadline', 
                     'career', 'workplace', 'coworker', 'manager', 'employee', 'salary', 'promotion',
                     'interview', 'resignation', 'fired', 'hired', 'overtime', 'corporate', 'company',
                     'supervisor', 'team', 'performance', 'evaluation', 'professional', 'business'],
            'relationship': ['partner', 'friend', 'family', 'relationship', 'love', 'breakup', 'dating',
                             'boyfriend', 'girlfriend', 'husband', 'wife', 'marriage', 'divorce',
                             'mother', 'father', 'sister', 'brother', 'parents', 'children', 'kids',
                             'ex', 'crush', 'romantic', 'social', 'friendship', 'argue', 'fight'],
            'health': ['sick', 'doctor', 'hospital', 'pain', 'health', 'medicine', 'treatment',
                       'illness', 'medical', 'diagnosis', 'surgery', 'therapy', 'symptoms',
                       'tired', 'exhausted', 'headache', 'fever', 'appointment', 'prescription'],
            'school': ['school', 'teacher', 'student', 'exam', 'grade', 'homework', 'class',
                       'university', 'college', 'study', 'education', 'degree', 'semester',
                       'course', 'professor', 'assignment', 'thesis', 'graduation', 'academic'],
            'financial': ['money', 'financial', 'budget', 'debt', 'bills', 'expense', 'income',
                          'savings', 'loan', 'credit', 'payment', 'broke', 'expensive', 'cheap',
                          'afford', 'purchase', 'investment', 'mortgage', 'rent', 'tax'],
            'personal': ['myself', 'personal', 'identity', 'self', 'confidence', 'growth',
                         'anxiety', 'depression', 'stress', 'mental', 'therapy', 'counseling',
                         'lonely', 'overwhelmed', 'tired', 'emotional', 'feelings', 'thoughts'],
            'life_events': ['birthday', 'wedding', 'funeral', 'graduation', 'moving', 'travel',
                           'vacation', 'holiday', 'celebration', 'anniversary', 'milestone'],
            'loss_grief': ['death', 'died', 'funeral', 'grief', 'loss', 'goodbye', 'memorial',
                          'miss', 'gone', 'passed away', 'mourning', 'grieving']
        }

        # Patrones contextuales más específicos para mejor análisis
        self.context_patterns = {
            'work_stress': ['deadline', 'pressure', 'overtime', 'workload', 'demanding'],
            'work_conflict': ['boss', 'manager', 'colleague', 'workplace drama', 'unfair'],
            'relationship_conflict': ['argue', 'fight', 'disagree', 'tension', 'misunderstanding'],
            'relationship_loss': ['breakup', 'divorce', 'separation', 'ended', 'over'],
            'health_concern': ['worried about', 'symptoms', 'pain', 'sick', 'medical'],
            'academic_pressure': ['exam', 'test', 'grade', 'failing', 'stressed about school'],
            'financial_stress': ['can\'t afford', 'broke', 'bills', 'debt', 'money problems'],
            'personal_growth': ['learning', 'improving', 'changing', 'developing', 'working on myself'],
            'life_transition': ['moving', 'new job', 'starting', 'ending', 'change']
        }

    def identify_context(self, text: str) -> Dict[str, any]:
        """
        Identifica el contexto temático principal del texto con análisis más detallado.
        
        Analiza el texto buscando palabras clave específicas, patrones contextuales
        y elementos emocionales para determinar un contexto rico y detallado.
        
        Args:
            text (str): Texto a analizar para identificación de contexto
            
        Returns:
            Dict[str, any]: Diccionario con información contextual detallada:
                - main_context: Categoría principal del contexto
                - sub_context: Sub-categoría específica si se detecta
                - key_elements: Elementos clave encontrados en el texto
                - emotional_triggers: Palabras o frases que indican carga emocional
                - temporal_indicators: Indicadores temporales (pasado, presente, futuro)
                 
        Proceso:
            1. Convierte el texto a minúsculas para análisis
            2. Busca palabras clave de cada categoría con pesos diferenciados
            3. Identifica patrones contextuales específicos
            4. Detecta elementos emocionales y temporales
            5. Retorna información contextual completa
        """
        text_lower = text.lower()
        context_scores = {}
        detected_patterns = []
        key_elements = []
        emotional_triggers = []
        temporal_indicators = {'past': False, 'present': False, 'future': False}
        
        # Análisis básico de categorías con pesos mejorados
        for context, keywords in self.context_keywords.items():
            score = 0
            found_keywords = []
            for keyword in keywords:
                if f' {keyword} ' in f' {text_lower} ':
                    score += 3  # Palabra completa tiene mayor peso
                    found_keywords.append(keyword)
                elif keyword in text_lower:
                    score += 1  # Palabra parcial tiene menor peso
                    found_keywords.append(keyword)
            
            if score > 0:
                context_scores[context] = score
                key_elements.extend(found_keywords)
        
        # Análisis de patrones contextuales específicos
        for pattern_name, pattern_words in self.context_patterns.items():
            for pattern in pattern_words:
                if pattern in text_lower:
                    detected_patterns.append(pattern_name)
                    context_scores[pattern_name.split('_')[0]] = context_scores.get(pattern_name.split('_')[0], 0) + 5
        
        # Detección de indicadores temporales
        past_indicators = ['was', 'were', 'had', 'did', 'yesterday', 'last', 'ago', 'before', 'used to']
        present_indicators = ['am', 'is', 'are', 'now', 'today', 'currently', 'right now']
        future_indicators = ['will', 'going to', 'tomorrow', 'next', 'soon', 'planning', 'hope']
        
        if any(indicator in text_lower for indicator in past_indicators):
            temporal_indicators['past'] = True
        if any(indicator in text_lower for indicator in present_indicators):
            temporal_indicators['present'] = True
        if any(indicator in text_lower for indicator in future_indicators):
            temporal_indicators['future'] = True
        
        # Detección de disparadores emocionales
        emotion_triggers = ['frustrated', 'angry', 'upset', 'sad', 'happy', 'excited', 'worried', 
                           'anxious', 'scared', 'disappointed', 'overwhelmed', 'stressed', 'confused']
        emotional_triggers = [trigger for trigger in emotion_triggers if trigger in text_lower]
        
        # Determinar contexto principal y sub-contexto
        main_context = max(context_scores, key=context_scores.get) if context_scores else 'general'
        sub_context = None
        
        # Identificar sub-contexto basado en patrones detectados
        relevant_patterns = [p for p in detected_patterns if p.startswith(main_context)]
        if relevant_patterns:
            sub_context = relevant_patterns[0]
        
        return {
            'main_context': main_context,
            'sub_context': sub_context,
            'key_elements': list(set(key_elements)),
            'emotional_triggers': emotional_triggers,
            'temporal_indicators': temporal_indicators,
            'detected_patterns': detected_patterns,
            'context_score': context_scores.get(main_context, 0)
        }

    def extract_key_phrases(self, text: str, context_info: Dict[str, any]) -> List[str]:
        """
        Extrae frases clave del texto que son relevantes para el contexto emocional.
        
        Identifica y extrae las frases más significativas del texto que pueden
        ser utilizadas para crear respuestas más personalizadas y específicas.
        
        Args:
            text (str): Texto original del usuario
            context_info (Dict): Información contextual del texto
            
        Returns:
            List[str]: Lista de frases clave extraídas y procesadas
        """
        # Tokenizar el texto en oraciones
        sentences = re.split(r'[.!?]\s+', text.strip())
        key_phrases = []
        
        # Filtrar oraciones significativas (más de 3 palabras)
        meaningful_sentences = [s.strip() for s in sentences if len(s.split()) > 3]
        
        # Priorizar oraciones que contienen elementos contextuales clave
        for sentence in meaningful_sentences:
            sentence_lower = sentence.lower()
            relevance_score = 0
            
            # Incrementar puntuación por elementos contextuales
            for element in context_info.get('key_elements', []):
                if element in sentence_lower:
                    relevance_score += 2
            
            # Incrementar puntuación por disparadores emocionales
            for trigger in context_info.get('emotional_triggers', []):
                if trigger in sentence_lower:
                    relevance_score += 3
            
            # Incrementar puntuación por palabras de intensidad
            for intensity_list in self.intensity_words.values():
                for word in intensity_list:
                    if word in sentence_lower:
                        relevance_score += 1
            
            if relevance_score > 0:
                key_phrases.append((sentence, relevance_score))
        
        # Ordenar por relevancia y tomar las mejores
        key_phrases.sort(key=lambda x: x[1], reverse=True)
        return [phrase[0] for phrase in key_phrases[:3]]  # Top 3 frases más relevantes

    def generate_context_summary(self, text: str) -> str:
        """
        Genera un resumen contextual más natural y específico del texto.
        
        Crea un resumen contextualizado que se integra de manera fluida en las
        respuestas empáticas, considerando el contexto específico y elementos emocionales.
        
        Args:
            text (str): Texto original del usuario
            
        Returns:
            str: Resumen contextual natural para usar en respuestas
        """
        context_info = self.identify_context(text)
        main_context = context_info['main_context']
        sub_context = context_info['sub_context']
        key_elements = context_info['key_elements']
        emotional_triggers = context_info['emotional_triggers']
        temporal_indicators = context_info['temporal_indicators']
        
        # Extraer frases clave del texto
        key_phrases = self.extract_key_phrases(text, context_info)
        
        # Generar resumen basado en el contexto específico y sub-contexto
        if sub_context:
            summary = self._generate_specific_context_summary(main_context, sub_context, key_phrases, emotional_triggers, temporal_indicators)
        else:
            summary = self._generate_general_context_summary(main_context, key_phrases, key_elements, emotional_triggers, temporal_indicators)
        
        return summary

    def _generate_specific_context_summary(self, main_context: str, sub_context: str, 
                                         key_phrases: List[str], emotional_triggers: List[str],
                                         temporal_indicators: Dict[str, bool]) -> str:
        """Genera resumen para contextos específicos identificados."""
        
        # Mapeo de sub-contextos a descripciones naturales
        specific_summaries = {
            'work_stress': "the intense pressure and demands you're facing at work",
            'work_conflict': "the difficult situation you're dealing with at your workplace",
            'relationship_conflict': "the tensions and disagreements in your relationship",
            'relationship_loss': "the painful end of your relationship",
            'health_concern': "the health issues you're worried about",
            'academic_pressure': "the academic stress and pressure you're under",
            'financial_stress': "the financial difficulties you're going through",
            'personal_growth': "the personal changes and growth you're experiencing",
            'life_transition': "the major life changes you're navigating"
        }
        
        if sub_context in specific_summaries:
            base_summary = specific_summaries[sub_context]
        else:
            base_summary = f"what you're experiencing with {main_context}"
        
        # Añadir elementos temporales para más naturalidad
        if temporal_indicators['past']:
            base_summary = base_summary.replace("you're", "you were")
            base_summary = f"what you went through with {base_summary}"
        elif temporal_indicators['future']:
            base_summary = f"what you're anticipating with {base_summary}"
        
        # Integrar elementos emocionales si están presentes
        if emotional_triggers:
            primary_emotion = emotional_triggers[0]
            base_summary = f"how {primary_emotion} you're feeling about {base_summary}"
        
        return base_summary

    def _generate_general_context_summary(self, main_context: str, key_phrases: List[str], 
                                        key_elements: List[str], emotional_triggers: List[str],
                                        temporal_indicators: Dict[str, bool]) -> str:
        """Genera resumen para contextos generales."""
        
        # Si tenemos frases clave, usar la más relevante convertida a segunda persona
        if key_phrases:
            best_phrase = key_phrases[0]
            converted_phrase = self.convert_to_second_person(best_phrase)
            
            # Limpiar y simplificar la frase
            converted_phrase = re.sub(r'^(you\s+)', '', converted_phrase, flags=re.IGNORECASE).strip()
            converted_phrase = converted_phrase.lower()
            
            # Asegurar que comience de manera natural
            if not converted_phrase.startswith(('the', 'this', 'what', 'how', 'that')):
                converted_phrase = f"what happened with {converted_phrase}"
            
            return converted_phrase
        
        # Fallback a descripciones contextuales generales
        context_descriptions = {
            'work': "your work situation",
            'relationship': "your relationship situation", 
            'health': "your health concerns",
            'school': "your academic situation",
            'financial': "your financial concerns",
            'personal': "what you're going through personally",
            'life_events': "this important event in your life",
            'loss_grief': "the loss you're experiencing"
        }
        
        base_description = context_descriptions.get(main_context, "what you're going through")
        
        # Añadir especificidad si hay elementos clave prominentes
        if key_elements:
            prominent_elements = [elem for elem in key_elements if len(elem) > 3][:2]
            if prominent_elements:
                elements_str = " and ".join(prominent_elements)
                base_description = f"the challenges with {elements_str}"
        
        return base_description

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
        Genera una respuesta empática completa y mejorada basada en el texto y emoción detectadas.
        
        Método principal que coordina todo el proceso de análisis avanzado y generación
        de respuestas empáticas contextualizadas y naturales.
        
        Args:
            text (str): Texto original del usuario
            emotion (str): Emoción detectada en el texto
            
        Returns:
            str: Respuesta empática completa con contexto rico y seguimiento
            
        Proceso de generación mejorado:
            1. Análisis contextual profundo del texto
            2. Normalización y mapeo inteligente de emociones
            3. Generación de contexto natural y específico
            4. Selección de patrón de respuesta contextualizado
            5. Cálculo de intensidad emocional para personalización
            6. Integración fluida de elementos contextuales
            7. Adición de seguimiento apropiado según intensidad
            
        Características avanzadas:
            - Análisis contextual multi-dimensional
            - Respuestas naturales y específicas
            - Integración fluida del contexto personal
            - Adaptación según intensidad emocional
            - Manejo robusto de emociones complejas
        """
        # Paso 1: Análisis contextual profundo
        context_info = self.identify_context(text)
        
        # Paso 2: Normalización inteligente de emociones
        emotion = emotion.lower()
        if emotion not in self.empathetic_patterns:
            emotion_category = self.emotion_mapping.get(emotion, 'neutral')
            
            # Mapeo más inteligente basado en contexto y contenido
            if emotion_category == 'positive':
                if any(word in text.lower() for word in ['excited', 'thrilled', 'amazing', 'fantastic']):
                    emotion = 'joy'
                elif context_info['main_context'] == 'work' and any(word in text.lower() for word in ['promotion', 'success', 'achieved']):
                    emotion = 'joy'
                else:
                    emotion = 'joy'
                    
            elif emotion_category == 'negative':
                # Mapeo contextual más preciso
                text_lower = text.lower()
                
                if context_info['sub_context'] == 'work_stress' or any(word in text_lower for word in ['frustrated', 'angry', 'mad', 'infuriated']):
                    emotion = 'anger'
                elif context_info['sub_context'] in ['relationship_loss', 'loss_grief'] or any(word in text_lower for word in ['sad', 'depressed', 'heartbroken', 'devastated']):
                    emotion = 'sadness'
                elif any(word in text_lower for word in ['scared', 'afraid', 'worried', 'anxious', 'nervous']):
                    emotion = 'fear'
                elif any(word in text_lower for word in ['disappointed', 'let down', 'expected', 'hoped']):
                    emotion = 'disappointment'
                elif any(word in text_lower for word in ['embarrassed', 'ashamed', 'humiliated', 'mortified']):
                    emotion = 'embarrassment'
                elif any(word in text_lower for word in ['disgusted', 'repulsed', 'sick', 'revolting']):
                    emotion = 'disgust'
                else:
                    # Default basado en contexto
                    if context_info['main_context'] in ['work', 'school']:
                        emotion = 'anger'  # Más común en contextos de estrés
                    else:
                        emotion = 'sadness'
            else:
                emotion = 'neutral'
        
        # Paso 3: Generación de contexto natural y específico
        context_summary = self.generate_context_summary(text)
        
        # Paso 4: Selección de patrón contextualizado
        available_patterns = self.empathetic_patterns.get(emotion, self.empathetic_patterns['neutral'])
        
        # Seleccionar patrón más apropiado basado en contexto e intensidad
        intensity = self.calculate_emotional_intensity(text)
        
        # Filtrar patrones según intensidad cuando sea apropiado
        if intensity == 'high_intensity':
            # Para alta intensidad, preferir patrones más fuertes
            preferred_patterns = [p for p in available_patterns if any(word in p.lower() for word in 
                                ['really', 'completely', 'absolutely', 'deeply', 'truly', 'so', 'incredibly'])]
            if preferred_patterns:
                available_patterns = preferred_patterns
        
        selected_pattern = random.choice(available_patterns)
        
        # Paso 5: Formatear respuesta con contexto
        main_response = selected_pattern.format(context=context_summary)
        
        # Paso 6: Seleccionar seguimiento apropiado
        follow_up_options = self.follow_up_phrases[intensity]
        
        # Personalizar seguimiento basado en contexto cuando sea relevante
        if context_info['main_context'] == 'work' and intensity == 'high_intensity':
            work_specific_followups = [
                "How are you managing the stress at work?",
                "What support do you have in your workplace?", 
                "Have you been able to talk to anyone about this situation?"
            ]
            follow_up_options.extend(work_specific_followups)
        elif context_info['main_context'] == 'relationship' and emotion in ['sadness', 'anger']:
            relationship_followups = [
                "Do you have support from friends or family right now?",
                "How are you taking care of yourself through this?",
                "What has been helping you process these feelings?"
            ]
            follow_up_options.extend(relationship_followups)
        
        follow_up = random.choice(follow_up_options)
        
        # Paso 7: Combinar respuesta final con transición natural
        if intensity == 'high_intensity':
            return f"{main_response} {follow_up}"
        else:
            # Para intensidades menores, usar transiciones más suaves
            transitions = ["", "I'm curious, ", "I wonder, ", "If you don't mind me asking, "]
            transition = random.choice(transitions)
            return f"{main_response} {transition}{follow_up.lower()}"
    
    def analyze_emotional_context_depth(self, text: str, emotion: str, context_info: Dict[str, any]) -> Dict[str, any]:
        """
        Realiza un análisis profundo del contexto emocional para personalización avanzada.
        
        Combina información emocional y contextual para crear un perfil más rico
        que permita respuestas más precisas y empáticas.
        
        Args:
            text (str): Texto original del usuario
            emotion (str): Emoción detectada
            context_info (Dict): Información contextual previamente analizada
            
        Returns:
            Dict[str, any]: Análisis contextual profundo con recomendaciones
        """
        analysis = {
            'emotional_complexity': 'simple',
            'support_needs': [],
            'conversation_direction': 'general',
            'empathy_level': 'standard',
            'follow_up_suggestions': []
        }
        
        text_lower = text.lower()
        
        # Determinar complejidad emocional
        emotion_words = context_info.get('emotional_triggers', [])
        if len(emotion_words) > 2:
            analysis['emotional_complexity'] = 'complex'
        elif len(emotion_words) > 1:
            analysis['emotional_complexity'] = 'moderate'
        
        # Identificar necesidades de apoyo específicas
        if 'overwhelmed' in text_lower or 'too much' in text_lower:
            analysis['support_needs'].append('stress_management')
        if any(word in text_lower for word in ['alone', 'isolated', 'nobody']):
            analysis['support_needs'].append('social_connection')
        if any(word in text_lower for word in ['help', 'advice', 'what should']):
            analysis['support_needs'].append('guidance')
        if any(word in text_lower for word in ['understand', 'confused', 'don\'t know']):
            analysis['support_needs'].append('clarity')
        
        # Determinar dirección de conversación
        if context_info['main_context'] in ['work', 'school'] and emotion in ['anger', 'stress']:
            analysis['conversation_direction'] = 'problem_solving'
        elif context_info['main_context'] == 'relationship' and emotion in ['sadness', 'anger']:
            analysis['conversation_direction'] = 'emotional_processing'
        elif emotion == 'fear':
            analysis['conversation_direction'] = 'reassurance'
        elif emotion == 'joy':
            analysis['conversation_direction'] = 'celebration'
        
        # Ajustar nivel de empatía
        intensity = self.calculate_emotional_intensity(text)
        if intensity == 'high_intensity' and emotion in ['sadness', 'fear', 'anger']:
            analysis['empathy_level'] = 'high'
        elif context_info['main_context'] in ['loss_grief', 'health']:
            analysis['empathy_level'] = 'high'
        
        return analysis

# ==================== SECCIÓN DE PRUEBAS ====================
# Ejecución de casos de prueba para validar el funcionamiento del generador

if __name__ == "__main__":
    """
    Sección de pruebas mejorada para validar el funcionamiento del generador de respuestas empáticas.
    
    Incluye casos de prueba variados que demuestran las capacidades mejoradas:
    - Análisis contextual profundo
    - Respuestas más naturales y específicas
    - Mejor integración del contexto personal
    - Manejo de emociones complejas
    """
    generator = EmpatheticResponseGenerator()
    
    # Casos de prueba expandidos con contextos más específicos y realistas
    test_cases = [
        # Casos de trabajo con diferentes sub-contextos
        ("I'm absolutely furious with my manager. He keeps giving me impossible deadlines while my colleagues get easy assignments. I've been working overtime every day this week and I'm completely burned out.", "anger"),
        ("I just found out I didn't get the promotion I've been working toward for two years. My boss gave it to someone who just started six months ago. I feel so defeated and don't know if I should even stay at this company.", "disappointment"),
        
        # Casos de relaciones con más detalle emocional
        ("My girlfriend of three years broke up with me yesterday. She said she needs space to figure things out, but I think she's seeing someone else. I'm devastated and can't stop crying. I don't know how to move on from this.", "sadness"),
        ("I had the most amazing date last night! We talked for hours and I felt like I could be completely myself. I haven't felt this connected to someone in years and I'm so excited to see where this goes.", "joy"),
        
        # Casos de salud con preocupaciones específicas
        ("I've been having these chest pains for weeks and the doctor wants to run more tests. I'm terrified that it might be something serious. I can't sleep and I keep imagining the worst-case scenarios.", "fear"),
        
        # Casos académicos con presión específica
        ("I'm three weeks behind on my thesis and my advisor is getting impatient. I feel like I'm drowning in research and I don't even know if my argument makes sense anymore. Everyone else seems to have it figured out.", "anxiety"),
        
        # Casos de vida personal complejos
        ("I feel so embarrassed about what happened at the party last weekend. I got way too drunk and said some things I shouldn't have. Now my friends are acting weird around me and I don't know how to fix it.", "embarrassment"),
        ("My mom called to tell me my childhood dog passed away. I know it sounds silly, but I've had him since I was eight and he was like my best friend. I'm at work trying not to cry but I feel so empty inside.", "grief"),
        
        # Casos con emociones mixtas
        ("I got accepted into my dream graduate program, but it means moving across the country and leaving my family behind. I'm excited but also terrified about starting over in a new place where I don't know anyone.", "mixed_emotions"),
        
        # Casos de transiciones de vida
        ("I'm getting married in two months and everyone keeps asking if I'm excited. Honestly, I'm having second thoughts. I love my fiancé but I'm scared about making such a huge commitment. What if we're not ready?", "confusion")
    ]

    print("=== Generador de Respuestas Empáticas - Versión Mejorada ===\n")
    print("Demostrando capacidades mejoradas de análisis contextual y respuestas naturales:\n")
    
    for i, (text, emotion) in enumerate(test_cases, 1):
        print(f"CASO {i}:")
        print(f"Texto: \"{text}\"")
        print(f"Emoción detectada: {emotion}")
        
        # Mostrar análisis contextual
        context_info = generator.identify_context(text)
        print(f"Contexto principal: {context_info['main_context']}")
        if context_info['sub_context']:
            print(f"Sub-contexto: {context_info['sub_context']}")
        print(f"Elementos clave: {', '.join(context_info['key_elements'][:3])}")
        if context_info['emotional_triggers']:
            print(f"Disparadores emocionales: {', '.join(context_info['emotional_triggers'])}")
        
        # Generar y mostrar respuesta
        response = generator.generate_empathetic_response(text, emotion)
        print(f"RESPUESTA EMPÁTICA: {response}")
        print("-" * 100)
        print()

    print("\n=== Pruebas de Análisis Contextual Específico ===\n")
    
    # Casos para demostrar análisis contextual específico
    context_test_cases = [
        "I'm worried about my presentation tomorrow at work",
        "My relationship with my partner has been really difficult lately",
        "I'm struggling with my mental health and feeling really overwhelmed"
    ]
    
    for text in context_test_cases:
        print(f"Texto: \"{text}\"")
        context_info = generator.identify_context(text)
        context_summary = generator.generate_context_summary(text)
        print(f"Análisis contextual: {context_info}")
        print(f"Resumen contextual: \"{context_summary}\"")
        print("-" * 80)
        print()
