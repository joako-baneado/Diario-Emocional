# Diario Emocional 📖

Una aplicación completa para registrar, analizar y visualizar tu estado emocional a través de texto y voz.

> **🚀 Optimizado con Lazy Loading**: Inicio ultrarrápido (~65ms) con carga inteligente de módulos solo cuando se necesitan.

## 🌟 Características

### Registro de Emociones
- **Grabación de voz**: Registra tus pensamientos hablando al micrófono
- **Entrada de texto**: Escribe directamente tus emociones y pensamientos
- **Análisis automático**: Detecta emociones usando IA (DistilRoBERTa)
- **Respuestas empáticas**: Recibe respuestas comprensivas y personalizadas
- **Cámara en vivo**: Visualización opcional de la cámara durante el registro

### Visualización del Historial
- **Explorar entradas pasadas**: Revisa todo tu historial emocional
- **Búsqueda avanzada**: Busca por contenido específico en tus entradas
- **Filtros por emoción**: Filtra entradas por tipo de emoción detectada
- **Estadísticas detalladas**: Gráficos y análisis de tus patrones emocionales
- **Exportación**: Guarda tus entradas en archivos de texto
- **Navegación fluida**: Cambia entre interfaces sin perder datos

### Optimizaciones de Rendimiento
- **⚡ Lazy Loading**: Módulos se cargan solo cuando se necesitan
- **🚀 Inicio ultrarrápido**: De 5.5 segundos a 65 milisegundos
- **💾 Gestión inteligente de memoria**: Uso eficiente de recursos
- **🔄 Navegación optimizada**: Sin recargas innecesarias entre pantallas
- **📊 Carga selectiva**: Instala solo las características que necesitas

## 🚀 Instalación

### Instalación Rápida (Recomendada)
```bash
# 1. Clona el repositorio
git clone https://github.com/joako-baneado/Diario-Emocional.git
cd Diario-Emocional

# 2. Configuración optimizada automática
python optimized_setup.py
```

### Instalación Manual
```bash
# 1. Clona el repositorio
git clone https://github.com/joako-baneado/Diario-Emocional.git
cd Diario-Emocional

# 2. Instala dependencias básicas
pip install customtkinter tk python-dotenv

# 3. Instala dependencias por categoría (opcional)
# IA y ML:
pip install transformers torch nltk scikit-learn

# Audio y Video:
pip install SpeechRecognition librosa opencv-python Pillow

# Datos y Visualización:
pip install pandas matplotlib numpy

# Utilidades:
pip install datasets joblib
```

### Instalación Completa Tradicional
```bash
# Para instalar todo de una vez (inicio más lento)
pip install -r requirements.txt
```

## 💻 Uso

### 🚀 Inicio Rápido
```bash
# Inicio optimizado (recomendado)
python -m app

# O usando script de Windows
quick_start.bat
```

### 🎯 Opciones de Inicio

#### Modo Rápido (Por Defecto)
- **Tiempo de inicio**: ~65ms
- **Memoria inicial**: Mínima
- **Características**: Se cargan bajo demanda
```bash
python -m app
```

#### Modo Completo (Para sistemas rápidos)
- **Tiempo de inicio**: ~5 segundos
- **Memoria inicial**: Completa
- **Características**: Todas precargadas
```bash
# Windows
full_start.bat

# Linux/Mac
PRELOAD_ALL_MODULES=1 python -m app
```

### Menú Principal
Al ejecutar la aplicación, verás un menú con dos opciones:

1. **✍️ Escribir en mi Diario**: Para registrar nuevas emociones
2. **📚 Ver mi Historial**: Para explorar entradas pasadas

### 🎙️ Registro de Emociones
- Haz clic en "🎙️ Grabar voz" para registrar audio
- Escribe en el campo de texto y presiona "✉️ Enviar texto"
- La IA analizará automáticamente tus emociones
- Recibirás respuestas empáticas personalizadas

> **💡 Optimización**: Los módulos de IA se cargan automáticamente la primera vez que los usas.

### 📊 Visualización del Historial
- **Buscar**: Usa la barra de búsqueda para encontrar contenido específico
- **Filtrar**: Selecciona emociones específicas en el dropdown
- **Estadísticas**: Haz clic en "📊 Estadísticas" para ver gráficos detallados
- **Exportar**: Guarda tus entradas filtradas en un archivo de texto

> **💡 Optimización**: Matplotlib se carga solo cuando abres las estadísticas.

### 🧭 Navegación Entre Interfaces
- **Desde cualquier pantalla**: Navega libremente entre el menú, diario y visor
- **Sin pérdida de datos**: Las ventanas se ocultan en lugar de cerrarse
- **Experiencia fluida**: Sin recargas innecesarias

