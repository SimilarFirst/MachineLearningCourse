"""
Вспомогательные функции для приложения Акира
"""
import re
import datetime
import time
import os
import zipfile
import requests
from pathlib import Path
from typing import Optional, List, Tuple
from config import logger, MODEL_URLS, PATHS


def detect_question_intonation(text: str) -> bool:
    """
    Определение вопросительной интонации в тексте
    
    Args:
        text: Текст для анализа
        
    Returns:
        True если текст является вопросом
    """
    # Проверка на вопросительный знак
    if '?' in text:
        return True
    
    # Вопросительные слова
    question_words = [
        'что', 'где', 'когда', 'почему', 'зачем', 'как', 'какой', 'какая', 'какое', 'какие',
        'кто', 'чей', 'чья', 'чьё', 'чьи', 'сколько', 'который', 'которая', 'которое', 'которые'
    ]
    
    text_lower = text.lower()
    words = text_lower.split()
    
    # Проверка первого слова
    if words and words[0] in question_words:
        return True
    
    # Проверка наличия вопросительных слов в начале предложения
    for word in words[:3]:
        if word in question_words:
            return True
    
    return False


def parse_time_from_text(text: str) -> Optional[datetime.datetime]:
    """
    Извлечение времени из текста
    
    Args:
        text: Текст с указанием времени
        
    Returns:
        Объект datetime или None
    """
    now = datetime.datetime.now()
    
    # Через N минут/часов/дней
    relative_match = re.search(r'через\s+(\d+)\s*(минут[уы]?|час[аов]?|секунд[уы]?|дней?|дня)', text, re.IGNORECASE)
    if relative_match:
        amount = int(relative_match.group(1))
        unit = relative_match.group(2).lower()
        
        if 'секунд' in unit:
            return now + datetime.timedelta(seconds=amount)
        elif 'минут' in unit:
            return now + datetime.timedelta(minutes=amount)
        elif 'час' in unit:
            return now + datetime.timedelta(hours=amount)
        elif 'д' in unit:
            return now + datetime.timedelta(days=amount)
    
    # В HH:MM
    time_match = re.search(r'в\s+(\d{1,2}):(\d{2})', text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))
        
        if 0 <= hour < 24 and 0 <= minute < 60:
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Если время уже прошло сегодня, устанавливаем на завтра
            if target_time <= now:
                target_time += datetime.timedelta(days=1)
            
            return target_time
    
    # В N часов
    hour_match = re.search(r'в\s+(\d{1,2})\s+час', text, re.IGNORECASE)
    if hour_match:
        hour = int(hour_match.group(1))
        
        if 0 <= hour < 24:
            target_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            if target_time <= now:
                target_time += datetime.timedelta(days=1)
            
            return target_time
    
    # Завтра
    if 'завтра' in text.lower():
        return now + datetime.timedelta(days=1)
    
    # Послезавтра
    if 'послезавтра' in text.lower():
        return now + datetime.timedelta(days=2)
    
    return None


def limit_response_by_sentences(text: str, max_sentences: int = 4) -> str:
    """
    Ограничение ответа по количеству предложений
    
    Args:
        text: Исходный текст
        max_sentences: Максимальное количество предложений
        
    Returns:
        Обрезанный текст
    """
    if not text:
        return ""
    
    # Разделение на предложения
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= max_sentences:
        return text
    
    # Возвращаем первые N предложений
    result = '. '.join(sentences[:max_sentences])
    if not result.endswith('.'):
        result += '.'
    
    return result


def download_file(url: str, destination: Path, chunk_size: int = 8192) -> bool:
    """
    Загрузка файла с прогресс-баром
    
    Args:
        url: URL файла
        destination: Путь для сохранения
        chunk_size: Размер чанка для загрузки
        
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Загрузка {url}...")
        
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\rПрогресс: {progress:.1f}%", end='', flush=True)
        
        print()  # Новая строка после прогресс-бара
        logger.info(f"Файл загружен: {destination}")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка загрузки файла: {e}")
        return False


def extract_zip(zip_path: Path, extract_to: Path) -> bool:
    """
    Извлечение ZIP архива
    
    Args:
        zip_path: Путь к ZIP файлу
        extract_to: Путь для извлечения
        
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Извлечение {zip_path}...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        logger.info(f"Архив извлечен в {extract_to}")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка извлечения архива: {e}")
        return False


