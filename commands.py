"""
Обработчики команд для голосового ассистента Акира
"""
import os
import sys
import subprocess
import webbrowser
import platform
from typing import Optional
from config import logger
import words


def search_web(query: str = ""):
    """Поиск в интернете"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        if not query:
            tts.speak("Что найти?")
            return
        
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        tts.speak(f"Ищу {query}")
        logger.info(f"Поиск в интернете: {query}")
    except Exception as e:
        logger.error(f"Ошибка поиска в интернете: {e}")


def weather():
    """Получение информации о погоде"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        weather_service = container.get_weather_service()
        tts = container.get_tts_engine()
        
        weather_info = weather_service.get_weather()
        if weather_info:
            tts.speak(weather_info)
        else:
            tts.speak("Не могу получить информацию о погоде")
    except Exception as e:
        logger.error(f"Ошибка получения погоды: {e}")


def open_program(program_name: str = ""):
    """Запуск программы"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        if not program_name:
            tts.speak("Какую программу открыть?")
            return
        
        program_name_lower = program_name.lower()
        system = platform.system()
        
        # Поиск программы в словаре
        program_path = None
        for prog, aliases in words.PROGRAMS.items():
            if any(alias in program_name_lower for alias in aliases):
                program_path = prog
                break
        
        if not program_path:
            program_path = program_name
        
        # Запуск в зависимости от ОС
        if system == "Windows":
            os.startfile(program_path)
        elif system == "Darwin":  # macOS
            subprocess.Popen(['open', '-a', program_path])
        else:  # Linux
            subprocess.Popen([program_path])
        
        tts.speak(f"Запускаю {program_name}")
        logger.info(f"Запуск программы: {program_name}")
    except Exception as e:
        logger.error(f"Ошибка запуска программы {program_name}: {e}")
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        tts.speak(f"Не могу запустить {program_name}")


def browser(url: str = ""):
    """Открытие браузера"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        if not url:
            url = words.WEBSITES.get('youtube', 'https://www.youtube.com')
        
        webbrowser.open(url)
        tts.speak("Открываю браузер")
        logger.info(f"Открытие браузера: {url}")
    except Exception as e:
        logger.error(f"Ошибка открытия браузера: {e}")


def game(game_name: str = ""):
    """Запуск игры"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        if not game_name:
            tts.speak("Какую игру запустить?")
            return
        
        game_name_lower = game_name.lower()
        
        # Поиск игры в словаре
        for game, aliases in words.GAMES.items():
            if any(alias in game_name_lower for alias in aliases):
                open_program(game)
                return
        
        tts.speak(f"Игра {game_name} не найдена")
        logger.warning(f"Игра не найдена: {game_name}")
    except Exception as e:
        logger.error(f"Ошибка запуска игры: {e}")


def yandex_music():
    """Запуск Яндекс Музыки"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        url = "https://music.yandex.ru"
        webbrowser.open(url)
        tts.speak("Запускаю Яндекс Музыку")
        logger.info("Запуск Яндекс Музыки")
    except Exception as e:
        logger.error(f"Ошибка запуска Яндекс Музыки: {e}")


def music_play():
    """Воспроизведение музыки"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        # Эмуляция нажатия клавиши Play/Pause
        system = platform.system()
        if system == "Windows":
            try:
                from pynput.keyboard import Key, Controller
                keyboard = Controller()
                keyboard.press(Key.media_play_pause)
                keyboard.release(Key.media_play_pause)
            except Exception:
                pass
        
        tts.speak("Включаю воспроизведение")
        logger.info("Воспроизведение музыки")
    except Exception as e:
        logger.error(f"Ошибка воспроизведения: {e}")


def music_pause():
    """Пауза музыки"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        system = platform.system()
        if system == "Windows":
            try:
                from pynput.keyboard import Key, Controller
                keyboard = Controller()
                keyboard.press(Key.media_play_pause)
                keyboard.release(Key.media_play_pause)
            except Exception:
                pass
        
        tts.speak("Ставлю на паузу")
        logger.info("Пауза музыки")
    except Exception as e:
        logger.error(f"Ошибка паузы: {e}")


def music_stop():
    """Остановка музыки"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        system = platform.system()
        if system == "Windows":
            try:
                from pynput.keyboard import Key, Controller
                keyboard = Controller()
                keyboard.press(Key.media_stop)
                keyboard.release(Key.media_stop)
            except Exception:
                pass
        
        tts.speak("Останавливаю музыку")
        logger.info("Остановка музыки")
    except Exception as e:
        logger.error(f"Ошибка остановки: {e}")


def music_next():
    """Следующий трек"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        system = platform.system()
        if system == "Windows":
            try:
                from pynput.keyboard import Key, Controller
                keyboard = Controller()
                keyboard.press(Key.media_next)
                keyboard.release(Key.media_next)
            except Exception:
                pass
        
        tts.speak("Следующий трек")
        logger.info("Следующий трек")
    except Exception as e:
        logger.error(f"Ошибка переключения трека: {e}")


def music_previous():
    """Предыдущий трек"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        system = platform.system()
        if system == "Windows":
            try:
                from pynput.keyboard import Key, Controller
                keyboard = Controller()
                keyboard.press(Key.media_previous)
                keyboard.release(Key.media_previous)
            except Exception:
                pass
        
        tts.speak("Предыдущий трек")
        logger.info("Предыдущий трек")
    except Exception as e:
        logger.error(f"Ошибка переключения трека: {e}")


def volume_up():
    """Увеличение громкости"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        system = platform.system()
        if system == "Windows":
            try:
                from pynput.keyboard import Key, Controller
                keyboard = Controller()
                for _ in range(2):
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)
            except Exception:
                pass
        
        tts.speak("Увеличиваю громкость")
        logger.info("Увеличение громкости")
    except Exception as e:
        logger.error(f"Ошибка увеличения громкости: {e}")


