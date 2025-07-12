import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# LangChain components para RAG
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma # Usa Chroma de langchain_community

# LangChain components para Agentes y Herramientas
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_community.utilities import SerpAPIWrapper # Para búsqueda web con SerpAPI

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

print("Cargando documentos PDF desde la carpeta 'data'...")
try:
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()
    if not documents:
        print("Advertencia: No se encontraron documentos PDF en la carpeta 'data'.")
except Exception as e:
    print(f"Error al cargar documentos: {e}")
    exit()

print("Dividiendo documentos en fragmentos...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)
print(f"Documentos divididos en {len(chunks)} fragmentos.")

print("Creando embeddings y almacenando en la base de datos vectorial (ChromaDB)...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

persist_directory = "./chroma_db"
if os.path.exists(persist_directory) and os.listdir(persist_directory):
    print("Cargando base de datos vectorial existente...")
    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
else:
    print("Base de datos vectorial no encontrada o vacía, creándola...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vector_db.persist()

print("Base de datos vectorial lista.")

print("Configurando el modelo de lenguaje (LLM)...")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1) # Ajuste la temperatura ligeramente

print("Configurando herramientas para el agente...")

retriever_tool = Tool(
    name="document_search",
    # Descripción reforzada
    description="Útil y ABSOLUTAMENTE PRIORITARIA para buscar información MUY ESPECÍFICA contenida SÓLO en los documentos jurídicos y legales cargados. Úsala SIEMPRE que la pregunta parezca directamente relacionada con el contenido de los PDFs (trámites, leyes internas, reglamentos). Responde la pregunta DIRECTAMENTE con la información CONFIABLE encontrada en los documentos. Si la pregunta no es específica de los documentos, no la uses.",
    func=vector_db.as_retriever().invoke,
)

search = SerpAPIWrapper()
web_search_tool = Tool(
    name="web_search",
    # Descripción clara sobre cuándo usarla
    description="Útil para buscar información GENERAL, noticias ACTUALES, datos que NO se encuentren en los documentos jurídicos cargados. Usa esta herramienta SÓLO cuando la herramienta 'document_search' no sea aplicable o no haya proporcionado una respuesta satisfactoria.",
    func=search.run
)

tools = [retriever_tool, web_search_tool]

print("Creando el agente de IA...")

prompt_template = PromptTemplate.from_template(
    """Eres un asistente jurídico experto, útil y preciso. Tu prioridad es SIEMPRE encontrar la información en los documentos jurídicos internos antes de recurrir a fuentes externas.

Aquí están las herramientas disponibles:
{tools}

Sigue rigurosamente este proceso de pensamiento para decidir qué herramienta usar:

Question: La pregunta del usuario.
Thought: Primero, evalúa si la pregunta del usuario puede ser respondida directamente por el contenido de los documentos jurídicos. Si es así, DEBES usar 'document_search'. Si la pregunta es demasiado general, requiere información actual, o si 'document_search' es poco probable que contenga la respuesta, entonces considera 'web_search'.
Action: La acción a realizar, debe ser una de [{tool_names}].
Action Input: La entrada para la acción (por ejemplo, la pregunta de búsqueda).
Observation: El resultado de la acción.
... (este ciclo Thought/Action/Action Input/Observation se puede repetir si es necesario para refinar la búsqueda)
Thought: Una vez que hayas obtenido la información relevante (ya sea de los documentos o de la web), formula tu respuesta final.
Final Answer: Tu respuesta final a la pregunta original del usuario, basada en la información obtenida. Si no encontraste información relevante en ninguna fuente, indícalo claramente.

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
)

agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

print("Asistente Jurídico listo y configurado con herramientas de búsqueda.")

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
    try:
        result = agent_executor.invoke({"input": user_message})
        response_text = result["output"]
        
        print(f"Respuesta generada por el agente: {response_text}")
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error al procesar la pregunta con el agente: {e}")
        return jsonify({"response": f"Lo siento, ocurrió un error interno al procesar tu pregunta: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)