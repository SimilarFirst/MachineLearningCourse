import os
from pathlib import Path

# Configuration settings for Akira Virtual Assistant

# Paths
PROJECT_ROOT = Path(__file__).parent
MODELS_DIR = PROJECT_ROOT / "models"
VOSK_MODEL_DIR = MODELS_DIR / "vosk_small"
SILERO_MODELS_DIR = MODELS_DIR / "silero_models" / "ru"
TEMP_DIR = PROJECT_ROOT / "temporary_files"
LOG_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
for dir_path in [MODELS_DIR, VOSK_MODEL_DIR, SILERO_MODELS_DIR, TEMP_DIR, LOG_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Audio settings
AUDIO_SETTINGS = {
    'CHUNK_SIZE': 1024,
    'FORMAT': 'int16',
    'CHANNELS': 1,
    'RATE': 16000
}

# Recognition settings
RECOGNITION_SETTINGS = {
    'VOICE_ACTIVATION_THRESHOLD': 0.01,
    'CONFIDENCE_THRESHOLD': 0.7,
    'MIN_PHRASE_LENGTH': 3,
    'MAX_SILENCE_DURATION': 1.0
}

# TTS settings
TTS_SETTINGS = {
    'RU_SPEAKER': 'kseniya',
    'EN_SPEAKER': 'en_6',
    'SAMPLE_RATE': 48000,
    'SPEED': 1.1,
    'PITCH_SHIFT_QUESTION': 1.05
}

# API Keys (set via environment variables)
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
DEFAULT_CITY = os.getenv('DEFAULT_CITY', 'Moscow')

# OpenRouter settings
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "deepseek/deepseek-r1"

# Window settings
WINDOW_SETTINGS = {
    'WIDTH': 400,
    'HEIGHT': 600,
    'TRANSPARENCY': 0.8,
    'ALWAYS_ON_TOP': True
}

# Character settings
CHARACTER_SETTINGS = {
    'MODEL_PATH': PROJECT_ROOT / "untitled.glb",
    'CURSOR_FOLLOW_SPEED': 0.05,
    'JUMP_DISTANCE': 100,
    'SLEEP_TIMEOUT': 300  # seconds
}

# System settings
SYSTEM_SETTINGS = {
    'MIC_ENABLED': int(os.getenv('MIC', '1')),
    'SPEECH_ENABLED': int(os.getenv('SPEECH_ENABLED', '1')),
    'CHATGPT_ENABLED': int(os.getenv('CHATGPT', '0')),
    'SPEECH_CONTROL': int(os.getenv('SPEECH_CONTROL', '0')),
    'RESPONSE_PRIORITY': int(os.getenv('RESPONSE_PRIORITY', '4')),
    'LOG_LEVEL': 'INFO'
}

# Cache settings
CACHE_SETTINGS = {
    'WEATHER_CACHE_DURATION': 600,  # 10 minutes
    'AI_RESPONSE_CACHE_SIZE': 100,
    'TTS_AUDIO_CACHE_SIZE': 50
}

# Hotkeys
HOTKEYS = {
    'TOGGLE_MIC': '<ctrl>+<alt>+m',
    'TOGGLE_SPEECH': '<ctrl>+<alt>+s',
    'SLEEP_MODE': '<ctrl>+<alt>+z'
}

# Language settings
LANGUAGE = os.getenv('LANGUAGE', 'ru')  # 'ru' or 'en'