def volume_down():
    """Уменьшение громкости"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        system = platform.system()
        if system == "Windows":
            try:
                from pynput.keyboard import Key, Controller
                keyboard = Controller()
                for _ in range(2):
                    keyboard.press(Key.media_volume_down)
                    keyboard.release(Key.media_volume_down)
            except Exception:
                pass
        
        tts.speak("Уменьшаю громкость")
        logger.info("Уменьшение громкости")
    except Exception as e:
        logger.error(f"Ошибка уменьшения громкости: {e}")


def offpc():
    """Выключение компьютера"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        tts.speak("Выключаю компьютер через 60 секунд. Скажите отмена для отмены.")
        logger.warning("Запланировано выключение компьютера")
        
        system = platform.system()
        if system == "Windows":
            os.system("shutdown /s /t 60")
        elif system == "Linux":
            os.system("shutdown -h +1")
        elif system == "Darwin":
            os.system("sudo shutdown -h +1")
    except Exception as e:
        logger.error(f"Ошибка выключения: {e}")


def cancel_shutdown():
    """Отмена выключения"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        system = platform.system()
        if system == "Windows":
            os.system("shutdown /a")
        elif system in ["Linux", "Darwin"]:
            os.system("shutdown -c")
        
        tts.speak("Выключение отменено")
        logger.info("Выключение отменено")
    except Exception as e:
        logger.error(f"Ошибка отмены выключения: {e}")


def system_info():
    """Информация о системе"""
    try:
        from dependency_injector import DependencyContainer
        from utils import get_system_info
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        info = get_system_info()
        if info:
            cpu = info.get('cpu_percent', 0)
            memory = info.get('memory_percent', 0)
            disk = info.get('disk_percent', 0)
            
            message = f"Загрузка процессора {cpu:.0f} процентов. "
            message += f"Использование памяти {memory:.0f} процентов. "
            message += f"Занято диска {disk:.0f} процентов."
            
            tts.speak(message)
            logger.info(f"Системная информация: CPU={cpu}%, RAM={memory}%, Disk={disk}%")
        else:
            tts.speak("Не могу получить информацию о системе")
    except Exception as e:
        logger.error(f"Ошибка получения системной информации: {e}")


def find_file(filename: str = ""):
    """Поиск файла"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        if not filename:
            tts.speak("Какой файл найти?")
            return
        
        tts.speak(f"Ищу файл {filename}")
        logger.info(f"Поиск файла: {filename}")
        
        # Здесь можно добавить реальный поиск файлов
        tts.speak("Функция поиска файлов в разработке")
    except Exception as e:
        logger.error(f"Ошибка поиска файла: {e}")


def clean_disk():
    """Очистка диска"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        tts.speak("Очищаю временные файлы")
        logger.info("Очистка диска")
        
        system = platform.system()
        if system == "Windows":
            os.system("cleanmgr")
        
        tts.speak("Очистка завершена")
    except Exception as e:
        logger.error(f"Ошибка очистки диска: {e}")


def set_reminder(text: str = ""):
    """Установка напоминания"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        reminder_manager = container.get_reminder_manager()
        
        if text:
            reminder_manager.set_reminder_from_text(text)
        else:
            tts = container.get_tts_engine()
            tts.speak("О чем напомнить?")
    except Exception as e:
        logger.error(f"Ошибка установки напоминания: {e}")


def list_reminders():
    """Список напоминаний"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        reminder_manager = container.get_reminder_manager()
        reminder_manager.speak_reminders()
    except Exception as e:
        logger.error(f"Ошибка получения списка напоминаний: {e}")


def sleep_mode():
    """Переход в спящий режим"""
    try:
        from dependency_injector import DependencyContainer
        from config import update_flag
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        tts.speak("Перехожу в спящий режим")
        update_flag('MIC', 0)
        logger.info("Переход в спящий режим")
    except Exception as e:
        logger.error(f"Ошибка перехода в спящий режим: {e}")


def wake_up():
    """Пробуждение из спящего режима"""
    try:
        from dependency_injector import DependencyContainer
        from config import update_flag
        container = DependencyContainer()
        tts = container.get_tts_engine()
        
        update_flag('MIC', 1)
        tts.speak("Я проснулся!")
        logger.info("Пробуждение из спящего режима")
    except Exception as e:
        logger.error(f"Ошибка пробуждения: {e}")


def repeat_last():
    """Повтор последнего сообщения"""
    try:
        from dependency_injector import DependencyContainer
        container = DependencyContainer()
        tts = container.get_tts_engine()
        tts.repeat_last()
        logger.info("Повтор последнего сообщения")
    except Exception as e:
        logger.error(f"Ошибка повтора: {e}")


def passed():
    """Заглушка для команд без действия"""
    pass


if __name__ == '__main__':
    print("Модуль команд загружен")
    print("Доступные команды:")
    
    # Получение всех функций модуля
    import inspect
    functions = [name for name, obj in inspect.getmembers(sys.modules[__name__]) 
                 if inspect.isfunction(obj) and not name.startswith('_')]
    
    for func in functions:
        print(f"  - {func}")
