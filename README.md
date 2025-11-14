# 🤖 IA Tutora - Servicio de Tutoría con IA

Sistema de tutoría inteligente que utiliza **Google Gemini** para proporcionar una experiencia de aprendizaje personalizada, guiando a los estudiantes a través de clases universitarias con feedback instantáneo y contextual.

## 📋 Características

- 🎓 **Tutor IA Personalizado**: Explica conceptos en bloques cortos y claros
- 📚 **Basado en Contenido PDF**: Lee y procesa material educativo automáticamente
- 💬 **Historial de Conversación**: Mantiene contexto de interacciones previas
- 📝 **Resumen Acumulativo**: Genera y actualiza resúmenes de la clase
- 🔄 **Feedback Pedagógico**: Resuelve dudas antes de avanzar al siguiente tema

## 🏗️ Arquitectura

```
iatutora/
├── run.py                      # Punto de entrada de la aplicación
├── src/
│   ├── __init__.py            # Configuración de Flask
│   ├── routes/
│   │   └── ia_class.py        # Endpoints de IA (/start, /ask)
│   └── utils/
│       ├── extract.py         # Extracción de texto de PDFs
│       └── mongo.py           # Conexión a MongoDB
├── uploads/
│   └── clase01.pdf            # Material educativo
├── requirements.txt           # Dependencias Python
├── Procfile                   # Configuración para Render
├── .env.example              # Plantilla de variables de entorno
└── .gitignore                # Archivos a ignorar en Git
```

## 🚀 Deployment en Render

### 1. Prerequisitos

