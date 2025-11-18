"""
Модуль для работы с OpenRouter AI (deepseek-r1)
"""
import time
import requests
from typing import Optional, List, Dict
from config import logger, OPENROUTER_CONFIG, API_KEYS, CACHE_SETTINGS


class AIChat:
    """Класс для взаимодействия с OpenRouter AI"""
    
    def __init__(self):
        self.api_key = API_KEYS['OPENROUTER_API_KEY']
        self.base_url = OPENROUTER_CONFIG['BASE_URL']
        self.model = OPENROUTER_CONFIG['MODEL']
        self.max_tokens = OPENROUTER_CONFIG['MAX_TOKENS']
        self.temperature = OPENROUTER_CONFIG['TEMPERATURE']
        self.timeout = OPENROUTER_CONFIG['TIMEOUT']
        
        # История диалога
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 10
        
        # Кэш ответов
        self._response_cache = {}
        self._cache_max_size = CACHE_SETTINGS['AI_RESPONSE_CACHE_SIZE']
        
        # Системный промпт
        self.system_prompt = """Ты - Акира, дружелюбный голосовой ассистент. 
Отвечай кратко и по существу. Твои ответы будут озвучены, поэтому избегай длинных текстов.
Будь вежливой и полезной. Отвечай на русском языке."""
    
    def chat(self, message: str, use_history: bool = True) -> Optional[str]:
        """
        Отправка сообщения в AI и получение ответа
        
        Args:
            message: Сообщение пользователя
            use_history: Использовать ли историю диалога
            
        Returns:
            Ответ AI или None
        """
        if not self.api_key:
            logger.warning("API ключ OpenRouter не настроен")
            return "API ключ для AI не настроен. Установите OPENROUTER_API_KEY в переменных окружения."
        
        # Проверка кэша
        cache_key = message.lower().strip()
        if cache_key in self._response_cache:
            logger.info("Использование кэшированного ответа AI")
            return self._response_cache[cache_key]
        
        try:
            # Формирование сообщений
            messages = []
            
            # Системный промпт
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
            
            # История диалога
            if use_history and self.conversation_history:
                messages.extend(self.conversation_history[-self.max_history:])
            
            # Текущее сообщение
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Запрос к API
            logger.info(f"Отправка запроса к OpenRouter: {message[:50]}...")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/akira-assistant",
                "X-Title": "Akira Voice Assistant"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Извлечение ответа
            ai_response = data['choices'][0]['message']['content']
            
            # Сохранение в историю
            if use_history:
                self.conversation_history.append({
                    "role": "user",
                    "content": message
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": ai_response
                })
            
            # Сохранение в кэш
            self._add_to_cache(cache_key, ai_response)
            
            logger.info(f"Получен ответ от AI: {ai_response[:50]}...")
            return ai_response
            
        except requests.exceptions.Timeout:
            logger.error("Таймаут запроса к OpenRouter")
            return "Извините, AI не отвечает. Попробуйте позже."
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса к OpenRouter: {e}")
            return "Не могу связаться с AI. Проверьте подключение к интернету."
        except Exception as e:
            logger.error(f"Ошибка обработки ответа AI: {e}")
            return "Произошла ошибка при обработке ответа AI."
    
    def fast_dialogue(self, message: str) -> Optional[str]:
        """
        Быстрый диалог без истории (для коротких вопросов)
        
        Args:
            message: Сообщение пользователя
            
        Returns:
            Ответ AI
        """
        return self.chat(message, use_history=False)
    
    def clear_history(self):
        """Очистка истории диалога"""
        self.conversation_history.clear()
        logger.info("История диалога очищена")
    
    def _add_to_cache(self, key: str, value: str):
        """
        Добавление ответа в кэш
        
        Args:
            key: Ключ (сообщение пользователя)
            value: Значение (ответ AI)
        """
        # Ограничение размера кэша
        if len(self._response_cache) >= self._cache_max_size:
            # Удаление самого старого элемента
            oldest_key = next(iter(self._response_cache))
            del self._response_cache[oldest_key]
        
        self._response_cache[key] = value
    
    def clear_cache(self):
        """Очистка кэша ответов"""
        self._response_cache.clear()
        logger.info("Кэш ответов AI очищен")
    
    def set_system_prompt(self, prompt: str):
        """
        Установка системного промпта
        
        Args:
            prompt: Новый системный промпт
        """
        self.system_prompt = prompt
        logger.info("Системный промпт обновлен")
    
    def get_conversation_summary(self) -> str:
        """
        Получение краткого содержания диалога
        
        Returns:
            Краткое содержание
        """
        if not self.conversation_history:
            return "История диалога пуста"
        
        summary = f"В истории {len(self.conversation_history)} сообщений:\n"
        
        for i, msg in enumerate(self.conversation_history[-5:], 1):
            role = "Пользователь" if msg['role'] == 'user' else "Акира"
            content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            summary += f"{i}. {role}: {content}\n"
        
        return summary


