"""
Script de prueba de rendimiento - Lazy Loading
---------------------------------------------

Este script demuestra los beneficios del lazy loading en el Diario Emocional.
Compara el tiempo de inicio con y sin lazy loading.

Funcionalidades:
- Mide tiempo de importación de módulos
- Muestra diferencia de rendimiento
- Analiza uso de memoria

Uso:
    python performance_test.py
"""

import time
import sys
import importlib
from memory_profiler import profile

def measure_import_time(module_name, description):
    """
    Mide el tiempo que tarda en importar un módulo.
    """
    start_time = time.time()
    try:
        importlib.import_module(module_name)
        end_time = time.time()
        import_time = (end_time - start_time) * 1000  # En milisegundos
        print(f"✅ {description}: {import_time:.2f}ms")
        return import_time
    except Exception as e:
        print(f"❌ Error importando {module_name}: {e}")
        return 0

def test_traditional_loading():
    """
    Simula la carga tradicional de todas las librerías al inicio.
    """
    print("\n🔴 CARGA TRADICIONAL (todas las librerías al inicio)")
    print("=" * 60)
    
    start_total = time.time()
    
    times = []
    times.append(measure_import_time("customtkinter", "CustomTkinter"))
    times.append(measure_import_time("tkinter", "Tkinter"))
    times.append(measure_import_time("cv2", "OpenCV"))
    times.append(measure_import_time("speech_recognition", "SpeechRecognition"))
    times.append(measure_import_time("transformers", "Transformers (Hugging Face)"))
    times.append(measure_import_time("torch", "PyTorch"))
    times.append(measure_import_time("matplotlib.pyplot", "Matplotlib"))
    times.append(measure_import_time("PIL", "Pillow (PIL)"))
    times.append(measure_import_time("numpy", "NumPy"))
    times.append(measure_import_time("pandas", "Pandas"))
    times.append(measure_import_time("nltk", "NLTK"))
    
    end_total = time.time()
    total_time = (end_total - start_total) * 1000
    
    print(f"\n⏱️ Tiempo total de carga: {total_time:.2f}ms")
    print(f"📊 Tiempo promedio por módulo: {total_time/len(times):.2f}ms")
    
    return total_time

def test_lazy_loading():
    """
    Simula la carga lazy (solo módulos básicos).
    """
    print("\n🟢 CARGA LAZY (solo módulos necesarios)")
    print("=" * 60)
    
    start_total = time.time()
    
    # Solo cargar módulos básicos para el menú
    times = []
    times.append(measure_import_time("customtkinter", "CustomTkinter (básico)"))
    times.append(measure_import_time("tkinter", "Tkinter (básico)"))
    times.append(measure_import_time("datetime", "DateTime"))
    times.append(measure_import_time("threading", "Threading"))
    times.append(measure_import_time("time", "Time"))
    
    end_total = time.time()
    total_time = (end_total - start_total) * 1000
    
    print(f"\n⏱️ Tiempo total de carga: {total_time:.2f}ms")
    print(f"📊 Tiempo promedio por módulo: {total_time/len(times):.2f}ms")
    
    return total_time

def simulate_feature_usage():
    """
    Simula el uso de características que requieren módulos pesados.
    """
    print("\n🔧 SIMULACIÓN DE USO DE CARACTERÍSTICAS")
    print("=" * 60)
    
    print("Usuario abre el menú principal... ✅ (ya cargado)")
    print("Usuario hace clic en 'Ver Historial'...")
    
    start_time = time.time()
    measure_import_time("matplotlib.pyplot", "  └─ Cargando Matplotlib para gráficos")
    end_time = time.time()
    viewer_time = (end_time - start_time) * 1000
    
    print("Usuario hace clic en 'Escribir Diario'...")
    
    start_time = time.time()
    times = []
    times.append(measure_import_time("cv2", "  ├─ Cargando OpenCV para cámara"))
    times.append(measure_import_time("speech_recognition", "  ├─ Cargando SpeechRecognition"))
    times.append(measure_import_time("transformers", "  ├─ Cargando Transformers para IA"))
    times.append(measure_import_time("PIL", "  └─ Cargando PIL para imágenes"))
    end_time = time.time()
    diary_time = (end_time - start_time) * 1000
    
    print(f"\n📈 Tiempo para abrir visor: {viewer_time:.2f}ms")
    print(f"📝 Tiempo para abrir diario: {diary_time:.2f}ms")
    
    return viewer_time, diary_time

def analyze_memory_usage():
    """
    Analiza el uso de memoria con lazy loading.
    """
    print("\n💾 ANÁLISIS DE MEMORIA")
    print("=" * 60)
    
    try:
        import psutil
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"Memoria inicial: {memory_before:.2f} MB")
        
        # Simular carga de módulos pesados
        import transformers
        memory_after_ai = process.memory_info().rss / 1024 / 1024
        print(f"Después de cargar IA: {memory_after_ai:.2f} MB (+{memory_after_ai-memory_before:.2f} MB)")
        
        import cv2
        memory_after_cv = process.memory_info().rss / 1024 / 1024
        print(f"Después de cargar OpenCV: {memory_after_cv:.2f} MB (+{memory_after_cv-memory_after_ai:.2f} MB)")
        
        import matplotlib.pyplot
        memory_after_plt = process.memory_info().rss / 1024 / 1024
        print(f"Después de cargar Matplotlib: {memory_after_plt:.2f} MB (+{memory_after_plt-memory_after_cv:.2f} MB)")
        
        print(f"\n📊 Incremento total de memoria: {memory_after_plt-memory_before:.2f} MB")
        
    except ImportError:
        print("❌ psutil no disponible. Instala con: pip install psutil")

def main():
    """
    Función principal del test de rendimiento.
    """
    print("🚀 PRUEBA DE RENDIMIENTO - LAZY LOADING")
    print("=" * 80)
    print("Este script compara el rendimiento de carga tradicional vs lazy loading")
    print("en el Diario Emocional.\n")
    
    # Test de carga tradicional
    traditional_time = test_traditional_loading()
    
    # Test de carga lazy
    lazy_time = test_lazy_loading()
    
    # Simulación de uso
    viewer_time, diary_time = simulate_feature_usage()
    
    # Análisis de memoria
    analyze_memory_usage()
    
    # Resumen comparativo
    print("\n📊 RESUMEN COMPARATIVO")
    print("=" * 60)
    improvement = ((traditional_time - lazy_time) / traditional_time) * 100
    print(f"🔴 Carga tradicional: {traditional_time:.2f}ms")
    print(f"🟢 Carga lazy (menú): {lazy_time:.2f}ms")
    print(f"⚡ Mejora en tiempo de inicio: {improvement:.1f}%")
    print(f"💡 Tiempo ahorrado: {traditional_time - lazy_time:.2f}ms")
    
    print(f"\n🎯 BENEFICIOS DEL LAZY LOADING:")
    print(f"   • Inicio {improvement:.1f}% más rápido")
    print(f"   • Menor uso inicial de memoria")
    print(f"   • Carga módulos solo cuando se necesitan")
    print(f"   • Mejor experiencia de usuario")
    
    print(f"\n⏰ TIEMPOS DE CARGA POR CARACTERÍSTICA:")
    print(f"   • Menú principal: {lazy_time:.2f}ms")
    print(f"   • Visor de historial: +{viewer_time:.2f}ms")
    print(f"   • Diario con IA: +{diary_time:.2f}ms")

if __name__ == "__main__":
    main()
