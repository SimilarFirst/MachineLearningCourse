import re
import datetime
import logging
from typing import Optional, Tuple
from config import config

logger = logging.getLogger(__name__)

def detect_question_intonation(text: str) -> bool:
    """Detect if text is a question based on punctuation and structure"""
    text = text.strip()
    if text.endswith('?'):
        return True

    # Russian question words
    question_words = ['что', 'где', 'когда', 'почему', 'зачем', 'как', 'кто', 'чей', 'какой', 'который']
    first_word = text.lower().split()[0] if text else ''
    return first_word in question_words

def parse_time_from_text(time_str: str) -> Optional[datetime.datetime]:
    """Parse time from natural language text"""
    now = datetime.datetime.now()
    time_str = time_str.lower().strip()

    # "через N минут/часов/секунд/дней"
    match = re.search(r'через (\d+) ?(минут[уы]?|час[аов]?|секунд[уы]?|дней?|дня)', time_str)
    if match:
        amount = int(match.group(1))
        unit = match.group(2)

        if 'минут' in unit:
            return now + datetime.timedelta(minutes=amount)
        elif 'час' in unit:
            return now + datetime.timedelta(hours=amount)
        elif 'секунд' in unit:
            return now + datetime.timedelta(seconds=amount)
        elif 'дн' in unit or 'дня' in unit:
            return now + datetime.timedelta(days=amount)

    # "в HH:MM"
    match = re.search(r'в (\d{1,2}):(\d{2})', time_str)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target_time <= now:
            target_time += datetime.timedelta(days=1)
        return target_time

    # "в N час"
    match = re.search(r'в (\d{1,2}) час', time_str)
    if match:
        hour = int(match.group(1))
        target_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        if target_time <= now:
            target_time += datetime.timedelta(days=1)
        return target_time

    # "завтра"
    if 'завтра' in time_str:
        tomorrow = now + datetime.timedelta(days=1)
        return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)

    # "послезавтра"
    if 'послезавтра' in time_str:
        day_after = now + datetime.timedelta(days=2)
        return day_after.replace(hour=9, minute=0, second=0, microsecond=0)

    return None

def limit_response_by_sentences(text: str, max_sentences: int = 4) -> str:
    """Limit response to maximum number of sentences"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return '. '.join(sentences[:max_sentences]) + ('.' if sentences[:max_sentences] else '')

def preprocess_text(text: str) -> str:
    """Preprocess text for recognition"""
    # Remove punctuation except for question marks
    text = re.sub(r'[^\w\s?]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def setup_logging():
    """Setup logging configuration"""
    log_file = config.LOG_DIR / f"akira_{datetime.date.today()}.log"

    logging.basicConfig(
        level=getattr(logging, config.SYSTEM_SETTINGS['LOG_LEVEL']),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def get_cursor_position() -> Tuple[int, int]:
    """Get current cursor position (Linux implementation)"""
    try:
        from Xlib import display
        d = display.Display()
        root = d.screen().root
        pointer = root.query_pointer()
        return pointer.root_x, pointer.root_y
    except ImportError:
        logger.warning("Xlib not available, cursor tracking disabled")
        return 0, 0
    except Exception as e:
        logger.error(f"Error getting cursor position: {e}")
        return 0, 0

def set_window_transparency(window, alpha: float):
    """Set window transparency (Linux implementation)"""
    try:
        # This is a placeholder - actual implementation depends on window manager
        # For compositing window managers like Compiz, Mutter, etc.
        pass
    except Exception as e:
        logger.error(f"Error setting window transparency: {e}")

def download_file(url: str, dest_path: str, desc: str = "Downloading"):
    """Download file with progress"""
    import requests
    from pathlib import Path

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        Path(dest_path).parent.mkdir(parents=True, exist_ok=True)

        with open(dest_path, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = int(50 * downloaded / total_size)
                    print(f"\r{desc}: [{'=' * progress}{' ' * (50 - progress)}] {downloaded}/{total_size}", end='', flush=True)
                print()  # New line after progress

        return True
    except Exception as e:
        logger.error(f"Error downloading {url}: {e}")
        return False