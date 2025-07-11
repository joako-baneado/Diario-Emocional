"""
Configuración Optimizada del Diario Emocional
--------------------------------------------

Este script configura el proyecto con optimizaciones de rendimiento
y lazy loading habilitado.

Funcionalidades:
- Instalación selectiva de dependencias
- Configuración de lazy loading
- Optimización de memoria
- Tests de rendimiento

Uso:
    python optimized_setup.py
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def print_header(title):
    """
    Imprime un encabezado formateado.
    """
    print("\n" + "=" * 60)
    print(f"🔧 {title}")
    print("=" * 60)

def print_step(step, description):
    """
    Imprime un paso del proceso.
    """
    print(f"\n{step} {description}...")

def run_command_with_timing(command, description):
    """
    Ejecuta un comando midiendo el tiempo.
    """
    print(f"\n⏱️  {description}...")
    start_time = time.time()
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"✅ Completado en {elapsed:.2f}s")
        return True, elapsed
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"❌ Error después de {elapsed:.2f}s: {e.stderr}")
        return False, elapsed

def install_core_dependencies():
    """
    Instala solo las dependencias principales necesarias para el menú.
    """
    print_header("INSTALACIÓN CORE (Lazy Loading)")
    
    core_packages = [
        "customtkinter==5.2.0",
        "tk==0.1.0", 
        "python-dotenv==1.0.0"
    ]
    
    total_time = 0
    
    for package in core_packages:
        success, elapsed = run_command_with_timing(
            f"{sys.executable} -m pip install {package}",
            f"Instalando {package.split('==')[0]}"
        )
        total_time += elapsed
        if not success:
            return False
    
    print(f"\n📊 Tiempo total instalación core: {total_time:.2f}s")
    return True

def install_optional_dependencies():
    """
    Instala dependencias opcionales por categoría.
    """
    print_header("INSTALACIÓN OPCIONAL (Por Categoría)")
    
    categories = {
        "IA y ML": [
            "transformers==4.34.1",
            "torch==2.1.0",
            "nltk==3.8.1",
            "scikit-learn==1.3.0"
        ],
        "Audio y Video": [
            "SpeechRecognition==3.10.0",
            "librosa==0.10.1",
            "opencv-python"  # Usar opencv-python en lugar de cv2
        ],
        "Datos y Visualización": [
            "pandas==2.1.1",
            "matplotlib==3.7.2",
            "numpy==1.24.3"
        ],
        "Utilidades": [
            "datasets==2.14.5",
            "joblib==1.3.2",
            "Pillow"  # Para PIL
        ]
    }
    
    user_choice = input("\n¿Instalar todas las categorías? (s/n): ").lower()
    
    if user_choice == 's':
        # Instalar todas
        for category, packages in categories.items():
            print(f"\n📦 Instalando categoría: {category}")
            for package in packages:
                run_command_with_timing(
                    f"{sys.executable} -m pip install {package}",
                    f"  └─ {package.split('==')[0]}"
                )
    else:
        # Instalación selectiva
        print("\n🎯 Instalación Selectiva:")
        for i, (category, packages) in enumerate(categories.items(), 1):
            print(f"{i}. {category}: {', '.join([p.split('==')[0] for p in packages])}")
        
        choices = input("Selecciona categorías (ej: 1,3): ").split(',')
        
        for choice in choices:
            try:
                idx = int(choice.strip()) - 1
                category_name = list(categories.keys())[idx]
                packages = list(categories.values())[idx]
                
                print(f"\n📦 Instalando: {category_name}")
                for package in packages:
                    run_command_with_timing(
                        f"{sys.executable} -m pip install {package}",
                        f"  └─ {package.split('==')[0]}"
                    )
            except (ValueError, IndexError):
                print(f"❌ Opción inválida: {choice}")

def create_lazy_loading_config():
    """
    Crea un archivo de configuración para lazy loading.
    """
    print_header("CONFIGURACIÓN DE LAZY LOADING")
    
    config_content = '''"""
Configuración de Lazy Loading - Diario Emocional
-----------------------------------------------

