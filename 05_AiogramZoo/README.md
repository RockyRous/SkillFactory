# Телеграм-Бот Московского зоопарка

Telegram-бот для популяризации программы опеки животных Московского зоопарка на основе викторины.

Инструкция по запуску бота с предоставленным токеном:

```
>> Запустить комманду "pip install -r requirements.txt" в предварительно созданной виртуальной среде.
>> В файле config.py можете установить свой АПИ-ключ телеграма, а также выключить режим дебага.
>> Запустить файл main.py 
>> Перейти @MoyZanudaBot в Telegram и начать разговор
```

## Функционал

* Предоставление информации о программе опеки Московского зоопарка
* Проведение викторины на тему "Твое тотемное животное" с выводом вопроса в тексте и вариантов ответа на клавиатуре.
* Подсчет и вывод результата на основе ответов пользователя, включая изображение животного, его наименование, описание.
* Передача контактов ответственного лица при возникновении вопросов
* Возможность оставить обратную связь внутри чата с ботом

> Источник информации о животных: https://moscowzoo.ru/animals/

## Описание викторины

* Викторина проходит в несколько этапов. 
* Сначала определяется какая группа животных больше подходит юзеру, потом определяется само животное из группы.
* На каждом этапе свои вопросы, которые регулируют рейтинг по отношению к каждой группе\животному.
* По завершению викторины выбирается результат с высшим рейтингом.
* Пользователю выводиться статистика его ответов (сколько балов у каждой группы)