def download_vosk_model() -> bool:
    """
    Загрузка модели Vosk если её нет
    
    Returns:
        True если модель доступна
    """
    vosk_dir = Path(PATHS['VOSK_MODEL'])
    
    # Проверка наличия модели
    if vosk_dir.exists() and any(vosk_dir.iterdir()):
        logger.info("Модель Vosk уже загружена")
        return True
    
    logger.info("Модель Vosk не найдена, начинаю загрузку...")
    
    # Загрузка модели
    temp_zip = Path(PATHS['TEMP_FILES']) / 'vosk_model.zip'
    
    if not download_file(MODEL_URLS['VOSK_SMALL_RU'], temp_zip):
        return False
    
    # Извлечение
    temp_extract = Path(PATHS['TEMP_FILES']) / 'vosk_extract'
    if not extract_zip(temp_zip, temp_extract):
        return False
    
    # Перемещение в нужную директорию
    extracted_dirs = list(temp_extract.iterdir())
    if extracted_dirs:
        extracted_model = extracted_dirs[0]
        
        # Копирование файлов
        import shutil
        if vosk_dir.exists():
            shutil.rmtree(vosk_dir)
        shutil.move(str(extracted_model), str(vosk_dir))
        
        logger.info("Модель Vosk успешно установлена")
    
    # Очистка временных файлов
    try:
        temp_zip.unlink()
        shutil.rmtree(temp_extract)
    except Exception:
        pass
    
    return True


def ensure_silero_models() -> bool:
    """
    Проверка и загрузка моделей Silero
    
    Returns:
        True если модели доступны
    """
    try:
        import torch
        
        # Модели загружаются автоматически через torch.hub
        logger.info("Проверка моделей Silero TTS...")
        
        # Попытка загрузки модели (она кэшируется автоматически)
        model, _ = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language='ru',
            speaker='v3_1_ru'
        )
        
        logger.info("Модели Silero TTS доступны")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка загрузки моделей Silero: {e}")
        return False


def format_time_delta(seconds: int) -> str:
    """
    Форматирование временного интервала в читаемый вид
    
    Args:
        seconds: Количество секунд
        
    Returns:
        Отформатированная строка
    """
    if seconds < 60:
        return f"{seconds} сек"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} мин"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} ч"
    else:
        days = seconds // 86400
        return f"{days} дн"


def sanitize_filename(filename: str) -> str:
    """
    Очистка имени файла от недопустимых символов
    
    Args:
        filename: Исходное имя файла
        
    Returns:
        Очищенное имя файла
    """
    # Удаление недопустимых символов
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Ограничение длины
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename


def get_system_info() -> dict:
    """
    Получение информации о системе
    
    Returns:
        Словарь с информацией о системе
    """
    try:
        import psutil
        import platform
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'cpu_percent': cpu_percent,
            'memory_total': memory.total,
            'memory_available': memory.available,
            'memory_percent': memory.percent,
            'disk_total': disk.total,
            'disk_used': disk.used,
            'disk_percent': disk.percent
        }
    except Exception as e:
        logger.error(f"Ошибка получения информации о системе: {e}")
        return {}


def interpolate(start: float, end: float, t: float) -> float:
    """
    Линейная интерполяция
    
    Args:
        start: Начальное значение
        end: Конечное значение
        t: Коэффициент интерполяции (0-1)
        
    Returns:
        Интерполированное значение
    """
    return start + (end - start) * t


def ease_in_out(t: float) -> float:
    """
    Функция плавности (ease-in-out)
    
    Args:
        t: Значение от 0 до 1
        
    Returns:
        Сглаженное значение
    """
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - pow(-2 * t + 2, 2) / 2


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Ограничение значения в диапазоне
    
    Args:
        value: Значение
        min_value: Минимум
        max_value: Максимум
        
    Returns:
        Ограниченное значение
    """
    return max(min_value, min(value, max_value))


# Инициализация при импорте
def initialize_models():
    """Инициализация всех необходимых моделей"""
    logger.info("Инициализация моделей...")
    
    # Загрузка Vosk
    if not download_vosk_model():
        logger.warning("Не удалось загрузить модель Vosk")
    
    # Проверка Silero
    if not ensure_silero_models():
        logger.warning("Не удалось загрузить модели Silero")
    
    logger.info("Инициализация моделей завершена")


if __name__ == '__main__':
    # Тестирование функций
    print("Тестирование utils.py")
    
    # Тест определения вопроса
    test_questions = [
        "Какая погода?",
        "Где мои ключи",
        "Это утверждение",
        "Почему небо голубое?"
    ]
    
    for q in test_questions:
        is_question = detect_question_intonation(q)
        print(f"'{q}' -> Вопрос: {is_question}")
    
    # Тест парсинга времени
    test_times = [
        "через 5 минут",
        "в 15:30",
        "завтра",
        "через 2 часа"
    ]
    
    for t in test_times:
        parsed = parse_time_from_text(t)
        print(f"'{t}' -> {parsed}")
    
    # Тест ограничения предложений
    long_text = "Первое предложение. Второе предложение. Третье предложение. Четвертое предложение. Пятое предложение."
    limited = limit_response_by_sentences(long_text, 3)
    print(f"Ограничено: {limited}")
