# Diario Emocional - Web Interface

## Overview

This is a web-based version of the Emotional Diary application that provides:

- **Flask Backend**: REST API for emotion analysis and empathetic response generation
- **Modern Web Interface**: Responsive design using Bootstrap 5
- **Voice Recording**: Browser-based WebRTC audio recording
- **Real-time Speech Recognition**: Convert speech to text for analysis
- **Emotion Analysis**: ML-powered emotion detection from text
- **Empathetic Responses**: AI-generated supportive messages
- **Multi-language Support**: Spanish interface with empathetic responses

## Features

### 🎯 Core Functionality
- Text input for emotional expression
- Voice recording with WebRTC
- Real-time emotion analysis
- Context-aware empathetic responses
- Emotional intensity assessment
- Context detection (work, relationships, health, etc.)

### 🎨 User Interface
- Responsive Bootstrap 5 design
- Modern gradient styling
- Animated elements and smooth transitions
- Mobile-friendly responsive layout
- Intuitive card-based interface

### 🤖 AI & ML Integration
- Text emotion classification using transformers
- Empathetic response generation using NLTK
- Context analysis and categorization
- Emotional intensity scoring
- Multi-language support

## Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Modern web browser with WebRTC support

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Diario-Emocional
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask application:**
   ```bash
   python web_app.py
   ```

4. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Usage

### Text Analysis
1. Enter your thoughts or feelings in the text area
2. Click "Analizar Texto" to analyze your emotions
3. View the results showing:
   - Detected emotion
   - Emotional intensity
   - Context category
   - Empathetic response

### Voice Recording
1. Click "Iniciar Grabación" to start recording
2. Speak your thoughts (the interface will show recording status)
3. Click "Detener Grabación" to stop
4. The audio will be automatically transcribed and analyzed

## API Endpoints

### POST /analyze
Analyze text for emotions and generate empathetic response.

**Request:**
```json
{
  "text": "Your emotional expression here"
}
```

**Response:**
```json
{
  "emotion": "alegría",
  "empathetic_response": "Generated empathetic response",
  "intensity": "alta",
  "context": "trabajo",
  "original_text": "Your input text",
  "raw_emotion": "joy",
  "raw_context": "work"
}
```

### POST /transcribe
Transcribe audio and analyze emotions.

**Request:**
```json
{
  "audio_data": "base64-encoded-audio-data"
}
```

**Response:**
```json
{
  "text": "Transcribed text",
  "emotion": "tristeza",
  "empathetic_response": "Generated response",
  "intensity": "media",
  "context": "personal"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Project Structure

```
Diario-Emocional/
├── web_app.py              # Main Flask application
├── app/                    # Core application modules
│   ├── empathy.py         # Empathetic response generator
│   ├── emotion_text.py    # Text emotion analysis
│   └── ...                # Other modules
├── templates/             # HTML templates
│   └── index.html         # Main web interface
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Custom styling
│   └── js/
│       └── app.js         # Frontend JavaScript
├── ml_models/             # Pre-trained ML models
└── requirements.txt       # Python dependencies
```

## Technology Stack

### Backend
- **Flask 2.3.2**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **PyTorch**: ML model inference
- **Transformers**: Hugging Face transformers
- **NLTK**: Natural language processing
- **SpeechRecognition**: Audio transcription

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Custom styling with gradients and animations
- **JavaScript ES6+**: Modern JavaScript features
- **Bootstrap 5**: Responsive UI framework
- **WebRTC**: Browser-based audio recording

### ML Models
- **DistilBERT**: Text emotion classification
- **Custom Empathy Model**: Empathetic response generation
- **NLTK Resources**: Text processing and analysis

## Browser Compatibility

- **Chrome 60+** (recommended)
- **Firefox 55+**
- **Safari 11+**
- **Edge 79+**

*Note: WebRTC audio recording requires HTTPS in production environments.*

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python web_app.py
```

### Adding New Emotions
To add support for new emotions:

1. Update the emotion mapping in `web_app.py`
2. Add corresponding CSS classes in `static/css/style.css`
3. Update the translation function in `static/js/app.js`

### Customizing Empathetic Responses
Modify the empathy patterns in `app/empathy.py` to customize the empathetic response generation.

## Troubleshooting

### Common Issues

1. **Module not found errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **Audio recording not working**: Check browser permissions and ensure HTTPS in production
3. **Model loading errors**: Verify that the ML models are present in the `ml_models/` directory
4. **NLTK data missing**: The app will automatically download required NLTK resources on first run

### Performance Optimization

- The ML models are loaded once at startup for better performance
- Static files are served directly by Flask (use a web server like Nginx in production)
- Browser caching is enabled for static assets

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face for the pre-trained transformer models
- Bootstrap team for the UI framework
- NLTK community for natural language processing tools