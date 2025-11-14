# 📡 API Documentation - IA Tutora Service

**Base URL:** `https://iatutora.onrender.com`

**Servicio:** Tutor IA para UniversIA  
**Tecnología:** Flask 3.1.2 + Google Gemini 2.0 Flash + MongoDB Atlas  
**Hosting:** Render (Free Tier)  
**Librería IA:** google-genai 0.3.0

---

## 🔐 Autenticación

No requiere autenticación en el servicio de IA. La autenticación debe manejarse en Next.js antes de llamar a estos endpoints.

---

## 📋 Endpoints

### 1. Iniciar Clase

Inicia una nueva sesión de clase con el tutor IA. El tutor presenta la clase y hace una pregunta inicial al estudiante.

**Endpoint:**
```
POST /api/ia/start
```

**URL Completa:**
```
https://iatutora.onrender.com/api/ia/start
```

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "user_id": "string" // ID único del estudiante
}
```

**Ejemplo de Request:**
```javascript
fetch('https://iatutora.onrender.com/api/ia/start', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_id: "estudiante-123"
  })
})
```

**Response (200 OK):**
```json
{
  "response": "¡Bienvenido a la Clase 1: Introducción a la Computación en la Nube!\n\nHoy exploraremos los conceptos fundamentales de la nube...\n\n¿Tienes alguna experiencia previa con servicios en la nube como Google Drive o Dropbox?"
}
```

**Códigos de Estado:**
- `200` - Éxito
- `400` - Error: `user_id` no proporcionado
- `500` - Error interno del servidor

---

### 2. Preguntar al Tutor

Envía una pregunta o respuesta al tutor IA. El tutor mantiene contexto de la conversación y proporciona feedback pedagógico.

**Endpoint:**
```
POST /api/ia/ask
```

**URL Completa:**
```
https://iatutora.onrender.com/api/ia/ask
```

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "user_id": "string",  // ID único del estudiante
  "message": "string"   // Pregunta o respuesta del estudiante
}
```

**Ejemplo de Request:**
```javascript
fetch('https://iatutora.onrender.com/api/ia/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_id: "estudiante-123",
    message: "¿Qué diferencia hay entre IaaS, PaaS y SaaS?"
  })
})
```

**Response (200 OK):**
```json
{
  "response": "Excelente pregunta. Estas son las tres capas principales de servicios en la nube:\n\n**IaaS (Infrastructure as a Service):**\n- Proporciona infraestructura virtualizada\n- Ejemplo: Amazon EC2, Google Compute Engine\n\n**PaaS (Platform as a Service):**\n- Plataforma completa para desarrollo\n- Ejemplo: Heroku, Google App Engine\n\n**SaaS (Software as a Service):**\n- Aplicaciones listas para usar\n- Ejemplo: Gmail, Salesforce\n\n¿Te gustaría que profundice en alguno de estos modelos?"
}
```

**Códigos de Estado:**
- `200` - Éxito
- `400` - Error: `user_id` o `message` no proporcionados
- `500` - Error interno del servidor

---

## 🗄️ Almacenamiento

El servicio guarda automáticamente en **MongoDB Atlas**:

### Colección: `historial`
Almacena todas las interacciones entre estudiante y tutor.

```javascript
{
  "user_id": "estudiante-123",
  "type": "start_class" | "ask",
  "student_message": "¿Qué es la nube?",
  "professor_response": "La nube es...",
  "timestamp": ISODate("2025-11-14T10:30:00Z")
}
```

### Colección: `resumen`
Mantiene un resumen acumulativo de la clase para cada estudiante.

```javascript
{
  "user_id": "estudiante-123",
  "summary": "Resumen completo de conceptos vistos...",
  "updated_at": ISODate("2025-11-14T10:35:00Z")
}
```

---

## ⚡ Consideraciones de Rendimiento

### Cold Start (Plan Gratuito de Render)
- **Primera petición después de 15 min de inactividad:** 30-60 segundos
- **Peticiones subsecuentes:** 2-5 segundos
- **Recomendación:** Mostrar loading state en el frontend

### Timeouts Recomendados
```javascript
// En Next.js API Route
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout

try {
  const response = await fetch(url, {
    signal: controller.signal,
    // ... otras opciones
  });
} finally {
  clearTimeout(timeoutId);
}
```

---

## 🔗 Integración con Next.js

### 1. Variables de Entorno

Agregar en `.env.local`:

```env
# IA Tutor Service
TUTOR_SERVICE_URL=https://iatutora.onrender.com
```

### 2. API Route: `app/api/chat/tutor/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/auth';