## 🎯 Emociones Detectadas

La aplicación puede identificar las siguientes emociones:
- 😊 **Alegría** (joy)
- 😢 **Tristeza** (sadness)  
- 😠 **Ira** (anger)
- 😰 **Miedo** (fear)
- 😲 **Sorpresa** (surprise)
- 😐 **Neutral** (neutral)
- 🤢 **Disgusto** (disgust)

## 🛠️ Tecnologías Utilizadas

### 🎨 Frontend & UI
- **CustomTkinter**: Interfaz moderna y responsiva
- **Tkinter**: Widgets adicionales y compatibilidad

### 🤖 Inteligencia Artificial
- **Transformers (Hugging Face)**: DistilRoBERTa para detección de emociones
- **PyTorch**: Backend de machine learning
- **NLTK**: Procesamiento de lenguaje natural

### 🎙️ Audio & Video  
- **SpeechRecognition**: Reconocimiento de voz multiidioma
- **OpenCV**: Captura y procesamiento de video en tiempo real
- **Librosa**: Análisis avanzado de audio

### 📊 Datos & Visualización
- **Matplotlib**: Gráficos estadísticos interactivos
- **Pandas**: Análisis y manipulación de datos
- **NumPy**: Computación numérica eficiente

### ⚡ Optimizaciones
- **Lazy Loading**: Carga inteligente de módulos bajo demanda
- **Memory Management**: Gestión eficiente de recursos
- **Threading**: Operaciones no bloqueantes

## 📁 Estructura del Proyecto

```
Diario-Emocional/
├── app/
│   ├── __main__.py              # 🚀 Menú principal optimizado
│   ├── interface.py             # 🎙️ Interfaz principal del diario
│   ├── diary_viewer.py          # 📊 Visor del historial  
│   ├── emotion_text.py          # 🧠 Análisis de texto
│   ├── emotion_audio.py         # 🎵 Análisis de audio
│   ├── empathy.py              # 💝 Generación de respuestas empáticas
│   ├── recorder.py             # 🎤 Grabación de audio
│   └── transcriber.py          # 📝 Transcripción de audio
├── logs/
│   └── diario_emocional_log.txt # 📄 Archivo de registro
├── ml_models/                   # 🤖 Modelos entrenados
├── training_model/              # 🏋️ Scripts de entrenamiento
├── docs/
│   └── OPTIMIZACIONES.md        # 📚 Guía de optimizaciones
├── requirements.txt             # 📦 Dependencias categorizadas
├── optimized_setup.py           # ⚡ Configuración inteligente
├── performance_test.py          # 🧪 Tests de rendimiento
├── quick_start.bat             # 🚀 Inicio rápido (Windows)
├── full_start.bat              # 🔥 Inicio completo (Windows)
└── README.md                   # 📖 Este archivo
```

## 🚀 Ejecución Alternativa

### Scripts de Inicio Rápido

#### Windows
```batch
# Inicio optimizado
quick_start.bat

# Inicio con todas las características
full_start.bat
```

#### Linux/Mac
```bash
# Inicio optimizado
python -m app

# Inicio completo
PRELOAD_ALL_MODULES=1 python -m app
```

### Ejecución Directa por Componente
```bash
# Solo el visor de historial
python view_diary.py

# Solo la interfaz principal (sin menú)
python app/interface.py

# Solo el diario viewer (sin menú)
python app/diary_viewer.py
```

### 🧪 Testing y Análisis
```bash
# Test de rendimiento comparativo
python performance_test.py

# Configuración inteligente con análisis
python optimized_setup.py
```

## ⚡ Rendimiento y Optimizaciones

### � Lazy Loading Implementado
- **Inicio ultrarrápido**: De 5.5s a 0.065s (85% más rápido)
- **Carga inteligente**: Módulos se cargan solo cuando se necesitan
- **Menor uso de memoria**: 70% menos consumo inicial
- **Experiencia fluida**: Sin esperas innecesarias

### �📊 Comparación de Rendimiento

| Componente | Tradicional | Optimizado | Mejora |
|------------|-------------|------------|---------|
| **Inicio del menú** | 5550ms | 65ms | 🚀 85% |
| **Memoria inicial** | ~200MB | ~60MB | 💾 70% |
| **Tiempo hasta UI** | 5.5s | Inmediato | ⚡ 100% |

### 🎯 Carga por Característica
- **Menú principal**: 65ms (instantáneo)
- **Diario con IA**: +2000ms (solo al usar IA)
- **Visor con gráficos**: +400ms (solo al ver estadísticas)
- **Grabación de voz**: +300ms (solo al grabar)

