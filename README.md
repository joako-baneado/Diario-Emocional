# Diario Emocional - Emotional Diary Desktop Application

A desktop application for emotional diary functionality with empathetic response generation.

## Features

- **Modern GUI Interface**: Clean, dark-themed interface built with tkinter
- **Text Input Processing**: Enter your thoughts and emotions via text input
- **Empathetic Response Generation**: AI-powered empathetic responses based on emotional content
- **Session Management**: Save and load emotional diary sessions
- **Multi-language Support**: Supports Spanish and English text processing
- **Emotional Context Analysis**: Identifies emotional contexts (work, relationships, health, etc.)
- **Intensity Detection**: Analyzes emotional intensity and provides appropriate responses

## Installation

### Prerequisites

- Python 3.8 or higher
- tkinter (usually comes with Python)
- Required Python packages (see requirements.txt)

### System Dependencies

On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3-tk python3-nltk python3-pil python3-pil.imagetk -y
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

Note: For full audio functionality (voice recording and transcription), you would also need:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio -y
pip install SpeechRecognition PyAudio
```

## Running the Application

### Method 1: Direct execution
```bash
python main.py
```

### Method 2: As a module
```bash
python -m app
```

## Usage

1. **Launch the application** using one of the methods above
2. **Enter your thoughts**: Type how you're feeling in the text input area
3. **Process emotions**: Click the "💭 Procesar Emociones" button
4. **View results**: 
   - Your original text appears in the "Tu texto" section
   - The empathetic response appears in the "Respuesta Empática" section
5. **Save session**: Click "💾 Guardar" to save your session to a file
6. **Clear**: Click "🗑️ Limpiar" to clear all text areas
7. **Try example**: Click "📝 Ejemplo" to load a sample text

## Features in Detail

### Empathetic Response Generation

The application uses a sophisticated empathetic response system that:

- **Analyzes emotional content** of your text
- **Identifies context** (work, relationships, health, personal, etc.)
- **Calculates emotional intensity** (high, medium, low)
- **Generates appropriate responses** based on emotion type and context
- **Provides follow-up questions** to encourage further reflection

### Supported Emotions

- **Positive emotions**: joy, gratitude, excitement, pride, relief, etc.
- **Negative emotions**: anger, sadness, fear, frustration, disappointment, etc.
- **Neutral emotions**: confusion, surprise, neutral states

### Context Recognition

The system recognizes various life contexts:
- Work and career
- Relationships and family
- Health and wellness
- Education and learning
- Financial concerns
- Personal development

## File Structure

```
Diario-Emocional/
├── app/
│   ├── __init__.py
│   ├── __main__.py          # Module entry point
│   ├── simple_gui.py        # Main GUI application
│   ├── empathy.py           # Empathetic response generation
│   ├── recorder.py          # Audio recording (for future use)
│   ├── transcriber.py       # Audio transcription (for future use)
│   └── ...
├── main.py                  # Main entry point
├── requirements.txt         # Python dependencies
├── test_empathy.py         # Test empathy functionality
├── test_gui_structure.py   # Test GUI structure
└── README.md               # This file
```

## Technical Details

### GUI Framework
- **tkinter**: Standard Python GUI library
- **Dark theme**: Custom styling for modern appearance
- **Responsive design**: Adapts to different window sizes
- **Threading**: Background processing to prevent UI freezing

### Natural Language Processing
- **NLTK**: Natural Language Toolkit for text processing
- **Context analysis**: Keyword-based context identification
- **Emotion mapping**: Multi-emotion support with intensity analysis
- **Response patterns**: Template-based response generation

### Future Enhancements

The application is designed to support future enhancements:

1. **Voice Recording**: Integration with `recorder.py` for audio input
2. **Speech Transcription**: Using `transcriber.py` for speech-to-text
3. **Machine Learning**: Enhanced emotion detection with ML models
4. **Data Persistence**: Database storage for session history
5. **Export Options**: PDF/Word export of sessions
6. **Multi-language**: Extended language support

## Testing

### Run Empathy Tests
```bash
python test_empathy.py
```

### Run GUI Structure Tests
```bash
python test_gui_structure.py
```

## Troubleshooting

### Common Issues

1. **tkinter not found**: Install `python3-tk` package
2. **NLTK data missing**: The application will automatically download required NLTK data
3. **Display issues**: Ensure you have a graphical environment for GUI applications

### Development Mode

For development, you can run individual components:

```bash
# Test empathy responses
python -c "from app.empathy import EmpatheticResponseGenerator; g = EmpatheticResponseGenerator(); print(g.generate_empathetic_response('I am happy', 'joy'))"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Diario Emocional application suite.