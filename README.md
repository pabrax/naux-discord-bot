# Naux Discord Bot

Un bot multifuncional para Discord que actúa como asistente personal, reproduce música, responde preguntas y gestiona acciones en tu servidor.

## Características

- 🎵 **Reproductor de música** - Reproduce música desde diversas fuentes
- 🤖 **Asistente personal** - Responde preguntas y ayuda con tareas
- ⚙️ **Gestión de servidor** - Automatiza acciones administrativas
- 🔧 **Fácil configuración** - Setup simple con uv

## Instalación

### Prerrequisitos

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) - Gestor de paquetes y entornos virtuales de Python

### Pasos de instalación

1. **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/naux-discord-bot.git
    cd naux-discord-bot
    ```

2. **Instala las dependencias:**
    ```bash
    uv sync
    ```

3. **Configura las variables de entorno:**
    ```bash
    cp .env.example .env
    # Edita .env con tu token de Discord y otras configuraciones
    ```

## Ejecución

```bash
uv run run.py
```

## Configuración

Asegúrate de configurar las siguientes variables en tu archivo `.env`:

- `DISCORD_TOKEN` - Token de tu bot de Discord
- `PREFIX` - Prefijo para los comandos (por defecto: `!`)

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Envía un pull request

## Licencia

Este proyecto está bajo la licencia MIT.
