Задача 1 - Схема
================

См. схему (PNG)

Задача 2
========

Реализация в рамках схемы 1:
1. Чтение сырах данных (Raw data + RMQ publisher) - настраивается reader с поддержкой retry policy.
2. Data "normalization" - актуализация данных, приведение к общему (стандартному) формату данных (кривых).
3. OLAP-хранилице - хранение проихводных величин (в т.ч. изменений) - Intraday/EOD Analysis service.
4. Telegram bot: Доступ к OLAP database через Data Gateway API для получения данных всех видов.


Задача 3 - запуск приложения
============================

1. Активровать venv

source ./venv/bin/activate

2. Запуск

python3 manage.py start


Описание
========

Загрузка данных:
модуль apps/scrapers/ats/scraper.py 

Скрипт создания таблицы (генерирован на основе модели): 
ats001.sql

Модель:
apps/scrapers/ats/models.py


