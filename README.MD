🚀 Asistente Jurídico IA: Recuperación Inteligente de Información Legal
✨ Descripción del Proyecto
Este proyecto implementa un asistente jurídico impulsado por Inteligencia Artificial diseñado para simplificar el acceso a la información legal en Chile. Utiliza Grandes Modelos de Lenguaje (LLMs), Generación Aumentada por Recuperación (RAG) y agentes inteligentes para proporcionar respuestas precisas, contextualizadas y citadas con fuentes, basándose en un corpus de documentos PDF locales y búsquedas web en tiempo real.

El objetivo es empoderar a los usuarios con conocimientos legales rápidos y fiables, reduciendo la complejidad y el tiempo que a menudo implica la búsqueda de información jurídica específica.

🌟 Características Principales
Agente Inteligente: Emplea un agente avanzado de LangChain con una estrategia ReAct (Reasoning and Acting) para procesar consultas, decidir acciones y generar respuestas.

Generación Aumentada por Recuperación (RAG):

Búsqueda de Documentos: Realiza búsquedas en una base vectorial local ChromaDB que contiene los embeddings de documentos legales en formato PDF cargados previamente.

Búsqueda Web: Se integra con la API de Búsqueda de Google (a través de SerpApi) para obtener información en tiempo real cuando los documentos locales no son suficientes o para consultas más generales.

Comprensión Contextual: Mantiene el contexto de la conversación usando ConversationBufferWindowMemory para asegurar interacciones fluidas y coherentes.

Citación de Fuentes: Proporciona citas claras para la información recuperada de los documentos PDF, aumentando la fiabilidad.

Interfaz Web Amigable: Un index.html sencillo para un chat interactivo.

Manejo Robusto de Errores: Gestiona los errores de API de forma controlada, ofreciendo mensajes informativos al usuario.

Arquitectura Escalable: Diseñado con modularidad para futuras expansiones y despliegues en plataformas serverless.

🛠️ Tecnologías Utilizadas
Python: Lenguaje principal de desarrollo.

Flask: Framework web ligero para la API de backend.

LangChain: Framework para construir aplicaciones impulsadas por LLMs y para la orquestación de agentes.

Google Gemini 1.5 Flash: El Modelo de Lenguaje Grande (LLM) central.

ChromaDB: Base de datos vectorial local para almacenar y consultar embeddings de documentos.

SerpApi (Google Search API): Para realizar búsquedas web.

HTML/CSS/JavaScript: Para la interfaz web interactiva y la gestión de sesiones en el lado del cliente (localStorage).

.env para la gestión de variables de entorno.

⚙️ Configuración e Instalación
Sigue estos pasos para poner en marcha tu Asistente Jurídico IA en tu entorno local.

1. Clonar el Repositorio
Bash

git clone https://github.com/nachoo369/asesorIA.git
cd asesorIA
2. Crear un Entorno Virtual
Es altamente recomendable usar un entorno virtual para gestionar las dependencias del proyecto.

Bash

python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
3. Instalar Dependencias
Instala todas las librerías necesarias utilizando pip:

Bash

pip install -r requirements.txt
Asegúrate de que tu archivo requirements.txt contenga lo siguiente (o añade cualquier otra dependencia que uses):

Flask
langchain
langchain-google-genai
python-dotenv
chromadb
serpapi
unstructured[pdf] # Para cargar PDFs
pypdf # Para cargar PDFs
4. Configurar Variables de Entorno
Crea un archivo llamado .env en la raíz de tu proyecto y añade tus claves API. ¡No compartas este archivo en repositorios públicos!

Fragmento de código

GOOGLE_API_KEY="TU_CLAVE_API_DE_GEMINI"
SERPAPI_API_KEY="TU_CLAVE_API_DE_SERPAPI"
Google API Key (Gemini): Obtenla desde Google AI Studio o Google Cloud Console.

SerpApi API Key: Regístrate en SerpApi para obtener una.

5. Preparar Documentos y Base de Datos Vectorial
Coloca tus archivos PDF legales en la carpeta data/ (crea esta carpeta si no existe).

Asegúrate de que tu app.py tiene la lógica para cargar estos PDFs y crear/actualizar la base de datos ChromaDB. Si tu chroma_db no se crea automáticamente al iniciar app.py, necesitarás un script para generarla.

Un ejemplo de cómo se generaría chroma_db (esto es solo un ejemplo, tu código ya lo hace):

Python

# Este código debería estar en app.py o en un script de carga
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
pdf_path = "data/mi_documento_legal.pdf" # Tu PDF
loader = PyPDFLoader(pdf_path)
documents = loader.load_and_split()
# Esto creará o cargará la base de datos ChromaDB
chroma_db = Chroma.from_documents(documents, embedding_model, persist_directory="./chroma_db")
6. Ejecutar la Aplicación Flask
Desde la raíz de tu proyecto, ejecuta la aplicación Flask:

Bash

flask run
Por defecto, la aplicación se ejecutará en http://127.0.0.1:5000/.

🌐 Interfaz Web de Prueba (index.html)
El proyecto incluye un archivo index.html en la carpeta templates/ que sirve como una interfaz de usuario básica para interactuar con el asistente.

¿Cómo funciona?
Cuando ejecutas flask run, Flask servirá este index.html por defecto al acceder a la URL base (http://127.0.0.1:5000/).

El index.html contiene un formulario de chat simple y lógica JavaScript que:

Envía las preguntas del usuario al endpoint /chat de tu API Flask.

Muestra las respuestas del asistente en la interfaz.

Gestiona el historial de la conversación en el localStorage de tu navegador, permitiendo que la conversación continúe incluso si recargas la página.

Uso
Simplemente abre tu navegador y navega a http://127.0.0.1:5000/. Podrás escribir tus preguntas en el campo de texto y ver las respuestas del Asistente Jurídico IA en tiempo real.

🧪 Pruebas y Uso (Ejemplos de Consulta)
Una vez que la aplicación esté corriendo, puedes interactuar con ella a través de la interfaz web o enviando solicitudes POST directamente a /chat.

Ejemplos de preguntas que puedes hacer al asistente:

"Hola, ¿cómo estás?" (Para probar la respuesta de saludo)

"¿Qué necesito para tramitar la posesión efectiva en Chile?" (Consulta sobre documentos internos)

"¿Cuál es el proceso para cambiar el nombre de un menor de edad?" (Consulta que podría usar documentos y/o búsqueda web)

"¿Dónde puedo encontrar información sobre la Ley de Protección al Consumidor en Chile?" (Consulta específica de ley)

"¿Qué es la servidumbre legal?" (Consulta que mezcla definición y contexto legal)

"¿Cuáles son los requisitos para contraer matrimonio civil en Chile?" (Otra consulta legal específica)

⏭️ Próximos Pasos y Mejoras Futuras
Despliegue en la Nube: Migrar la aplicación a servicios serverless como Firebase Functions, Google Cloud Run o Render para mayor escalabilidad y disponibilidad.

Memoria a Largo Plazo: Implementar una solución de base de datos para la memoria de conversación persistente (ej., Firestore, Redis) que no dependa solo del localStorage del cliente, permitiendo sesiones multi-dispositivo y perfiles de usuario.

Interfaz de Usuario Avanzada: Mejorar la UI/UX del chat con más funcionalidades (ej., carga de archivos directa, visualización de fuentes interactivas).

Monitoreo y Observabilidad: Integrar herramientas de monitoreo para rastrear el rendimiento, errores y uso de recursos de la API.

Ampliación del Corpus: Añadir más documentos legales, jurisprudencia y normativa de diferentes áreas del derecho.