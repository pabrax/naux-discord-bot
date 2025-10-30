import difflib
from typing import Dict, Any, List
import discord

from bot.utils.dicts.command_db import command_db


SIMILARITY_THRESHOLD = 0.6
MAX_SUGGESTIONS = 5


def get_command_by_name_or_alias(db: Dict[str, Dict[str, Any]], query: str):
    q = query.lower().strip()
    for name, info in db.items():
        if name.lower() == q:
            return name, info
        for alias in info.get("aliases", []):
            if alias.lower() == q:
                return name, info
    return None


def find_similar_commands(db: Dict[str, Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    query_lower = query.lower().strip()
    suggestions = []

    for command, info in db.items():
        name_l = command.lower()

        if query_lower in name_l:
            suggestions.append({"command": command, "info": info, "match_type": "name_exact", "relevance": 100})
            continue

        for alias in info.get("aliases", []):
            if query_lower in alias.lower():
                suggestions.append({"command": command, "info": info, "match_type": "alias", "relevance": 90})
                break

        if query_lower in info.get("description", "").lower():
            suggestions.append({"command": command, "info": info, "match_type": "description", "relevance": 70})

        similarity = difflib.SequenceMatcher(None, query_lower, name_l).ratio()
        if similarity > SIMILARITY_THRESHOLD:
            suggestions.append({"command": command, "info": info, "match_type": "similarity", "relevance": int(similarity * 100)})

    seen = set()
    unique = []
    for s in sorted(suggestions, key=lambda x: x["relevance"], reverse=True):
        if s["command"] not in seen:
            seen.add(s["command"])
            unique.append(s)

    return unique[:MAX_SUGGESTIONS]


def build_general_help_embed(db: Dict[str, Dict[str, Any]] = command_db) -> discord.Embed:
    embed = discord.Embed(
        title="🤖 Ayuda de Naux",
        description="¡Hola! Soy Naux, tu asistente. Aquí tienes mis comandos agrupados por categoría:",
        color=0x00FF00,
    )

    # Data-driven: categories can live in the db in the future; for now keep a safe default grouping
    categories = {
        "💬 Conversación": ["chat", "ai"],
        "🎵 Música": ["play", "connect", "skip", "queue", "np", "volume", "clear", "loop"],
        "🔧 Orquestador": ["automate", "exec", "scrape", "deploy", "backup", "status", "log"],
        "ℹ️ Información": ["ping", "serverinfo", "userinfo", "uptime", "currency", "clima"],
        "🔎 Otros": ["poke"],
    }

    for cat, cmds in categories.items():
        lines = []
        for c in cmds:
            if c in db:
                info = db[c]
                lines.append(f"`{info['usage']}` - {info['description']}")
        if lines:
            embed.add_field(name=cat, value="\n".join(lines), inline=False)

    embed.add_field(
        name="💡 Consejos",
        value="• Usa `/help <comando>` para información específica\n• Escribe parcialmente un comando para obtener sugerencias",
        inline=False,
    )
    embed.set_footer(text="¿Necesitas más? Revisa command_list o naux_manual para detalles del flujo.")
    return embed


def build_command_detail_embed(name: str, info: Dict[str, Any]) -> discord.Embed:
    embed = discord.Embed(title=f"ℹ️ Ayuda: {name}", color=0x00AAFF)
    embed.add_field(name="Uso", value=info.get("usage", "—"), inline=False)
    embed.add_field(name="Descripción", value=info.get("description", "—"), inline=False)
    examples = info.get("examples", [])
    if examples:
        embed.add_field(name="Ejemplo", value=f"`{examples[0]}`", inline=False)
    aliases = info.get("aliases", [])
    if aliases:
        embed.add_field(name="Aliases", value=", ".join(f"`{a}`" for a in aliases), inline=False)
    return embed


def build_suggestions_embed(query: str, suggestions: List[Dict[str, Any]]) -> discord.Embed:
    embed = discord.Embed(title=f"🔍 Sugerencias para: '{query}'", color=0xFFAA00)
    embed.description = "Encontré estos comandos que podrían coincidir:"
    match_icons = {"name_exact": "🎯", "alias": "🔗", "description": "📝", "similarity": "🔍"}

    for s in suggestions:
        cmd = s["command"]
        info = s["info"]
        icon = match_icons.get(s.get("match_type", ""), "❓")
        relevance = s.get("relevance", 0)
        name = f"{icon} {cmd} ({relevance}% coincidencia)"
        value = f"**Uso:** {info.get('usage', '—')}\n**Descripción:** {info.get('description', '—')}"
        examples = info.get("examples", [])
        if examples:
            value += f"\n**Ejemplo:** `{examples[0]}`"
        embed.add_field(name=name, value=value, inline=False)

    embed.set_footer(text="Tip: Usa exactamente el comando sugerido para mejores resultados")
    return embed


def build_no_results_embed(query: str, db: Dict[str, Dict[str, Any]] = command_db) -> discord.Embed:
    embed = discord.Embed(
        title=f"❓ No encontré: '{query}'",
        description="No pude encontrar comandos relacionados con tu búsqueda.",
        color=0xFF6666,
    )
    embed.add_field(
        name="💡 Consejos",
        value="• Verifica la ortografía\n• Usa `/help` para ver todos los comandos\n• Prueba con palabras clave como 'música', 'chat', 'script'",
        inline=False,
    )

    popular = ["chat", "play", "ping", "clima"]
    popular_lines = [f"`{db[c]['usage']}`" for c in popular if c in db]
    if popular_lines:
        embed.add_field(name="🔥 Comandos populares", value="\n".join(popular_lines), inline=False)

    return embed