Este archivo controla qué módulos se cargan automáticamente
y cuáles se cargan bajo demanda.
"""

# Configuración de carga de módulos
LAZY_LOADING_CONFIG = {
    # Módulos que se cargan siempre (aplicación básica)
    "always_load": [
        "customtkinter",
        "tkinter", 
        "datetime",
        "threading",
        "time",
        "os",
        "sys"
    ],
    
    # Módulos que se cargan solo para el diario principal
    "diary_modules": [
        "cv2",
        "speech_recognition", 
        "PIL",
        "numpy"
    ],
    
    # Módulos que se cargan solo para IA/ML
    "ai_modules": [
        "transformers",
        "torch",
        "nltk",
        "scikit-learn"
    ],
    
    # Módulos que se cargan solo para estadísticas
    "stats_modules": [
        "matplotlib",
        "pandas"
    ],
    
    # Configuraciones de rendimiento
    "performance": {
        "preload_ai_models": False,  # Si cargar modelos de IA al inicio
        "cache_models": True,        # Si mantener modelos en caché
        "lazy_camera": True,         # Si cargar cámara solo cuando se use
        "defer_heavy_imports": True  # Si diferir importaciones pesadas
    }
}

def should_preload_module(module_name):
    """
    Determina si un módulo debe cargarse automáticamente.
    """
    return module_name in LAZY_LOADING_CONFIG["always_load"]

def get_module_category(module_name):
    """
    Obtiene la categoría de un módulo.
    """
    for category, modules in LAZY_LOADING_CONFIG.items():
        if isinstance(modules, list) and module_name in modules:
            return category
    return "unknown"
'''
    
    config_path = "app/lazy_config.py"
    
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        print(f"✅ Configuración creada: {config_path}")
        return True
    except Exception as e:
        print(f"❌ Error creando configuración: {e}")
        return False

def run_performance_test():
    """
    Ejecuta una prueba de rendimiento básica.
    """
    print_header("PRUEBA DE RENDIMIENTO")
    
    print("🧪 Ejecutando test de tiempo de inicio...")
    
    # Test del menú principal
    start_time = time.time()
    try:
        # Simular importación del menú
        import tkinter
        import customtkinter
        end_time = time.time()
        menu_time = (end_time - start_time) * 1000
        print(f"✅ Menú principal: {menu_time:.2f}ms")
    except Exception as e:
        print(f"❌ Error en test del menú: {e}")
        return False
    
    # Test opcional de módulos pesados
    test_heavy = input("\n¿Probar carga de módulos pesados? (s/n): ").lower()
    
    if test_heavy == 's':
        heavy_modules = {
            "Transformers (IA)": "transformers",
            "OpenCV (Video)": "cv2", 
            "Matplotlib (Gráficos)": "matplotlib"
        }
        
        for name, module in heavy_modules.items():
            start_time = time.time()
            try:
                __import__(module)
                end_time = time.time()
                load_time = (end_time - start_time) * 1000
                print(f"✅ {name}: {load_time:.2f}ms")
            except ImportError:
                print(f"⚠️  {name}: No instalado")
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
    
    return True

def create_launch_scripts():
    """
    Crea scripts de lanzamiento optimizados.
    """
    print_header("SCRIPTS DE LANZAMIENTO")
    
    # Script rápido (solo menú)
    quick_script = '''@echo off
echo 🚀 Iniciando Diario Emocional (Modo Rápido)
echo Solo cargando módulos básicos para el menú...
python -m app
pause
'''
    
    # Script completo (todas las características)
    full_script = '''@echo off
echo 🔥 Iniciando Diario Emocional (Modo Completo)
echo Precargando todos los módulos...
set PRELOAD_ALL_MODULES=1
python -m app
pause
'''
    
    scripts = {
        "quick_start.bat": quick_script,
        "full_start.bat": full_script
    }
    
    for filename, content in scripts.items():
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Script creado: {filename}")
        except Exception as e:
            print(f"❌ Error creando {filename}: {e}")

def main():
    """
    Función principal de configuración optimizada.
    """
    print("🚀 CONFIGURACIÓN OPTIMIZADA DEL DIARIO EMOCIONAL")
    print("=" * 80)
    print("Esta configuración implementa lazy loading para mejorar el rendimiento.")
    print("Los módulos se cargarán solo cuando se necesiten.")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or python_version.minor < 8:
        print("❌ Error: Se requiere Python 3.8 o superior")
        return
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    steps = [
        ("Instalar dependencias core", install_core_dependencies),
        ("Instalar dependencias opcionales", install_optional_dependencies),
        ("Crear configuración lazy loading", create_lazy_loading_config),
        ("Ejecutar prueba de rendimiento", run_performance_test),
        ("Crear scripts de lanzamiento", create_launch_scripts)
    ]
    
    for step_name, step_function in steps:
        try:
            success = step_function()
            if not success:
                print(f"⚠️  Falló: {step_name}")
                continue_anyway = input("¿Continuar de todos modos? (s/n): ").lower()
                if continue_anyway != 's':
                    break
        except KeyboardInterrupt:
            print("\n❌ Instalación cancelada por el usuario")
            return
        except Exception as e:
            print(f"❌ Error inesperado en {step_name}: {e}")
    
    print_header("CONFIGURACIÓN COMPLETADA")
    print("🎉 ¡Diario Emocional configurado con optimizaciones!")
    print("\n📋 Resumen de optimizaciones:")
    print("   ✅ Lazy loading habilitado")
    print("   ✅ Carga selectiva de módulos")
    print("   ✅ Configuración personalizable")
    print("   ✅ Scripts de lanzamiento optimizados")
    
    print("\n🚀 Para iniciar:")
    print("   • Modo rápido: python -m app")
    print("   • Desde script: quick_start.bat")
    print("   • Modo completo: full_start.bat")

if __name__ == "__main__":
    main()
