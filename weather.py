"""
Модуль для работы с погодой через OpenWeatherMap API
"""
import time
import requests
from typing import Optional, Dict
from config import logger, WEATHER_CONFIG, API_KEYS


class WeatherService:
    """Сервис для получения информации о погоде"""
    
    def __init__(self):
        self.api_key = API_KEYS['OPENWEATHER_API_KEY']
        self.base_url = WEATHER_CONFIG['BASE_URL']
        self.default_city = WEATHER_CONFIG['DEFAULT_CITY']
        self.units = WEATHER_CONFIG['UNITS']
        self.lang = WEATHER_CONFIG['LANG']
        self.cache_duration = WEATHER_CONFIG['CACHE_DURATION']
        
        # Кэш для погоды
        self._cache = {}
        self._cache_time = {}
    
    def get_weather(self, city: Optional[str] = None) -> Optional[str]:
        """
        Получение информации о погоде
        
        Args:
            city: Название города (если None, используется город по умолчанию)
            
        Returns:
            Строка с информацией о погоде или None
        """
        if not self.api_key:
            logger.warning("API ключ OpenWeatherMap не настроен")
            return "API ключ погоды не настроен. Установите OPENWEATHER_API_KEY в переменных окружения."
        
        city = city or self.default_city
        
        # Проверка кэша
        if self._is_cache_valid(city):
            logger.info(f"Использование кэшированной погоды для {city}")
            return self._cache[city]
        
        try:
            # Запрос к API
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': self.units,
                'lang': self.lang
            }
            
            logger.info(f"Запрос погоды для {city}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            weather_text = self._format_weather(data, city)
            
            # Сохранение в кэш
            self._cache[city] = weather_text
            self._cache_time[city] = time.time()
            
            return weather_text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса погоды: {e}")
            return "Не могу получить информацию о погоде. Проверьте подключение к интернету."
        except Exception as e:
            logger.error(f"Ошибка обработки погоды: {e}")
            return "Произошла ошибка при получении погоды."
    
    def _format_weather(self, data: Dict, city: str) -> str:
        """
        Форматирование данных о погоде в текст
        
        Args:
            data: Данные от API
            city: Название города
            
        Returns:
            Отформатированная строка
        """
        try:
            # Извлечение данных
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            
            # Формирование текста
            text = f"Погода в городе {city}. "
            text += f"Температура {temp:.0f} градусов. "
            text += f"Ощущается как {feels_like:.0f}. "
            text += f"{description.capitalize()}. "
            text += f"Влажность {humidity} процентов. "
            text += f"Давление {pressure} миллиметров ртутного столба. "
            text += f"Скорость ветра {wind_speed:.1f} метров в секунду."
            
            return text
            
        except KeyError as e:
            logger.error(f"Ошибка парсинга данных погоды: {e}")
            return "Не могу обработать данные о погоде."
    
    def _is_cache_valid(self, city: str) -> bool:
        """
        Проверка валидности кэша
        
        Args:
            city: Название города
            
        Returns:
            True если кэш валиден
        """
        if city not in self._cache or city not in self._cache_time:
            return False
        
        elapsed = time.time() - self._cache_time[city]
        return elapsed < self.cache_duration
    
    def get_forecast(self, city: Optional[str] = None, days: int = 3) -> Optional[str]:
        """
        Получение прогноза погоды
        
        Args:
            city: Название города
            days: Количество дней прогноза
            
        Returns:
            Строка с прогнозом или None
        """
        if not self.api_key:
            logger.warning("API ключ OpenWeatherMap не настроен")
            return "API ключ погоды не настроен."
        
        city = city or self.default_city
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': self.units,
                'lang': self.lang,
                'cnt': days * 8  # 8 записей на день (каждые 3 часа)
            }
            
            logger.info(f"Запрос прогноза для {city}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecast_text = self._format_forecast(data, city, days)
            
            return forecast_text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса прогноза: {e}")
            return "Не могу получить прогноз погоды."
        except Exception as e:
            logger.error(f"Ошибка обработки прогноза: {e}")
            return "Произошла ошибка при получении прогноза."
    
    def _format_forecast(self, data: Dict, city: str, days: int) -> str:
        """
        Форматирование прогноза погоды
        
        Args:
            data: Данные от API
            city: Название города
            days: Количество дней
            
        Returns:
            Отформатированная строка
        """
        try:
            text = f"Прогноз погоды для города {city} на {days} дня. "
            
            # Группировка по дням
            forecasts = data['list']
            current_date = None
            day_count = 0
            
            for forecast in forecasts:
                if day_count >= days:
                    break
                
                date = forecast['dt_txt'].split()[0]
                
                if date != current_date:
                    current_date = date
                    day_count += 1
                    
                    temp = forecast['main']['temp']
                    description = forecast['weather'][0]['description']
                    
                    text += f"День {day_count}: {temp:.0f} градусов, {description}. "
            
            return text
            
        except Exception as e:
            logger.error(f"Ошибка форматирования прогноза: {e}")
            return "Не могу обработать прогноз погоды."
    
    def clear_cache(self):
        """Очистка кэша"""
        self._cache.clear()
        self._cache_time.clear()
        logger.info("Кэш погоды очищен")


# Функция для обратной совместимости
def get_weather(city: Optional[str] = None) -> Optional[str]:
    """
    Получение погоды (для обратной совместимости)
    
    Args:
        city: Название города
        
    Returns:
        Информация о погоде
    """
    service = WeatherService()
    return service.get_weather(city)


if __name__ == '__main__':
    # Тестирование
    print("Тестирование модуля погоды")
    
    service = WeatherService()
    
    # Проверка наличия API ключа
    if not service.api_key:
        print("⚠️  API ключ не настроен")
        print("Установите переменную окружения OPENWEATHER_API_KEY")
    else:
        print(f"✓ API ключ настроен")
        
        # Тест получения погоды
        weather = service.get_weather()
        if weather:
            print(f"\nТекущая погода:\n{weather}")
        
        # Тест прогноза
        forecast = service.get_forecast(days=2)
        if forecast:
            print(f"\nПрогноз:\n{forecast}")
