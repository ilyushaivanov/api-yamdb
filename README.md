# api_yamdb
api_yamdb

## Описание проекта

Проект YaMDb собирает отзывы пользователей на произведения.


### Как запустить проект:

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Стек технологий:

Django-Rest-Framework
```

PostMan
```


## Наполнение БД:

python manage.py import_csv  

## Как открыть доку:

По адресу http://127.0.0.1:8000/redoc/ к нему подключена документация.


## Пример запросов/ответов:

Запрос: 

http://127.0.0.1:8000/api/v1/auth/signup/

Ответ:

{
  "email": "{{userEmail}}",
  "username": "{{adminUsername}}"
}

Запрос: 

http://127.0.0.1:8000/api/v1/genres/

Ответ:

{
  "name": "anon-genre",
  "slug": "anon-genre-slug"
}

Запрос: 

http://127.0.0.1:8000/api/v1/titles/

Ответ:

{
    "nema": "Unauthorized user title",
    "year": 2020,
    "description": "No description",
    "genre": [
        "{{adminGenre}}"
    ],
    "category": "{{adminCategory}}"
}



## Авторство:

https://github.com/ilyushaivanov

https://github.com/Zxcuwuu

https://github.com/VitalyVodoleikin
