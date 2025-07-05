// Emotional Diary Web Application JavaScript

class EmotionalDiaryApp {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkBrowserSupport();
    }

    setupEventListeners() {
        // Text analysis
        document.getElementById('analyzeTextBtn').addEventListener('click', () => {
            this.analyzeText();
        });

        // Voice recording
        document.getElementById('startRecordingBtn').addEventListener('click', () => {
            this.startRecording();
        });

        document.getElementById('stopRecordingBtn').addEventListener('click', () => {
            this.stopRecording();
        });

        // Enter key support for text input
        document.getElementById('textInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.analyzeText();
            }
        });
    }

    checkBrowserSupport() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            this.showError('Tu navegador no soporta grabación de audio. Por favor, usa Chrome, Firefox, o Safari.');
            document.getElementById('startRecordingBtn').disabled = true;
        }
    }

    async analyzeText() {
        const text = document.getElementById('textInput').value.trim();
        
        if (!text) {
            this.showError('Por favor, ingresa algún texto para analizar.');
            return;
        }

        this.showLoading();
        this.hideError();

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            if (response.ok) {
                this.displayResults(data);
            } else {
                this.showError(data.error || 'Error analizando el texto');
            }
        } catch (error) {
            this.showError('Error de conexión: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100
                } 
            });

            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });

            this.audioChunks = [];
            this.isRecording = true;

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                this.processRecording();
            };

            this.mediaRecorder.start();

            // Update UI
            document.getElementById('startRecordingBtn').classList.add('d-none');
            document.getElementById('stopRecordingBtn').classList.remove('d-none');
            document.getElementById('recordingStatus').classList.remove('d-none');

            this.hideError();

        } catch (error) {
            this.showError('Error accediendo al micrófono: ' + error.message);
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;

            // Stop all tracks
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());

            // Update UI
            document.getElementById('startRecordingBtn').classList.remove('d-none');
            document.getElementById('stopRecordingBtn').classList.add('d-none');
            document.getElementById('recordingStatus').classList.add('d-none');
            document.getElementById('processingStatus').classList.remove('d-none');
        }
    }

    async processRecording() {
        try {
            // Create audio blob
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
            
            // Create audio URL for playback
            const audioUrl = URL.createObjectURL(audioBlob);
            const audioPlayer = document.getElementById('audioPlayback');
            audioPlayer.src = audioUrl;
            audioPlayer.classList.remove('d-none');

            // Convert to base64 for transmission
            const base64Audio = await this.blobToBase64(audioBlob);

            // Send to server for transcription and analysis
            const response = await fetch('/transcribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ audio_data: base64Audio })
            });

            const data = await response.json();

            if (response.ok) {
                // Update text input with transcribed text
                document.getElementById('textInput').value = data.text;
                
                // Display results
                this.displayResults(data);
            } else {
                this.showError(data.error || 'Error procesando el audio');
            }

        } catch (error) {
            this.showError('Error procesando la grabación: ' + error.message);
        } finally {
            document.getElementById('processingStatus').classList.add('d-none');
        }
    }

    blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    displayResults(data) {
        // Show results section
        document.getElementById('resultsSection').classList.remove('d-none');
        document.getElementById('responseSection').classList.remove('d-none');

        // Display emotion with appropriate styling
        const emotionBadge = document.getElementById('emotionResult');
        emotionBadge.textContent = data.emotion;
        emotionBadge.className = `badge bg-primary fs-6 emotion-${data.raw_emotion ? data.raw_emotion.toLowerCase() : data.emotion.toLowerCase()}`;

        // Display intensity with appropriate styling
        const intensityBadge = document.getElementById('intensityResult');
        intensityBadge.textContent = this.translateIntensity(data.intensity);
        intensityBadge.className = `badge bg-info fs-6 intensity-${data.intensity.toLowerCase().replace('_intensity', '')}`;

        // Display context with appropriate styling
        const contextBadge = document.getElementById('contextResult');
        contextBadge.textContent = data.context;
        contextBadge.className = `badge bg-success fs-6 context-${data.raw_context ? data.raw_context.toLowerCase() : data.context.toLowerCase()}`;

        // Display empathetic response
        document.getElementById('empatheticResponse').textContent = data.empathetic_response;

        // Smooth scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }

    translateEmotion(emotion) {
        const translations = {
            'joy': 'Alegría',
            'sadness': 'Tristeza',
            'anger': 'Ira',
            'fear': 'Miedo',
            'surprise': 'Sorpresa',
            'disgust': 'Disgusto',
            'neutral': 'Neutral'
        };
        return translations[emotion.toLowerCase()] || emotion;
    }

    translateIntensity(intensity) {
        const translations = {
            'high': 'Alta',
            'medium': 'Media',
            'low': 'Baja',
            'high_intensity': 'Alta',
            'medium_intensity': 'Media',
            'low_intensity': 'Baja'
        };
        return translations[intensity.toLowerCase()] || intensity;
    }

    translateContext(context) {
        const translations = {
            'work': 'Trabajo',
            'relationship': 'Relaciones',
            'health': 'Salud',
            'school': 'Estudios',
            'financial': 'Finanzas',
            'personal': 'Personal'
        };
        return translations[context.toLowerCase()] || context;
    }

    showLoading() {
        document.getElementById('loadingSpinner').classList.remove('d-none');
    }

    hideLoading() {
        document.getElementById('loadingSpinner').classList.add('d-none');
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorSection').classList.remove('d-none');
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }

    hideError() {
        document.getElementById('errorSection').classList.add('d-none');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EmotionalDiaryApp();
});

// Add some helpful keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl + R to start recording
    if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        const startBtn = document.getElementById('startRecordingBtn');
        const stopBtn = document.getElementById('stopRecordingBtn');
        
        if (!startBtn.classList.contains('d-none')) {
            startBtn.click();
        } else if (!stopBtn.classList.contains('d-none')) {
            stopBtn.click();
        }
    }
});

// Add tooltips for better UX
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});