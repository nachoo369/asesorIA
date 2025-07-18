import os
import time # Importar el módulo time para medir el rendimiento
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# LangChain components para RAG
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma

# LangChain components para Agentes y Herramientas
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_community.utilities import SerpAPIWrapper # Para búsqueda web con SerpAPI
from langchain.memory import ConversationBufferWindowMemory # ¡IMPORTADO PARA LA MEMORIA!


app = Flask(__name__)

# --- Configuración inicial de LangChain ---
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not GOOGLE_API_KEY:
    print("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
    print("Por favor, crea un archivo .env y añade la línea: GOOGLE_API_KEY='tu_api_key_aqui'")
    exit()
if not SERPAPI_API_KEY:
    print("Error: La variable de entorno SERPAPI_API_KEY no está configurada.")
    print("Por favor, crea un archivo .env y añade la línea: SERPAPI_API_KEY='tu_api_key_de_serpapi_aqui'")
    print("Puedes obtener una API Key gratuita en https://serpapi.com/")
    exit()

os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY

# --- INICIO DE LA SECCIÓN DE CARGA Y PROCESAMIENTO CON METADATOS ---

print("Cargando documentos PDF desde la carpeta 'data'...")
documents = []
try:
    loader = PyPDFDirectoryLoader("data")
    loaded_documents = loader.load()
    if not loaded_documents:
        print("Advertencia: No se encontraron documentos PDF en la carpeta 'data'.")
    else:
        # ASIGNAR METADATOS PERSONALIZADOS A CADA DOCUMENTO
        # Cada documento en `loaded_documents` ya tiene un `metadata` con 'source' (el nombre del archivo).
        # Vamos a enriquecerlo.
        for doc in loaded_documents:
            # Obtener el nombre del archivo del path de origen
            file_name = os.path.basename(doc.metadata.get('source', 'unknown_source.pdf'))
            
            # --- LÓGICA MEJORADA PARA ASIGNAR METADATOS ---
            # Puedes usar una lógica para asignar metadatos basados en el nombre del archivo.
            # Idealmente, para mayor precisión, tendrías un mapeo más robusto (ej. desde un JSON)
            
            # Metadatos por defecto
            doc.metadata["nombre_documento"] = file_name.replace(".pdf", "").replace("_", " ").title()
            doc.metadata["tipo_documento"] = "Documento Jurídico"
            doc.metadata["fuente_url"] = "N/A (Cargado localmente)"
            doc.metadata["fecha_actualizacion"] = "Fecha Desconocida" # Mejor un placeholder que una fecha incorrecta
            
            # Ejemplos de mapeo más específico basado en el nombre del archivo
            if "ley_20898" in file_name.lower():
                doc.metadata["nombre_documento"] = "Ley N° 20.898 (Regularización)"
                doc.metadata["tipo_documento"] = "Ley"
                doc.metadata["fuente_url"] = "https://www.bcn.cl/leychile/navegar?idNorma=1086968"
                doc.metadata["fecha_actualizacion"] = "2021-03-01" # ¡Actualiza con la fecha real!
            elif "oguc" in file_name.lower():
                doc.metadata["nombre_documento"] = "Ordenanza General de Urbanismo y Construcciones (OGUC)"
                doc.metadata["tipo_documento"] = "Ordenanza"
                doc.metadata["fuente_url"] = "https://www.minvu.gob.cl/ordenanza-general-de-urbanismo-y-construcciones/"
                doc.metadata["fecha_actualizacion"] = "2024-02-15" # ¡Actualiza con la fecha real!
            elif "dfl_458" in file_name.lower():
                doc.metadata["nombre_documento"] = "DFL N° 458 (Ley General de Urbanismo y Construcciones)"
                doc.metadata["tipo_documento"] = "DFL"
                doc.metadata["fuente_url"] = "https://www.bcn.cl/leychile/navegar?idNorma=20743"
                doc.metadata["fecha_actualizacion"] = "2023-08-01" # ¡Actualiza con la fecha real!
            # Agrega más condiciones 'elif' para cada uno de tus PDFs clave

            # Asegúrate de que el 'source' original del loader también se mantenga
            doc.metadata['original_source'] = doc.metadata.get('source') 
            
            documents.append(doc) # Añade el documento modificado a la lista
            print(f"Documento '{file_name}' cargado con metadatos: {doc.metadata}")

except Exception as e:
    print(f"Error al cargar documentos: {e}")
    exit()

print(f"Total de documentos cargados (y potencialmente enriquecidos): {len(documents)}")

print("Dividiendo documentos en fragmentos...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
# Ahora `chunks` contendrá los metadatos que acabamos de asignar a los `documents`
chunks = text_splitter.split_documents(documents) 
print(f"Documentos divididos en {len(chunks)} fragmentos.")

print("Creando embeddings y almacenando en la base de datos vectorial (ChromaDB)...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

persist_directory = "./chroma_db"

# Lógica para cargar o crear la base de datos vectorial
# Si añades nuevos documentos o modificas los existentes,
# generalmente querrás recrear la base de datos para que los cambios se reflejen.
# Para desarrollo, borrar la carpeta 'chroma_db' antes de ejecutar es una opción simple.
if os.path.exists(persist_directory) and os.path.isdir(persist_directory) and len(os.listdir(persist_directory)) > 0:
    print("Cargando base de datos vectorial existente...")
    # Considera una estrategia de "upsert" si necesitas añadir documentos incrementalmente
    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    # Si quieres forzar la recreación si hay cambios en los documentos fuente,
    # podrías añadir aquí una lógica para verificar si el número de chunks o los hashes han cambiado.
else:
    print("Base de datos vectorial no encontrada o vacía, creándola...")
    vector_db = Chroma.from_documents(
        documents=chunks, # Aquí los chunks ya tienen los metadatos
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vector_db.persist() # Asegúrate de persistir los cambios

print("Base de datos vectorial lista.")

# --- FIN DE LA SECCIÓN DE CARGA Y PROCESAMIENTO CON METADATOS ---

print("Configurando el modelo de lenguaje (LLM)...")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)

# --- CONFIGURACIÓN DE MEMORIA PARA EL AGENTE ---
print("Configurando la memoria para el agente...")
# 'k' define cuántas interacciones anteriores (pares pregunta/respuesta) el agente recordará
# Puedes ajustar 'k' según tus necesidades. 3-5 suele ser un buen inicio para mantener el contexto.
memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=5)
# --- FIN CONFIGURACIÓN DE MEMORIA ---


print("Configurando herramientas para el agente...")

retriever_tool = Tool(
    name="document_search",
    # Descripción reforzada y explícita sobre la citación de metadatos
    description="Útil y ABSOLUTAMENTE PRIORITARIA para buscar información MUY ESPECÍFICA contenida SÓLO en los documentos jurídicos y legales cargados sobre regularización de propiedades en Chile. Incluye leyes, decretos, y guías oficiales. **Si usas esta herramienta, DEBES extraer el 'nombre_documento', 'tipo_documento', y 'fecha_actualizacion' (si están disponibles en los metadatos de los resultados) y CITARLOS CLARAMENTE en tu respuesta.** Úsala SIEMPRE que la pregunta parezca directamente relacionada con el contenido de los PDFs (trámites, leyes internas, reglamentos). Responde la pregunta DIRECTAMENTE con la información CONFIABLE encontrada en los documentos. Si la pregunta no es específica de los documentos, no la uses.",
    func=vector_db.as_retriever(search_kwargs={"k": 5}).invoke, # Recupera los 5 chunks más relevantes
)

search = SerpAPIWrapper()
web_search_tool = Tool(
    name="web_search",
    # Descripción clara sobre cuándo usarla
    description="Útil para buscar información GENERAL, noticias ACTUALES, o datos que NO se encuentren en los documentos jurídicos cargados. Usa esta herramienta SÓLO cuando la herramienta 'document_search' no sea aplicable o no haya proporcionado una respuesta satisfactoria. No cita fuentes específicas de esta herramienta, solo menciona que la información es de una búsqueda web.",
    func=search.run
)

tools = [retriever_tool, web_search_tool]

prompt_template = PromptTemplate.from_template(
    """Eres un asistente jurídico experto y preciso especializado en tramites legales de Chile.
    **Tu objetivo principal es asistir al usuario con cualquier trámite legal o pregunta relacionada con la regularización de propiedades en Chile.**
    Tu prioridad es SIEMPRE encontrar la información en los documentos jurídicos internos antes de recurrir a fuentes externas.

Aquí están las herramientas disponibles:
{tools}

Sigue rigurosamente este proceso de pensamiento para decidir qué herramienta usar:

Question: La pregunta del usuario.
Thought: Primero, evalúa si la pregunta del usuario puede ser respondida directamente por el contenido de los documentos jurídicos internos cargados. Si es así, DEBES usar 'document_search'. Si la pregunta es demasiado general, requiere información actual que no estaría en los documentos, o si 'document_search' es poco probable que contenga la respuesta, entonces considera 'web_search'.
Action: La acción a realizar, debe ser una de [{tool_names}].
Action Input: La entrada para la acción (por ejemplo, la pregunta de búsqueda).
Observation: El resultado de la acción.
... (este ciclo Thought/Action/Action Input/Observation se puede repetir si es necesario para refinar la búsqueda)
Thought: Una vez que hayas obtenido la información relevante (ya sea de los documentos o de la web), formula tu respuesta final.
Final Answer: Tu respuesta final a la pregunta original del usuario, basada en la información obtenida.
    **CRÍTICO:**
    1. Si utilizaste la herramienta 'document_search', DEBES CITAR la fuente de la información utilizando los metadatos 'nombre_documento', 'tipo_documento', y 'fecha_actualizacion' si están disponibles. Si un chunk tiene 'original_source' (la ruta del archivo), puedes mencionarlo para dar más contexto.
    2. Ejemplo de citación: "(Fuente: Ley General de Urbanismo y Construcciones, DFL N° 458, actualizada al 2023-08-01)" o "(Fuente: Guía MINVU de Regularización, Sección 3.1, Doc: guia_minvu.pdf)".
    3. Si usaste 'web_search', no cites una fuente específica, solo puedes mencionar que la información se obtuvo de una "búsqueda en línea".
    4. Si no encontraste información relevante en NINGUNA fuente, indícalo claramente diciendo algo como "Lo siento, no tengo información precisa sobre eso en este momento. Te recomiendo consultar las fuentes oficiales o a un profesional del área.". **No inventes información bajo ninguna circunstancia.**

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
)
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    memory=memory # ¡AGREGADO: PASANDO LA MEMORIA AL AGENT_EXECUTOR!
)

print("Asistente Jurídico listo y configurado con herramientas de búsqueda y memoria.")

@app.route('/Asistenteia')
def index():
    return render_template('index.html')
@app.route('/')
def inicio():
    return render_template('inicio.html')
@app.route('/reg')
def guia():
    return render_template('reg.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"response": "Por favor, introduce una pregunta válida."}), 400

    print(f"Recibida pregunta del usuario: {user_message}")
    start_time = time.time() # Iniciar el temporizador para medir el rendimiento
    try:
        # El historial de chat se pasa automáticamente por la memoria configurada en agent_executor
        result = agent_executor.invoke({"input": user_message})
        response_text = result["output"]
        
        end_time = time.time() # Detener el temporizador
        response_time = end_time - start_time
        print(f"Tiempo de respuesta: {response_time:.2f} segundos")
        print(f"Respuesta generada por el agente: {response_text}")
        
        return jsonify({"response": response_text})
    except Exception as e:
        error_message = str(e)
        if "429" in error_message or "quota" in error_message.lower():
            return jsonify({
                "response": "Se ha excedido el límite de uso diario de la API de Gemini. Por favor, intenta nuevamente más tarde o considera usar un plan de mayor capacidad."
            }), 429
        print(f"Error al procesar la pregunta con el agente: {e}")
        return jsonify({
            "response": "Lo siento, ocurrió un error interno al procesar tu pregunta. Por favor, inténtalo de nuevo más tarde o consulta a un profesional."
        }), 500
if __name__ == '__main__':
    # Asegúrate de que la carpeta 'data' contenga tus PDFs y que estos tengan nombres descriptivos.
    # Si modificas los PDFs o añades nuevos, borra la carpeta 'chroma_db' antes de ejecutar
    # para que la base de datos se regenere con los metadatos actualizados.
    app.run(debug=True, port=5000)