from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Obtener URI de MongoDB desde variables de entorno
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise ValueError(
        "MONGO_URI no está configurada. "
        "Por favor configura la variable de entorno MONGO_URI con tu conexión a MongoDB Atlas."
    )

# Conectar a MongoDB (funciona con Atlas o local)
mongo_client = MongoClient(mongo_uri)

# Usar base de datos 'universia' (o la especificada en URI)
mongo_db = mongo_client.get_database("universia")
