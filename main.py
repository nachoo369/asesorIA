import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings # Importaciones para Google Gemini
from langchain_text_splitters import RecursiveCharacterTextSplitter # Para dividir documentos
from langchain_community.document_loaders import PyPDFDirectoryLoader # Para cargar PDFs
from langchain_community.vectorstores import Chroma # Para la base de datos vectorial
from langchain.chains import RetrievalQA # Para la cadena de pregunta y respuesta

# Cargar variables de entorno (como GOOGLE_API_KEY)
load_dotenv()

# --- Verificación de la API Key de Google ---
# Asegúrate de que la variable de entorno GOOGLE_API_KEY esté configurada.
# Puedes obtener tu API Key de Google AI Studio en https://aistudio.google.com/app/apikey
if not os.getenv("GOOGLE_API_KEY"):
    print("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
    print("Por favor, crea un archivo .env en la misma carpeta que main.py")
    print("y añade la línea: GOOGLE_API_KEY='tu_api_key_aqui'")
    exit()

# --- 1. Cargar documentos PDF ---
print("Cargando documentos PDF desde la carpeta 'data'...")
try:
    # PyPDFDirectoryLoader cargará todos los PDFs de la carpeta "data"
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()
    if not documents:
        print("Advertencia: No se encontraron documentos PDF en la carpeta 'data'.")
        print("Asegúrate de colocar tus archivos PDF en la carpeta 'data'.")
        # Si no hay documentos, el asistente no tendrá información para responder.
except Exception as e:
    print(f"Error al cargar documentos: {e}")
    print("Asegúrate de que la carpeta 'data' existe y contiene archivos PDF válidos.")
    exit()

# --- 2. Dividir documentos en fragmentos (chunks) ---
print("Dividiendo documentos en fragmentos...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, # Tamaño de cada fragmento
    chunk_overlap=200 # Superposición entre fragmentos para mantener el contexto
)
chunks = text_splitter.split_documents(documents)
print(f"Documentos divididos en {len(chunks)} fragmentos.")

# --- 3. Crear embeddings y almacenar en ChromaDB ---
print("Creando embeddings y almacenando en la base de datos vectorial (ChromaDB)...")
# Inicializar el modelo de embeddings de Google (gratuito para uso básico)
# 'models/embedding-001' es el modelo de embeddings de Gemini
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Crear una base de datos vectorial Chroma a partir de los fragmentos y embeddings.
# Esto creará una carpeta 'chroma_db' en el mismo directorio para almacenar los embeddings localmente.
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db" # Guarda la base de datos en esta carpeta
)
# Persistir la base de datos para que no tenga que ser recreada cada vez que ejecutes el script.
# La advertencia de LangChain indica que Chroma 0.4.x+ lo hace automáticamente.
vector_db.persist()
print("Base de datos vectorial creada y persistida en './chroma_db'.")

# --- 4. Configurar el motor de consulta ---
print("Configurando el motor de consulta...")
# Inicializar el modelo de lenguaje grande (LLM) de Google (Gemini 1.5 Flash, gratuito para uso básico)
# Cambiamos 'gemini-pro' a 'gemini-1.5-flash' para mayor compatibilidad.
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2) 

# Crear un recuperador (retriever) desde la base de datos vectorial.
# Esto buscará los fragmentos más relevantes para una consulta del usuario.
retriever = vector_db.as_retriever()

# Configurar la cadena de RetrievalQA (Retrieval Question Answering).
# Esta cadena orquesta el proceso: toma la consulta, recupera fragmentos relevantes y genera una respuesta con el LLM.
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", # "stuff" significa que junta todos los fragmentos recuperados en un solo prompt para el LLM.
    retriever=retriever,
    return_source_documents=True # Opcional: si es True, la respuesta incluirá los documentos fuente utilizados.
)

print("\n🧑‍⚖️ Asistente Jurídico - Pregúntame sobre trámites legales (escribe 'salir' para terminar)\n")

# --- 5. Bucle de interacción con el usuario ---
while True:
    user_input = input("Tú: ")
    if user_input.lower() in ["salir", "exit"]:
        print("¡Adiós! Gracias por usar el Asistente Jurídico.")
        break
    
    if not user_input.strip(): # Evitar que el usuario envíe preguntas vacías
        print("Asistente: Por favor, introduce una pregunta válida.")
        continue

    print("Asistente: Buscando y generando respuesta...")
    try:
        # Realizar la consulta a la cadena QA
        result = qa_chain.invoke({"query": user_input})
        response_text = result["result"]
        
        print(f"Asistente: {response_text}\n")

        # Opcional: Si quieres ver las fuentes de donde sacó la información
        # if result.get("source_documents"):
        #     print("--- Fuentes utilizadas ---")
        #     for i, doc in enumerate(result["source_documents"]):
        #         print(f"Fuente {i+1}: {doc.metadata.get('source', 'Desconocido')}")
        #         # print(f"Contenido (fragmento): {doc.page_content[:200]}...") # Para ver un pedazo del contenido

    except Exception as e:
        print(f"Asistente: Lo siento, ocurrió un error al procesar tu pregunta: {e}")
        print("Por favor, verifica tu conexión a internet y tu GOOGLE_API_KEY.")
        print("Asegúrate de que tus documentos PDF no estén corruptos o vacíos.")

