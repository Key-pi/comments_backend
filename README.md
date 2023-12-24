


## Поднятие проекта

1. Запустите файл:

    ```bash
    sh setup_project
    ```

2. Вы можете указать переменные в файле `.env`:

    ```env
    EMAIL_HOST_USER=Your@Gmail
    EMAIL_HOST_PASSWORD=YourPassword
    ```

   Если указаны эти переменные, письма будут отправляться от вашей почты. В противном случае сообщения будут выводиться в консоль.

3. Запустите команду:

    ```bash
    docker-compose build
    ```

4. Запустите проект:

    ```bash
    docker-compose up
    ```

5. Войдите в контейнер бекенда:

    ```bash
    docker-compose exec backend bash
    ```

6. Выполните команды:

    ```bash
    python manage.py migrate
    python manage.py collectstatic
    python manage.py createsuperuser
    ```
7. Переходите по ссылке: http://0.0.0.0:8001/api/docs/#/

## Функционал

1. Queue
2. Cache
3. Events
4. JWT
5. Localization (admin panel too)
6. Pagination
7. Swagger

Комментарии могут создавать как авторизованные, так и неавторизованные пользователи. Для авторизованного пользователя поле "email" заполнять не обязательно.

## Получение пароля приложения Google

1. Зайдите в свою учетную запись Google: [https://myaccount.google.com/](https://myaccount.google.com/)
2. Перейдите в раздел "Безопасность".
3. В поиске найдите "Пароли приложений".
4. Введите название своего приложения (например, "djangotest") и выберите "Создать".
5. Вам будет предоставлен сгенерированный пароль приложения.
6. Скопируйте его без пробелов и используйте в `EMAIL_HOST_PASSWORD`.