> 📚 **Documentación completa**: Ver `docs/OPTIMIZACIONES.md` para detalles técnicos.

## 📊 Funcionalidades del Visor

### Búsqueda y Filtrado
- **Búsqueda de texto**: Encuentra entradas que contengan palabras específicas
- **Filtros de emoción**: Ve solo las entradas de emociones específicas  
- **Actualización en tiempo real**: Los filtros se aplican automáticamente

### Estadísticas Avanzadas
- **Gráfico de barras**: Distribución de emociones por frecuencia
- **Gráfico circular**: Proporción de cada emoción
- **Estadísticas textuales**: Resumen detallado con porcentajes

### Exportación
- **Formato de texto**: Exporta entradas filtradas a archivos .txt
- **Metadatos incluidos**: Fecha de exportación y total de entradas
- **Formato legible**: Mantiene la estructura original del log

## 🔧 Configuración

### Idioma de reconocimiento de voz
El reconocimiento de voz está configurado para español (es-ES). Puedes cambiarlo en `interface.py`:
```python
text = self.recognizer.recognize_google(audio, language="es-ES")
```

### Ubicación del archivo de log
Los logs se guardan en `./logs/diario_emocional_log.txt`. Puedes cambiar la ubicación en `diary_viewer.py`:
```python
self.log_file_path = "./logs/diario_emocional_log.txt"
```

## 🔧 Resolución de Problemas

### 🐛 Problemas Comunes

#### Error de importación al inicio
```
ImportError: No module named 'transformers'
```
**Solución**: Las dependencias de IA se cargan bajo demanda. Solo instala lo que necesitas:
```bash
# Solo para usar el menú y visor básico
pip install customtkinter tk

# Para análisis de IA
pip install transformers torch nltk
```

#### Inicio lento en primera ejecución
**Causa**: Descarga de modelos de IA la primera vez
**Solución**: Es normal. Las siguientes ejecuciones serán rápidas gracias al cache.

#### Error de cámara
```
cv2.error: Camera not found
```
**Solución**: 
1. Verifica que tengas una cámara conectada
2. Cierra otras aplicaciones que usen la cámara
3. La cámara se carga solo cuando abres el diario principal

#### Problema con micrófono
**Solución**:
1. Verifica permisos de micrófono en tu sistema
2. El módulo de audio se carga solo al hacer clic en "Grabar voz"

### 🛠️ Diagnóstico de Rendimiento
```bash
# Ejecutar test de rendimiento
python performance_test.py

# Ver qué módulos están cargados
python -c "import sys; print(list(sys.modules.keys()))"
```

### 🔄 Reinstalación Limpia
```bash
# 1. Limpiar instalaciones previas
pip uninstall -y -r requirements.txt

# 2. Instalación optimizada
python optimized_setup.py
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ve el archivo [LICENSE](LICENSE) para más detalles.

## 🐛 Reportar Problemas

Si encuentras algún problema o tienes sugerencias, por favor [crea un issue](https://github.com/joako-baneado/Diario-Emocional/issues).

## 🙏 Agradecimientos

- [Hugging Face](https://huggingface.co/) por los modelos de IA preentrenados
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) por la interfaz moderna
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) por el reconocimiento de voz

## 📚 Documentación Adicional

- **[Guía de Optimizaciones](docs/OPTIMIZACIONES.md)**: Detalles técnicos sobre lazy loading
- **[Configuración Avanzada](optimized_setup.py)**: Script de instalación inteligente
- **[Tests de Rendimiento](performance_test.py)**: Análisis comparativo de velocidad

## 📝 Changelog

### v2.0.0 - Optimización Completa (2025-07-11)
- ✅ **Lazy Loading**: Implementado en todos los módulos
- ✅ **Inicio 85% más rápido**: De 5.5s a 65ms
- ✅ **Navegación mejorada**: Entre interfaces sin pérdida de datos
- ✅ **Instalación selectiva**: Por categorías de funcionalidades
- ✅ **Scripts optimizados**: Inicio rápido y completo
- ✅ **Tests de rendimiento**: Análisis automático incluido
- ✅ **Documentación completa**: Guías técnicas detalladas

### v1.0.0 - Versión Inicial
- ✅ Diario emocional con análisis de IA
- ✅ Grabación de voz y entrada de texto
- ✅ Visor de historial con estadísticas
- ✅ Respuestas empáticas personalizadas
- ✅ Interfaz moderna con CustomTkinter

---

⭐ **¡Dale una estrella al proyecto si te resulta útil!** ⭐