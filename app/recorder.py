# app/recorder.py
import speech_recognition as sr
import os
from datetime import datetime
import threading
import queue


class AudioRecorder:
    def __init__(self, audio_folder="audio_inputs"):
        self.audio_folder = audio_folder
        os.makedirs(self.audio_folder, exist_ok=True)
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.recording_thread = None
        
        # Calibrate microphone
        self._calibrate_microphone()
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
        except Exception as e:
            print(f"Error calibrating microphone: {e}")
    
    def start_recording(self):
        """Start recording audio in a separate thread"""
        if self.is_recording:
            return False
        
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        return True
    
    def stop_recording(self):
        """Stop recording and return the audio file path"""
        if not self.is_recording:
            return None
        
        self.is_recording = False
        
        # Wait for recording thread to finish
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2)
        
        # Get audio from queue
        try:
            audio_data = self.audio_queue.get_nowait()
            return self._save_audio(audio_data)
        except queue.Empty:
            return None
    
    def _record_audio(self):
        """Record audio until stopped"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=None)
                if self.is_recording:
                    self.audio_queue.put(audio)
        except Exception as e:
            print(f"Error recording audio: {e}")
            self.is_recording = False
    
    def _save_audio(self, audio_data):
        """Save audio data to file"""
        try:
            timestamp = datetime.now()
            filename = timestamp.strftime("grabacion_%Y-%m-%d_%H-%M-%S")
            filepath = os.path.join(self.audio_folder, f"{filename}.wav")
            
            with open(filepath, "wb") as f:
                f.write(audio_data.get_wav_data())
            
            return filepath
        except Exception as e:
            print(f"Error saving audio: {e}")
            return None
    
    def record_fixed_duration(self, duration_seconds=5):
        """Record for a fixed duration (legacy method)"""
        try:
            with self.microphone as source:
                audio = self.recognizer.record(source, duration=duration_seconds)
            return self._save_audio(audio)
        except Exception as e:
            print(f"Error recording fixed duration: {e}")
            return None


# Legacy compatibility - if run as script
if __name__ == "__main__":
    recorder = AudioRecorder()
    print("Grabando por 5 segundos...")
    filepath = recorder.record_fixed_duration(5)
    if filepath:
        print(f"Audio guardado como: {filepath}")
    else:
        print("Error al grabar audio")
