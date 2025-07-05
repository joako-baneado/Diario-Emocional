from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys
import logging
import tempfile
import base64
import wave
import io
import json

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import the existing modules
try:
    from app.empathy import EmpatheticResponseGenerator, download_nltk_resources
    from app.emotion_text import predict_emotion
except ImportError:
    # Fallback for when running from different directory
    from empathy import EmpatheticResponseGenerator, download_nltk_resources
    from emotion_text import predict_emotion
import speech_recognition as sr

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the empathy generator
empathy_generator = EmpatheticResponseGenerator()

# Download required NLTK resources
download_nltk_resources()

@app.route('/')
def index():
    """Main page with the emotional diary interface"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze text for emotion and generate empathetic response"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze emotion
        emotion = predict_emotion(text)
        logger.info(f"Detected emotion: {emotion}")
        
        # Generate empathetic response
        empathetic_response = empathy_generator.generate_empathetic_response(text, emotion)
        
        # Get emotional intensity
        intensity = empathy_generator.calculate_emotional_intensity(text)
        
        # Get context
        context = empathy_generator.identify_context(text)
        
        # Create emotion mapping for better translation
        emotion_mapping = {
            'joy': 'alegría',
            'sadness': 'tristeza',
            'anger': 'ira',
            'fear': 'miedo',
            'surprise': 'sorpresa',
            'disgust': 'disgusto',
            'neutral': 'neutral',
            'annoyance': 'irritación',
            'anxiety': 'ansiedad',
            'happiness': 'felicidad',
            'love': 'amor',
            'embarrassment': 'vergüenza',
            'disappointment': 'decepción'
        }
        
        # Context mapping for better translation
        context_mapping = {
            'work': 'trabajo',
            'relationship': 'relaciones',
            'health': 'salud',
            'school': 'estudios',
            'financial': 'finanzas',
            'personal': 'personal',
            'general': 'general'
        }
        
        # Translate emotion and context
        translated_emotion = emotion_mapping.get(emotion.lower(), emotion)
        translated_context = context_mapping.get(context.lower(), context)
        
        return jsonify({
            'emotion': translated_emotion,
            'empathetic_response': empathetic_response,
            'intensity': intensity,
            'context': translated_context,
            'original_text': text,
            'raw_emotion': emotion,
            'raw_context': context
        })
    
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        return jsonify({'error': f'Error analyzing text: {str(e)}'}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio to text and analyze emotions"""
    try:
        data = request.get_json()
        audio_data = data.get('audio_data', '')
        
        if not audio_data:
            return jsonify({'error': 'No audio data provided'}), 400
        
        # Decode base64 audio data
        audio_bytes = base64.b64decode(audio_data.split(',')[1])
        
        # Create temporary file for audio processing
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            # Initialize speech recognition
            recognizer = sr.Recognizer()
            
            # Read the audio file
            with sr.AudioFile(tmp_file_path) as source:
                audio = recognizer.record(source)
            
            # Recognize speech
            try:
                text = recognizer.recognize_google(audio, language='es-ES')
                logger.info(f"Transcribed text: {text}")
                
                # Analyze emotion
                emotion = predict_emotion(text)
                
                # Generate empathetic response
                empathetic_response = empathy_generator.generate_empathetic_response(text, emotion)
                
                # Get emotional intensity
                intensity = empathy_generator.calculate_emotional_intensity(text)
                
                # Get context
                context = empathy_generator.identify_context(text)
                
                return jsonify({
                    'text': text,
                    'emotion': emotion,
                    'empathetic_response': empathetic_response,
                    'intensity': intensity,
                    'context': context
                })
                
            except sr.UnknownValueError:
                return jsonify({'error': 'Could not understand audio'}), 400
            except sr.RequestError as e:
                return jsonify({'error': f'Speech recognition error: {str(e)}'}), 500
                
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
    
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return jsonify({'error': f'Error transcribing audio: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)