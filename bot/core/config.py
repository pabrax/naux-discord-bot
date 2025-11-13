import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Cargar variables de entorno
load_dotenv()

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiscordConfig:
    """Configuración específica de Discord"""
    
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.channel_id = self._get_channel_id()
        self.prefix = os.getenv("PREFIX", "!")
        
        # Validación crítica
        if not self.token:
            raise ValueError("❌ DISCORD_TOKEN es requerido en las variables de entorno")
        
        logger.info("✅ Configuración de Discord cargada correctamente")
    
    def _get_channel_id(self) -> Optional[int]:
        """Obtener channel ID con validación"""
        channel_id_str = os.getenv("DISCORD_CHANNEL_ID")
        if channel_id_str:
            try:
                return int(channel_id_str)
            except ValueError:
                logger.warning(f"⚠️ DISCORD_CHANNEL_ID inválido: {channel_id_str}")
                return None
        return None


class LLMConfig:
    """Configuración del modelo de lenguaje"""
    
    def __init__(self):
        self.model_name = os.getenv("IA_MODEL_NAME")
        self.api_key = os.getenv("IA_API_KEY")
        self.api_url = os.getenv("IA_API_URL")
        
        # Validación
        self._validate_config()
        logger.info(f"✅ Configuración LLM cargada - Modelo: {self.model_name}")
    
    def _validate_config(self):
        """Validar configuración del LLM"""
        if not self.api_key:
            raise ValueError("❌ IA_API_KEY es requerido")
        if not self.model_name:
            raise ValueError("❌ IA_MODEL_NAME es requerido")
        if not self.api_url:
            raise ValueError("❌ IA_API_URL es requerido")


class AppConfig:
    """Configuración general de la aplicación"""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        logger.info(f"✅ Configuración general - Entorno: {self.environment}")


# Instancias globales de configuración
try:
    discord_config = DiscordConfig()
    llm_config = LLMConfig()
    app_config = AppConfig()
    
    # Backward compatibility - mantener las variables originales
    DISCORD_TOKEN = discord_config.token
    DISCORD_CHANNEL_ID = discord_config.channel_id or 0
    PREFIX = discord_config.prefix
    
    # Para compatibilidad con groq_model.py
    class IaSettings:
        IA_MODEL_NAME = llm_config.model_name
        IA_API_KEY = llm_config.api_key
        IA_API_URL = llm_config.api_url
    
    ia_settings = IaSettings()
    
    logger.info("🚀 Todas las configuraciones cargadas exitosamente")
    
except Exception as e:
    logger.error(f"❌ Error cargando configuración: {e}")
    raise
