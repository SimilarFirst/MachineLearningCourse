"""
Dependency Injection контейнер для приложения Акира
"""
from typing import Optional
from config import logger


class DependencyContainer:
    """Контейнер зависимостей (Singleton)"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._tts_engine = None
            self._voice_recognizer = None
            self._weather_service = None
            self._ai_chat = None
            self._reminder_manager = None
            self._character_3d = None
            DependencyContainer._initialized = True
    
    def get_tts_engine(self):
        """Получение TTS движка"""
        if self._tts_engine is None:
            from voices import TTSEngine
            self._tts_engine = TTSEngine()
            self._tts_engine.load_model()
            logger.info("TTS Engine инициализирован")
        return self._tts_engine
    
    def get_voice_recognizer(self):
        """Получение распознавателя речи"""
        if self._voice_recognizer is None:
            from mic import VoiceRecognizer, AudioProcessor, CommandRecognizer
            audio_processor = AudioProcessor()
            command_recognizer = CommandRecognizer()
            self._voice_recognizer = VoiceRecognizer(audio_processor, command_recognizer)
            self._voice_recognizer.initialize()
            logger.info("Voice Recognizer инициализирован")
        return self._voice_recognizer
    
    def get_weather_service(self):
        """Получение сервиса погоды"""
        if self._weather_service is None:
            from weather import WeatherService
            self._weather_service = WeatherService()
            logger.info("Weather Service инициализирован")
        return self._weather_service
    
    def get_ai_chat(self):
        """Получение AI чата"""
        if self._ai_chat is None:
            from ai_chat import AIChat
            self._ai_chat = AIChat()
            logger.info("AI Chat инициализирован")
        return self._ai_chat
    
    def get_reminder_manager(self):
        """Получение менеджера напоминаний"""
        if self._reminder_manager is None:
            from voices import ReminderManager
            self._reminder_manager = ReminderManager()
            logger.info("Reminder Manager инициализирован")
        return self._reminder_manager
    
    def get_character_3d(self):
        """Получение 3D персонажа"""
        if self._character_3d is None:
            from character_3d import Character3D
            self._character_3d = Character3D()
            logger.info("Character 3D инициализирован")
        return self._character_3d
    
    def cleanup(self):
        """Очистка всех ресурсов"""
        logger.info("Очистка ресурсов контейнера...")
        
        if self._tts_engine:
            self._tts_engine.cleanup()
        
        if self._voice_recognizer:
            self._voice_recognizer.cleanup()
        
        if self._reminder_manager:
            self._reminder_manager.cleanup()
        
        if self._character_3d:
            self._character_3d.cleanup()
        
        logger.info("Ресурсы очищены")


# Глобальный экземпляр контейнера
container = DependencyContainer()


if __name__ == '__main__':
    print("Dependency Injection контейнер")
    print("Доступные сервисы:")
    print("  - TTS Engine")
    print("  - Voice Recognizer")
    print("  - Weather Service")
    print("  - AI Chat")
    print("  - Reminder Manager")
    print("  - Character 3D")
