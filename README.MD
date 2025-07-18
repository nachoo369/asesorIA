# 🚀 Asistente Jurídico IA: Recuperación Inteligente de Información Legal

## ✨ Descripción del Proyecto
Este proyecto implementa un **asistente jurídico impulsado por Inteligencia Artificial** diseñado para simplificar el acceso a la información legal en Chile. Utiliza **Grandes Modelos de Lenguaje (LLMs)**, **Generación Aumentada por Recuperación (RAG)** y agentes inteligentes para proporcionar respuestas precisas, contextualizadas y citadas con fuentes, basándose en un corpus de documentos PDF locales y búsquedas web en tiempo real.

El objetivo es empoderar a los usuarios con conocimientos legales rápidos y fiables, reduciendo la complejidad y el tiempo que a menudo implica la búsqueda de información jurídica específica.

---

## 🌟 Características Principales
- **Agente Inteligente:** Emplea un agente avanzado de **LangChain** con estrategia **ReAct** (Reasoning and Acting).
- **Generación Aumentada por Recuperación (RAG):**
  - **Búsqueda de Documentos:** Base vectorial **ChromaDB** con embeddings de PDFs legales.
  - **Búsqueda Web:** Integración con **SerpApi** (Google Search).
- **Comprensión Contextual:** Memoria conversacional con `ConversationBufferWindowMemory`.
- **Citación de Fuentes:** Proporciona referencias claras para aumentar la fiabilidad.
- **Interfaz Web Amigable:** Archivo `index.html` con chat interactivo.
- **Manejo Robusto de Errores:** Controla errores de API y notifica al usuario.
- **Arquitectura Escalable:** Modular, orientada a despliegues en la nube.

---

## 🛠️ Tecnologías Utilizadas
- **Python** (lenguaje principal)
- **Flask** (API backend)
- **LangChain** (orquestación de agentes y RAG)
- **Google Gemini 1.5 Flash** (LLM principal)
- **ChromaDB** (base de datos vectorial)
- **SerpApi** (Google Search API)
- **HTML/CSS/JavaScript** (interfaz web)
- **.env** (gestión de variables de entorno)

---

## ⚙️ Configuración e Instalación
### 1. Clonar el Repositorio
```bash
git clone https://github.com/nachoo369/asesorIA.git
cd asesorIA
```

### 2. Crear un Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

Ejemplo de `requirements.txt`:
```
Flask
langchain
langchain-google-genai
python-dotenv
chromadb
serpapi
unstructured[pdf]
pypdf
```

### 4. Configurar Variables de Entorno
Crear archivo **.env** en la raíz:
```env
GOOGLE_API_KEY="TU_CLAVE_API_DE_GEMINI"
SERPAPI_API_KEY="TU_CLAVE_API_DE_SERPAPI"
```

- **Google API Key:** desde Google AI Studio / Google Cloud.
- **SerpApi API Key:** desde SerpApi.

---

## 📂 Preparar Documentos y Base Vectorial
Coloca los PDFs en `data/` y asegúrate que `app.py` los cargue en **ChromaDB**.  
Ejemplo:
```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

loader = PyPDFLoader("data/mi_documento_legal.pdf")
documents = loader.load_and_split()

chroma_db = Chroma.from_documents(documents, embedding_model, persist_directory="./chroma_db")
```

---

## ▶️ Ejecutar la Aplicación Flask
```bash
flask run
```
Accede a: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🌐 Interfaz Web
El archivo `templates/index.html` incluye:
- Chat simple
- Lógica JavaScript para enviar consultas a `/chat`
- Historial en `localStorage`

---

## 🧪 Ejemplos de Uso
- **Saludo:** `Hola, ¿cómo estás?`
- **Consulta legal:** `¿Qué necesito para tramitar la posesión efectiva en Chile?`
- **Cambio de nombre:** `¿Cuál es el proceso para cambiar el nombre de un menor de edad?`
- **Consulta ley:** `¿Dónde puedo encontrar información sobre la Ley de Protección al Consumidor en Chile?`
- **Definición:** `¿Qué es la servidumbre legal?`

---

## ⏭️ Próximos Pasos y Mejoras Futuras
- **Despliegue en la Nube:** Firebase, Google Cloud Run, Render.
- **Memoria a Largo Plazo:** Firestore, Redis.
- **Interfaz Avanzada:** UI/UX moderna, carga de archivos.
- **Monitoreo:** Integración de herramientas para métricas y logs.
- **Ampliación del Corpus:** Más leyes, jurisprudencia y normativa.

---
