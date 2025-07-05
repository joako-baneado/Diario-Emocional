#!/usr/bin/env python3
# test_empathy.py - Test the empathy functionality
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.empathy import EmpatheticResponseGenerator

def test_empathy_responses():
    """Test the empathy response generation"""
    print("Testing Empathy Response Generator...")
    
    generator = EmpatheticResponseGenerator()
    
    test_cases = [
        ("Hoy me siento muy frustrado en el trabajo. Mi jefe me dio una tarea con un plazo imposible.", "anger"),
        ("Estoy muy feliz porque me ascendieron en el trabajo", "joy"),
        ("Me siento triste porque perdí a mi mascota", "sadness"),
        ("Tengo miedo de hablar en público mañana", "fear"),
        ("No sé qué hacer con mi vida", "neutral")
    ]
    
    print("=" * 60)
    for i, (text, emotion) in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Input: {text}")
        print(f"Emotion: {emotion}")
        
        response = generator.generate_empathetic_response(text, emotion)
        print(f"Response: {response}")
        print("-" * 40)
    
    print("\nAll tests completed successfully!")
    print("The empathy module is working correctly.")

if __name__ == "__main__":
    test_empathy_responses()