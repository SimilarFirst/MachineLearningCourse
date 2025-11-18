from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DependencyContainer:
    """Dependency injection container for managing services"""

    def __init__(self):
        self._services = {}
        self._singletons = {}

    def get_voice_recognizer(self):
        """Get voice recognizer instance"""
        if 'voice_recognizer' not in self._singletons:
            try:
                from mic import VoiceRecognizer, AudioProcessor, CommandRecognizer
                audio_processor = AudioProcessor()
                command_recognizer = CommandRecognizer()
                self._singletons['voice_recognizer'] = VoiceRecognizer(audio_processor, command_recognizer)
            except ImportError as e:
                logger.error(f"Failed to import voice recognition modules: {e}")
                return None
        return self._singletons['voice_recognizer']

    def get_tts_engine(self):
        """Get TTS engine instance"""
        if 'tts_engine' not in self._singletons:
            try:
                from voices import TTSEngine
                self._singletons['tts_engine'] = TTSEngine()
            except ImportError as e:
                logger.error(f"Failed to import TTS engine: {e}")
                return None
        return self._singletons['tts_engine']

    def get_reminder_manager(self):
        """Get reminder manager instance"""
        if 'reminder_manager' not in self._singletons:
            try:
                from voices import ReminderManager
                self._singletons['reminder_manager'] = ReminderManager()
            except ImportError as e:
                logger.error(f"Failed to import reminder manager: {e}")
                return None
        return self._singletons['reminder_manager']

    def get_ai_chat(self):
        """Get AI chat instance"""
        if 'ai_chat' not in self._singletons:
            try:
                from api_integrations import AIChat
                self._singletons['ai_chat'] = AIChat()
            except ImportError as e:
                logger.error(f"Failed to import AI chat: {e}")
                return None
        return self._singletons['ai_chat']

    def get_weather_api(self):
        """Get weather API instance"""
        if 'weather_api' not in self._singletons:
            try:
                from api_integrations import WeatherAPI
                self._singletons['weather_api'] = WeatherAPI()
            except ImportError as e:
                logger.error(f"Failed to import weather API: {e}")
                return None
        return self._singletons['weather_api']

    def get_character_renderer(self):
        """Get character renderer instance"""
        if 'character_renderer' not in self._singletons:
            try:
                from rendering import CharacterRenderer
                self._singletons['character_renderer'] = CharacterRenderer()
            except ImportError as e:
                logger.error(f"Failed to import character renderer: {e}")
                return None
        return self._singletons['character_renderer']

    def cleanup(self):
        """Cleanup all services"""
        for service in self._singletons.values():
            if hasattr(service, 'cleanup'):
                try:
                    service.cleanup()
                except Exception as e:
                    logger.error(f"Error cleaning up service {service}: {e}")

        self._singletons.clear()
        self._services.clear()