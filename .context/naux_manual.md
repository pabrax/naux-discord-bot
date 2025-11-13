# Naux - Manual de Diseño y Arquitectura (v1)

## 1. Propósito del Proyecto
Naux es un bot de Discord orientado a servir como asistente general y herramienta de automatización. Su función principal es apoyar a los usuarios del servidor mediante conversación inteligente y la capacidad de ejecutar acciones reales a través de servicios externos, flujos automatizados o scripts locales.

No está pensado como moderador o administrador estricto. Su enfoque es acompañar, asistir y conectar.

## 2. Descripción General
Naux:
- Responde preguntas y mantiene conversaciones usando un modelo de lenguaje (LLM).
- Puede reproducir música en canales de voz.
- Se integra con APIs externas y flujos automatizados (p. ej. n8n).
- Puede ejecutar acciones locales o remotas a través de endpoints (scripts, servicios, tareas automatizadas).

Su objetivo es ser útil y accesible en el día a día del servidor.

## 3. Filosofía de Diseño
- **Modularidad:** Cada capacidad (música, conversación, acciones, integraciones) es un módulo independiente.
- **Simplicidad primero:** Se construye para poder entenderlo, modificarlo y extenderlo sin depender de una infraestructura compleja.
- **Asistente, no humano:** Naux se expresa de forma amigable y clara, pero reconoce que es una herramienta.
- **Acciones explícitas:** Para tareas que afectan sistemas (ej. actualizar servicios), se usan comandos estructurados. Para tareas simples, lenguaje natural.

## 4. Alcance de la Versión Local (MVP)
La versión inicial está pensada para uso personal/local.  
Características principales:
- Corre en una máquina local o VPS pequeño.
- Se comunica con flujos externos (ej. n8n) mediante webhooks o APIs simples.
- Ejecuta scripts locales cuando se solicite.
- Mantiene conversaciones útiles por medio del LLM.
- Reproduce música de forma básica.

No incluye:
- Panel de configuración
- Multi-servidor a escala
- Dashboards de monitoreo
- Persistencia compleja

Estos elementos pueden considerarse en versiones futuras.

## 5. Arquitectura General

```
Discord Client
     │
     ▼
     ├── Módulo LLM (adaptador a modelo elegido)
     │
     ├── Action Router
     │       ├── Webhooks (n8n)
     │       ├── APIs externas
     │       └── Scripts locales
     │
     └── Music Engine
```

- **Discord Client:** Maneja eventos y comandos de Discord.
- **LLM Module:** Maneja prompts y respuestas del modelo.
- **Action Router:** Punto único para ejecución de tareas y disparo de flujos.
- **Music Engine:** Maneja reproducción en canales de voz.

## 6. Módulos Principales

### 6.1 Discord Gateway
- Recibe mensajes, slash commands y eventos de Discord.
- Deriva comandos estructurados al Action Router.
- Deriva mensajes abiertos al Módulo LLM.


### 6.3 Módulo LLM
- Adapta llamadas al modelo elegido (OpenAI, Ollama, etc).
- Maneja prompts base, evitando que el bot actúe como humano.
- Provee respuestas formateadas para Discord.

### 6.4 Módulo Acciones Remotas
- Define acciones como funciones y endpoints.
- Puede:
  - Llamar flujos en n8n (webhooks).
  - Ejecutar scripts locales.
  - Interactuar con servicios HTTP.
- Se prioriza claridad y trazabilidad sobre complejidad.

### 6.5 Módulo Música
- Maneja conexión a voz, colas de reproducción y cierre.
- Se mantiene simple para evitar problemas de estabilidad.

## 7. Estándares de Desarrollo
- Código organizado por módulos.
- No hardcodear rutas de servicios externos.
- Variables sensibles van en `.env`.
- Logs simples: cada acción registra fecha, tipo y resultado.

## 8. Entorno y Configuración
- Python 3.10+
- Librería de Discord (discord.py o nextcord)
- Cliente para LLM según proveedor
- `.env` para tokens (Discord, APIs, etc.)

## 9. Casos de Uso Principales

1. **Conversa con el usuario:**
   ```
   Usuario → "Naux, explícame X"
   Naux → Respuesta del LLM
   ```

2. **Dispara una automatización:**
   ```
   /call_service nombre=deploy_proyecto
   Action Router → webhook n8n → acción ejecutada
   ```

3. **Ejecuta un script local:**
   ```
   /run_script actualizar_dependencias
   ```

4. **Reproduce música:**
   ```
   /play <enlace>
   ```

## 10. Futuro y Escalabilidad
Versión futura orientada a terceros:
- Gestión de acciones configurables desde una interfaz.
- Usuario define sus propios flujos externos.
- Multi-servidor con carga balanceada.
- Persistencia para historial y preferencias.