class SmartAssistant:
    """Умный ассистент с расширенными возможностями"""
    
    def __init__(self, ai_chat: AIChat):
        self.ai_chat = ai_chat
    
    def answer_question(self, question: str) -> Optional[str]:
        """
        Ответ на вопрос с контекстом
        
        Args:
            question: Вопрос пользователя
            
        Returns:
            Ответ
        """
        # Добавление контекста к вопросу
        context = "Ответь кратко и понятно. "
        full_question = context + question
        
        return self.ai_chat.chat(full_question)
    
    def explain_concept(self, concept: str) -> Optional[str]:
        """
        Объяснение концепции
        
        Args:
            concept: Концепция для объяснения
            
        Returns:
            Объяснение
        """
        prompt = f"Объясни простыми словами за 2-3 предложения: {concept}"
        return self.ai_chat.fast_dialogue(prompt)
    
    def translate(self, text: str, target_lang: str = "английский") -> Optional[str]:
        """
        Перевод текста
        
        Args:
            text: Текст для перевода
            target_lang: Целевой язык
            
        Returns:
            Переведенный текст
        """
        prompt = f"Переведи на {target_lang}: {text}"
        return self.ai_chat.fast_dialogue(prompt)
    
    def generate_idea(self, topic: str) -> Optional[str]:
        """
        Генерация идеи по теме
        
        Args:
            topic: Тема
            
        Returns:
            Идея
        """
        prompt = f"Предложи интересную идею на тему: {topic}"
        return self.ai_chat.fast_dialogue(prompt)


# Функции для обратной совместимости
def chat_with_ai(message: str) -> Optional[str]:
    """
    Чат с AI (для обратной совместимости)
    
    Args:
        message: Сообщение
        
    Returns:
        Ответ AI
    """
    ai = AIChat()
    return ai.chat(message)


def fast_dialogue(message: str) -> Optional[str]:
    """
    Быстрый диалог (для обратной совместимости)
    
    Args:
        message: Сообщение
        
    Returns:
        Ответ AI
    """
    ai = AIChat()
    return ai.fast_dialogue(message)


if __name__ == '__main__':
    # Тестирование
    print("Тестирование модуля AI Chat")
    
    ai = AIChat()
    
    # Проверка наличия API ключа
    if not ai.api_key:
        print("⚠️  API ключ не настроен")
        print("Установите переменную окружения OPENROUTER_API_KEY")
    else:
        print(f"✓ API ключ настроен")
        print(f"✓ Модель: {ai.model}")
        
        # Тест быстрого диалога
        print("\nТест быстрого диалога:")
        response = ai.fast_dialogue("Привет! Как дела?")
        if response:
            print(f"AI: {response}")
        
        # Тест с историей
        print("\nТест с историей:")
        ai.chat("Меня зовут Иван")
        response = ai.chat("Как меня зовут?")
        if response:
            print(f"AI: {response}")
        
        # Вывод истории
        print("\n" + ai.get_conversation_summary())
