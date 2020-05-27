# Система опросов пользователей.

## Требование: Docker & docker-compose

## Запуск сервиса:
```shell script
docker-compose down
docker-compose build
docker-compose run --service-ports backend
```

## Доступные запросы:
* Получение списка активных опросов: GET /polls/active
* Получение пройденных пользователем опросов с детализацией по ответам: GET /polls/users/<идентификатор_пользователя>/answers-detail
* POST /polls/answer.
    * Тело запроса (application/json):
        ```json
        {
            "text": "<Ответ в виде текста в случае, если тип вопроса: TEXT_ANSWER>",
            "choices": ["Допустимый вариант ответа (для SINGLE_ANSWER), связанный с вопросом (или их множество для SEVERAL_OPTIONS_ANSWER)"],
            "user": "Идентификатор пользователя, который отвечает на вопрос",
            "question": "Идентификатор вопроса"
        }
        ```
