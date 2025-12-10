# Project "course_1"

## Описание:

Проект course_1 - это приложение на Python.

## О проекте

Создание приложения с выводом курса валюты, обработка XL и вывод json.
Разработан на IDE PyCharm 2025.2.5

## Шаги установки:

1. Как клонировать проект
````
clone https://github.com/gdeunas/course_1.git
cd course_1
````
2. Настройте виртуальное окружение и установите зависимости:
````
python -m venv env
source env/bin/activate  # Linux/MacOS
env\Scripts\activate     # Windows
````
Для dev:
````
poetry add isort
poetry add mypy
poetry add flake8
poetry add black
````
3. Создайте файл настроек окружения:
````
cp .env.example .env
````
## Как запустить проект
````
python3 src/main.py
````
## Об API

1. Переименовать файл ".env.example" в ".env" 
2. Внести свои параметры API

Пример:
````
import requests
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo
r = requests.get(url)
data = r.json()
print(data)
````

## Создать html файлы с покрытием
````
pytest --cov=src --cov-report=html 
````
Создаться папка htmlcov с покрытием.

## Задание

Реализуйте на выбор минимум одну из задач в каждой категории.

Используйте материалы по декомпозиции задачи, которую вы делали на предыдущем курсе.

При работе над задачей ориентируйтесь на теги, расставленные перед каждым заданием. Например:
````
#json #requests #API #datetime #logging #pytest #pandas
````
Вы можете выполнить несколько задач или выбрать задачу посложнее. Курсовая — это дополнительная возможность попрактиковаться в западающих темах под руководством наставника.

Задачи по категориям:
Веб-страницы:
````
Главная
События

Сервисы:
Выгодные категории повышенного кешбэка

Отчеты:
Траты по категории
````
## Пример структуры проекта
````
.
├── src
│ ├── __init__.py
│ ├── utils.py
│ ├── main.py
│ ├── views.py
│ ├── reports.py
│ └── services.py
├── data
│ ├── operations.xlsx
├── tests
│ ├── __init__.py
│ ├── test_utils.py
│ ├── test_views.py
│ ├── test_reports.py
│ └── test_services.py
├── user_settings.json
├── .venv/
├── .env
├── .env_template
├── .git/
├── .idea/
├── .flake8
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md
````

## Документация:

Для получения дополнительной информации обратитесь к [документации] (docs/README.md).

## Лицензия:

Этот проект лицензирован по [лицензии MIT] (LICENSE).