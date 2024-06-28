import logging
import ecs_logging
import time
from random import randint
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(current_dir, 'log.json')

# Инициализация логгера
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file)
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)

def log_message(method, message, file_name=None):
    """
    Функция для вызова метода логгера.

    Args:
        method: Метод логгера (info, warning, error, critical).
        message: Сообщение для записи в лог.
        file_name: Имя файла, которое нужно добавить в лог.
    """

    # Получение атрибута метода логгера по имени
    log_method = getattr(logger, method)

    # Формирование сообщения с информацией о времени и файле
    log_message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    if file_name:
        log_message += f" (файл: {file_name})"
    
    # Вызов метода логгера
    log_method(message, extra={"http.request.body.content": message})