- Cuenta en [Render](https://render.com)
- Cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (gratis)
- API Key de [Google AI Studio](https://aistudio.google.com/app/apikey)

### 2. Configurar MongoDB Atlas

1. Crear cuenta en https://cloud.mongodb.com
2. Crear un **Cluster gratuito** (M0 Sandbox - 512MB)
3. En **Database Access**: Crear usuario con contraseña
4. En **Network Access**: Agregar IP `0.0.0.0/0` (permitir todo)
5. En **Database**: Click "Connect" → "Connect your application"
6. Copiar el **Connection String**:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/universia?retryWrites=true&w=majority
   ```
7. Reemplazar `<username>` y `<password>` con tus credenciales

### 3. Obtener API Key de Google Gemini

1. Visitar https://aistudio.google.com/app/apikey
2. Crear un nuevo proyecto (si no tienes uno)
3. Generar API Key
4. Copiar la key (formato: `AIzaSy...`)

### 4. Desplegar en Render

#### Opción A: Desde GitHub (Recomendado)

1. **Subir código a GitHub:**
   ```bash
   cd iatutora
   git init
   git add .
   git commit -m "Initial commit - IA Tutora"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/iatutora.git
   git push -u origin main
   ```

2. **En Render Dashboard:**
   - Click **"New +"** → **"Web Service"**
   - Connect tu repositorio de GitHub
   - Configurar:
     - **Name**: `iatutora` (o el nombre que prefieras)
     - **Region**: Oregon (US West) o la más cercana
     - **Branch**: `main`
     - **Root Directory**: (dejar vacío)
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn run:app` (detecta automáticamente el Procfile)
     - **Plan**: `Free`

3. **Variables de Entorno** (en Render):
   - Click **"Environment"** → **"Add Environment Variable"**
   - Agregar:
     ```
     MONGO_URI = mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/universia
     GOOGLE_API_KEY = AIzaSyC8Ewo8C9hOwqz8C5mX807Y8I-fUVrMIN8
     FLASK_ENV = production
     ```

4. **Deploy:**
   - Click **"Create Web Service"**
   - Esperar 5-10 minutos mientras se despliega
   - Obtener URL: `https://iatutora-xxx.onrender.com`

#### Opción B: Deploy Manual (sin GitHub)

1. En Render: **"New +"** → **"Web Service"** → **"Deploy an existing image from a registry"**
2. Subir código comprimido (ZIP)
3. Seguir los mismos pasos de configuración

### 5. Verificar Deployment

Una vez desplegado, probar los endpoints:

```bash
# Health check (si implementas uno)
curl https://iatutora-xxx.onrender.com/

# Iniciar clase
curl -X POST https://iatutora-xxx.onrender.com/api/ia/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-user-123"}'

# Hacer una pregunta
curl -X POST https://iatutora-xxx.onrender.com/api/ia/ask \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-123",
    "message": "¿Qué es la computación en la nube?"
  }'
```

## 💻 Desarrollo Local

### 1. Clonar repositorio

```bash
git clone https://github.com/tu-usuario/iatutora.git
cd iatutora
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar `.env.example` a `.env` y completar:

```bash
cp .env.example .env
```

Editar `.env`:
```env
MONGO_URI=mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/universia
GOOGLE_API_KEY=AIzaSy...
FLASK_ENV=development
```

### 5. Ejecutar aplicación

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## 📡 API Endpoints

### `POST /api/ia/start`

Inicia una nueva clase con el tutor IA.

**Request:**
```json
{
  "user_id": "estudiante-123"
}
```

**Response:**
```json
{
  "response": "¡Bienvenido a la Clase 1! Hoy hablaremos sobre...\n\n¿Tienes alguna experiencia previa con la nube?"
}
```

### `POST /api/ia/ask`

Envía una pregunta al tutor IA.

**Request:**
```json
{
  "user_id": "estudiante-123",
  "message": "¿Qué es IaaS?"
}
```

**Response:**
```json
{
  "response": "IaaS (Infrastructure as a Service) es un modelo de computación en la nube donde...\n\n¿Te gustaría que te dé un ejemplo práctico?"
}
```

## 🗄️ Colecciones de MongoDB

### `historial`
Almacena todas las interacciones entre estudiante y tutor IA.

```javascript
{
  "_id": ObjectId,
  "user_id": "estudiante-123",
  "type": "start" | "ask",
  "student_message": "¿Qué es la nube?",
  "professor_response": "La nube es...",
  "timestamp": ISODate
}
```

### `resumen`
Mantiene un resumen acumulativo de la clase para cada estudiante.

```javascript
{
  "_id": ObjectId,
  "user_id": "estudiante-123",
  "summary": "Resumen completo de todos los conceptos vistos...",
  "updated_at": ISODate
}
```

## 🔧 Tecnologías Utilizadas

- **Flask 3.0** - Framework web
- **Google Generative AI (Gemini)** - Modelo de lenguaje
- **MongoDB** - Base de datos NoSQL
- **PDFPlumber** - Extracción de texto de PDFs
- **Gunicorn** - Servidor WSGI para producción
- **python-dotenv** - Gestión de variables de entorno

## 📝 Notas Importantes

### Limitaciones del Plan Gratuito de Render

- ⏰ **Inactividad**: El servicio se "duerme" después de 15 minutos sin uso
- 🔄 **Primera carga**: Puede tardar 30-60 segundos en "despertar"
- 💾 **Almacenamiento**: Archivos subidos se borran con cada deploy
- ⏱️ **Tiempo de ejecución**: 750 horas/mes (suficiente para desarrollo)

### Recomendaciones

1. **PDF en el repositorio**: El archivo `clase01.pdf` debe estar en Git para que esté disponible en producción
2. **MongoDB Atlas**: Asegúrate de que la IP `0.0.0.0/0` esté whitelisted
3. **API Keys**: NUNCA subir el archivo `.env` a GitHub (ya está en `.gitignore`)
4. **Logs**: Monitorear en Render Dashboard → Tu servicio → Logs

## 🔐 Seguridad

- ✅ Variables de entorno protegidas con `.env`
- ✅ `.gitignore` configurado para excluir archivos sensibles
- ✅ Conexión segura a MongoDB Atlas (TLS/SSL)
- ⚠️ **TODO**: Implementar autenticación de usuarios
- ⚠️ **TODO**: Rate limiting para prevenir abuso

## 🐛 Troubleshooting

### Error: "MONGO_URI no está configurada"
- Verificar que la variable esté en Render → Environment Variables
- Revisar que no haya espacios extra en el valor

### Error: "Authentication failed"
- Verificar usuario/password de MongoDB Atlas
- Confirmar que el usuario tenga permisos de lectura/escritura

### El servicio no responde
- Revisar logs en Render Dashboard
- Verificar que el `Procfile` esté correcto
- Confirmar que `gunicorn` esté en `requirements.txt`

### PDFs no se encuentran
- Asegúrate de que `/uploads/clase01.pdf` esté en el repositorio
- Verifica la ruta en `ia_class.py` (línea 12)

## 📞 Soporte

Para problemas o preguntas:
- 📧 Email: [tu-email]
- 🐛 Issues: https://github.com/tu-usuario/iatutora/issues

## 📄 Licencia

Este proyecto es parte del sistema **UniversIA** - Plataforma educativa con IA.

---

**Última actualización:** Noviembre 14, 2025
