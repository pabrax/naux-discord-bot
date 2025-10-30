

## **USO GENERAL** — *Comandos de orientación y convivencia básica*

| Comando     | Propósito                                              | Comentario estratégico                                                      |
| ----------- | ------------------------------------------------------ | --------------------------------------------------------------------------- |
| `!help`     | Muestra categorías de comandos y breve descripción.    | Útil si lo haces modular (p. ej. `!help música`, `!help automatizaciones`). |
| `!ping`     | Verifica latencia.                                     | Sencillo. Puede incluir uptime para mayor sentido.                          |
| `!clima`    | Estado del clima en una ciudad (por defecto Medellín). | Mejor si permite `!clima <ciudad>` para flexibilidad.                       |
| `!cls`      | Limpia X mensajes recientes.                           | Bot moderación suave; procura permisos correctos.                           |
| `!currency` | Muestra tasa de conversión entre monedas.              | Si lo conectas a una API, considera caching para no abusar.                 |
| `!chat`     | Interacción conversacional general.                    | Puede ser IA, pero ten claro el tono: breve, útil, no invasivo.             |

**Sugerencias para expandir este bloque:**

| Nuevo comando        | Qué resuelve                                                                    |
| -------------------- | ------------------------------------------------------------------------------- |
| `!uptime`            | Saber cuánto tiempo lleva funcionando el bot (útil para monitoreo).             |
| `!serverinfo`        | Datos del servidor (roles, usuarios, canales); sirve para diagnósticos rápidos. |
| `!userinfo @usuario` | Info de un usuario: roles, fecha ingreso, etc. Apoya interacción social.        |

---

## **MÚSICA** — *Zona de experiencia compartida*

Ya marcaste los esenciales. La clave aquí no es agregar más, sino **pulir la experiencia**:

| Comando                | Propósito                     |
| ---------------------- | ----------------------------- |
| `!play <url / nombre>` | Reproduce o agrega a la cola. |
| `!connect`             | Entra al VC del usuario.      |
| `!skip`                | Salta canción actual.         |
| `!disconnect`          | Sale del VC.                  |
| `!queue`               | Lista la cola.                |
| `!np`                  | Muestra canción actual.       |
| `!volume <0-100>`      | Ajusta volumen.               |
| `!clear`               | Vacía la cola.                |
| `!loop`                | Alterna repetición.           |

**Pequeñas mejoras de experiencia a considerar:**

| Mejora                                   | Por qué vale             |
| ---------------------------------------- | ------------------------ |
| Mostrar *thumbnail* y duración en `!np`. | Aporta presencia visual. |
| Buscar por nombre si no es URL.          | Flujo más natural.       |
| Autocomplete para `!play`.               | Se siente “profesional”. |

La música es la capa “social” de tu bot.

---

## **ACCIONES QUE VIVEN FUERA DEL BOT** — *Tu bot como panel de control remoto*

Aquí es donde tu bot deja de ser un bot “de servidor” y se vuelve parte de tu **infraestructura personal**.

| Comando                  | Propósito                                                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `!automate <acción>`     | Ejecuta flujos externos (n8n / Zapier / Webhooks). Ideal para: enviar emails, publicar mensajes, limpiar repos, crear archivos, etc.  |
| `!exec <acción>`         | Ejecuta funciones internas del servidor: scripts Python, Bash, o interacciones con tu software propio. Peligroso → controla permisos. |
| `!scrape <url> <target>` | Corre scraping con tu pipeline personalizado. Te permite extraer datos sin abrir navegador.                                           |

**Este bloque es el corazón de tu bot.**

Lo amplío con ideas concretas:

| Nuevo comando        | Qué haría                                                                   | Para qué sirve                                            |
| -------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------- |
| `!status`            | Ver estado de tus servicios (pings a contenedores, base de datos, workers). | Diagnóstico rápido de tu infraestructura.                 |
| `!deploy <proyecto>` | Despliega una app vía webhook o runner.                                     | Controlar despliegues desde Discord.                      |
| `!backup <servicio>` | Ejecuta una tarea de respaldo.                                              | Mantener sistemas seguros sin abrir la terminal.          |
| `!log <servicio>`    | Devuelve las últimas líneas de logs.                                        | Depuración remota básica.                                 |
| `!ai <prompt>`       | Solicita una inferencia a tu modelo / API.                                  | Un canal para pensamiento ligero sin cambiar de contexto. |

Esto convierte tu bot en **tu CLI distribuida**.

---

## **DISEÑO GLOBAL**

Tu bot se divide ahora en **tres capas claras**:

| Capa        | Función                                          | Cómo se siente                                    |
| ----------- | ------------------------------------------------ | ------------------------------------------------- |
| Social      | Música, respuestas, clima, chat.                 | Hace el servidor más agradable y vivo.            |
| Asistente   | Información útil: divisas, clima, `!serverinfo`. | Acceso rápido a datos sin cambiar de app.         |
| Orquestador | `!automate`, `!exec`, `!deploy`, `!log`.         | El bot se vuelve un *punto de control operativo*. |

Tu bot ya no es “un bot”, es **tu interfaz conversacional hacia tu propio ecosistema**.

La gracia no está en tener mil comandos, sino en que **cada comando tenga un caso real detrás**.

---

1. Priorizar: ¿qué de lo externo necesitas controlar primero?
2. Diseñar el *estándar de comandos* (nombres, estructura, feedback, permisos).
3. Escribir una base “segura” para `!automate` y `!exec` (evitar que otros abusen de eso).

