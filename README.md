# Система опросов пользователей.

## Требование: Docker & docker-compose

## Запуск сервиса:
```shell script
docker-compose down
docker-compose build
docker-compose run --service-ports backend
```

## Endpoint'ы:
* GET /polls/active: Получение списка активных опросов
* GET /polls/users/<идентификатор_пользователя>/answers-detail: Получение пройденных пользователем опросов с детализацией по ответам
* POST /polls/answer: Ответ на вопросы (см. GET /polls/answer в браузере)