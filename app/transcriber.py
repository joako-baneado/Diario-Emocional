# app/transcriber.py
import speech_recognition as sr
import os
from datetime import datetime


class AudioTranscriber:
    def __init__(self, audio_folder="audio_inputs", text_folder="text_outputs"):
        self.audio_folder = audio_folder
        self.text_folder = text_folder
        os.makedirs(self.text_folder, exist_ok=True)
        
        self.recognizer = sr.Recognizer()
    
    def transcribe_audio_file(self, audio_file_path, language="es-PE"):
        """Transcribe audio file to text"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Error with Google Speech Recognition: {e}")
            return None
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    def transcribe_audio_data(self, audio_data, language="es-PE"):
        """Transcribe audio data directly to text"""
        try:
            text = self.recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Error with Google Speech Recognition: {e}")
            return None
        except Exception as e:
            print(f"Error transcribing audio data: {e}")
            return None
    
    def transcribe_latest_audio(self, language="es-PE"):
        """Transcribe the most recent audio file"""
        try:
            audio_files = [f for f in os.listdir(self.audio_folder) if f.endswith(".wav")]
            if not audio_files:
                return None
            
            latest_file = max(audio_files, key=lambda f: os.path.getctime(os.path.join(self.audio_folder, f)))
            audio_path = os.path.join(self.audio_folder, latest_file)
            
            return self.transcribe_audio_file(audio_path, language)
        except Exception as e:
            print(f"Error transcribing latest audio: {e}")
            return None
    
    def save_transcription(self, text, audio_filename=None):
        """Save transcription to text file"""
        try:
            timestamp = datetime.now()
            date_time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            if audio_filename:
                txt_name = os.path.splitext(audio_filename)[0] + ".txt"
            else:
                txt_name = timestamp.strftime("transcripcion_%Y-%m-%d_%H-%M-%S.txt")
            
            txt_path = os.path.join(self.text_folder, txt_name)
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"Fecha y hora de transcripción: {date_time_str}\n")
                f.write("Texto reconocido:\n")
                f.write(text)
            
            return txt_path
        except Exception as e:
            print(f"Error saving transcription: {e}")
            return None


# Legacy compatibility - if run as script
if __name__ == "__main__":
    transcriber = AudioTranscriber()
    text = transcriber.transcribe_latest_audio()
    if text:
        print("Texto reconocido:", text)
        txt_path = transcriber.save_transcription(text)
        if txt_path:
            print(f"Texto guardado en: {txt_path}")
    else:
        print("No se pudo transcribir el audio")
