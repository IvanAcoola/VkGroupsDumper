# Дампер групп для vk.com
Данный скрипт предназначен для сохранения информации с группы вк через токен (Участники, Руководители, Черный список, Каждый диалог с сообщениями)

## Описание

Основные модули:
  - Класс VkGroupDumper, работающий через vkapi (dumperClass.py)

Основые библиотеки:
  - vk_api
  - sqlite3

## Использование

```
dumper = dumperClass.VkGroupDumper(token)
dumper.dump_all()
```

Готовое решение для использования - main.py

## Установка

Клонируем репозиторий
```
git clone https://github.com/IvanAcoola/vkgroupsdumper.git
cd vkgroupsdumper
```
Создаем окружение и загружаем библиотеки
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Укажите в списке tokens (main.py) необходимые для работы токены

Запуск
```
python3 main.py
```

## Результат работы

В качестве результата создается sqlite база, содержащая следующие таблицы:
  - admins
  - banned
  - members
  - id(Айди собеседника) - данных таблиц создается столько, сколько диалогов

Для просмотра базы рекомендуется использовать https://sqlitestudio.pl



***Запрещается использование в вредоносных целях***
