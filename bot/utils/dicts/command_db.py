command_db = {
    
    # Basicos
    "help": {
        "description": "📚 Mostrar categorías de comandos y ayuda contextual",
        "usage": "/help [categoría]",
        "examples": ["/help", "/help música"],
        "aliases": ["menu"],
    },
    "ping": {
        "description": "🏓 Verificar latencia del bot",
        "usage": "/ping",
        "examples": ["/ping"],
        "aliases": [],
    },
    "clima": {
        "description": "🌤️ Obtener clima de una ciudad (por defecto Medellín)",
        "usage": "/clima [ciudad]",
        "examples": ["/clima", "/clima Bogotá"],
        "aliases": ["weather"],
    },
    "currency": {
        "description": "💱 Convertir entre monedas",
        "usage": "/currency from:<moneda> to:<moneda>",
        "examples": ["/currency from:USD to:COP"],
        "aliases": ["fx", "cotizacion"],
    },
    "chat": {
        "description": "💬 Conversación con IA (historial opcional)",
        "usage": "/chat prompt:<mensaje>",
        "examples": ["/chat prompt:Hola, resume este texto..."],
        "aliases": ["ai", "llm"],
    },
    "uptime": {
        "description": "⏱️ Mostrar tiempo de actividad del bot",
        "usage": "/uptime",
        "examples": ["/uptime"],
        "aliases": [],
    },
    "serverinfo": {
        "description": "🖥️ Mostrar información del servidor (miembros, roles, canales)",
        "usage": "/serverinfo",
        "examples": ["/serverinfo"],
        "aliases": ["server"],
    },
    "userinfo": {
        "description": "ℹ️ Mostrar información de un usuario",
        "usage": "/userinfo user:<usuario>",
        "examples": ["/userinfo user:@pablo"],
        "aliases": ["user"],
    },

    # Musica
    "play": {
        "description": "🎵 Añadir a la cola / reproducir (audio en voz)",
        "usage": "/play query:<url|nombre>",
        "examples": ["/play query:https://..."],
        "aliases": ["reproducir"],
    },
    "queue": {
        "description": "📜 Mostrar la cola de reproducción",
        "usage": "/queue",
        "examples": ["/queue"],
        "aliases": [],
    },
    "skip": {
        "description": "⏭️ Saltar la canción actual",
        "usage": "/skip",
        "examples": ["/skip"],
        "aliases": [],
    },
    "np": {
        "description": "🎧 Mostrar la canción que está sonando",
        "usage": "/np",
        "examples": ["/np"],
        "aliases": ["nowplaying"],
    },
    "volume": {
        "description": "🔊 Ajustar volumen de reproducción",
        "usage": "/volume level:<0-100>",
        "examples": ["/volume level:50"],
        "aliases": [],
    },
    "loop": {
        "description": "🔁 Alternar repetición (canción o cola según opción)",
        "usage": "/loop mode:<off|song|queue>",
        "examples": ["/loop mode:song", "/loop mode:queue"],
        "aliases": [],
    },
    "poke": {
        "description": "🐾 Consultar datos de un Pokémon",
        "usage": "/poke name:<nombre>",
        "examples": ["/poke name:pikachu"],
        "aliases": [],
    },
}