export async function POST(request: NextRequest) {
  try {
    const session = await auth();
    if (!session?.user) {
      return NextResponse.json({ error: 'No autenticado' }, { status: 401 });
    }

    const { message } = await request.json();

    const response = await fetch(
      `${process.env.TUTOR_SERVICE_URL}/api/ia/ask`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: session.user.id,
          message: message,
        }),
      }
    );

    if (!response.ok) {
      throw new Error('Error del servicio IA');
    }

    const data = await response.json();
    return NextResponse.json({ success: true, response: data.response });

  } catch (error) {
    return NextResponse.json(
      { error: 'Error al procesar solicitud' },
      { status: 500 }
    );
  }
}
```

### 3. API Route: `app/api/chat/tutor/start/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/auth';

export async function POST(request: NextRequest) {
  try {
    const session = await auth();
    if (!session?.user) {
      return NextResponse.json({ error: 'No autenticado' }, { status: 401 });
    }

    const response = await fetch(
      `${process.env.TUTOR_SERVICE_URL}/api/ia/start`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: session.user.id,
        }),
      }
    );

    if (!response.ok) {
      throw new Error('Error al iniciar clase');
    }

    const data = await response.json();
    return NextResponse.json({ success: true, response: data.response });

  } catch (error) {
    return NextResponse.json(
      { error: 'Error al iniciar clase' },
      { status: 500 }
    );
  }
}
```

### 4. Uso en Frontend

```typescript
// Iniciar clase
const startClass = async () => {
  const response = await fetch('/api/chat/tutor/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ courseId: 'curso-123' }),
  });
  
  const data = await response.json();
  if (data.success) {
    console.log(data.response); // Mensaje inicial del tutor
  }
};

// Enviar mensaje
const sendMessage = async (message: string) => {
  const response = await fetch('/api/chat/tutor', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  
  const data = await response.json();
  if (data.success) {
    console.log(data.response); // Respuesta del tutor
  }
};
```

---

## 🧪 Testing

### cURL Examples

```bash
# Iniciar clase
curl -X POST https://iatutora.onrender.com/api/ia/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-123"}'

# Hacer pregunta
curl -X POST https://iatutora.onrender.com/api/ia/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-123", "message": "¿Qué es la nube?"}'
```

### PowerShell Examples

```powershell
# Iniciar clase
Invoke-WebRequest -Uri "https://iatutora.onrender.com/api/ia/start" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"user_id": "test-123"}' | 
  Select-Object -ExpandProperty Content

# Hacer pregunta
Invoke-WebRequest -Uri "https://iatutora.onrender.com/api/ia/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"user_id": "test-123", "message": "¿Qué es la nube?"}' |
  Select-Object -ExpandProperty Content
```

---

## ⚠️ Limitaciones

### Plan Gratuito de Render
- ⏰ El servicio se duerme tras 15 minutos de inactividad
- 🔄 Tiempo de "despertar": 30-60 segundos en la primera petición
- 💾 750 horas de ejecución por mes
- 🌐 Sin custom domain (puedes usar el dominio .onrender.com)

### Google Gemini API
- 📊 Límites de tokens por minuto según tu plan
- ⚡ Rate limiting aplicado automáticamente

---

## 🐛 Manejo de Errores

### Errores Comunes

**Error 400 - Bad Request:**
```json
{
  "error": "user_id requerido"
}
```
**Solución:** Verificar que se envía `user_id` en el body.

---

**Error 500 - Internal Server Error:**
```json
{
  "error": "Error interno del servidor"
}
```
**Posibles causas:**
- MongoDB Atlas desconectado
- Google Gemini API sin respuesta
- Error en el procesamiento del PDF

**Solución:** Revisar logs en Render Dashboard.

---

**Timeout:**
```
Error: Request timeout
```
**Solución:** Implementar retry logic y aumentar timeout a 60s.

---

## 📊 Monitoreo

### Render Dashboard
- **Logs:** Ver en tiempo real las peticiones y respuestas
- **Metrics:** CPU, memoria, requests por minuto
- **URL:** https://dashboard.render.com

### MongoDB Atlas
- **Database → Browse Collections:** Ver datos guardados
- **Monitoring:** Conexiones activas, queries lentas
- **URL:** https://cloud.mongodb.com

---

## 🔧 Troubleshooting

### El servicio no responde
1. Verificar en Render Dashboard que el servicio está "Live"
2. Revisar logs para errores
3. Verificar variables de entorno (MONGO_URI, GOOGLE_API_KEY)

### Respuestas lentas
1. Cold start normal: 30-60s en primera petición
2. Considerar upgrade a plan pagado para eliminar cold starts
3. Implementar ping periódico (cada 14 min) para mantener activo

### Errores de MongoDB
1. Verificar Network Access en MongoDB Atlas (`0.0.0.0/0`)
2. Verificar que el usuario tiene permisos de lectura/escritura
3. Revisar MONGO_URI en variables de entorno de Render

---

## 📞 Soporte

**Repositorio:** https://github.com/RuizJpaul/iatutora  
**Issues:** https://github.com/RuizJpaul/iatutora/issues

---

**Última actualización:** Noviembre 14, 2025  
**Versión:** 1.0.0  
**Status:** ✅ Production Ready
