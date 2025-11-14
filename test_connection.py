"""
Script para probar la conexión a MongoDB Atlas
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Cargar variables de entorno
load_dotenv()

print("🔍 Probando conexión a MongoDB Atlas...")
print("-" * 50)

# Obtener URI
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    print("❌ ERROR: MONGO_URI no está configurada en .env")
    exit(1)

print(f"📡 URI detectada: {mongo_uri[:50]}...")

try:
    # Intentar conectar
    print("\n⏳ Conectando...")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # Probar la conexión
    client.admin.command('ping')
    
    print("✅ Conexión exitosa a MongoDB Atlas!")
    
    # Obtener base de datos
    db = client.universia
    
    # Listar colecciones
    collections = db.list_collection_names()
    print(f"\n📚 Base de datos: universia")
    print(f"📂 Colecciones encontradas: {len(collections)}")
    
    if collections:
        for col in collections:
            count = db[col].count_documents({})
            print(f"   - {col}: {count} documentos")
    else:
        print("   (Sin colecciones aún - se crearán al usar la app)")
    
    print("\n✅ Tu proyecto está listo para usar MongoDB Atlas!")
    
except Exception as e:
    print(f"\n❌ ERROR al conectar:")
    print(f"   {str(e)}")
    print("\n💡 Verifica:")
    print("   1. Tu usuario/password en MongoDB Atlas")
    print("   2. Que la IP 0.0.0.0/0 esté en Network Access")
    print("   3. Que el cluster esté activo")
    
finally:
    if 'client' in locals():
        client.close()
