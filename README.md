# API сервиса YaMDb

## Описание

Проект YaMDb собирает отзывы пользователей на произведения.Произведения делятся на категории: "Категории": "Фильмы", "Музыка". Также можно присваивать жанры произведениям, оставлять отзывы, комментировать их.

### Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории "Книги" могут быть произведения "Винни-Пух и все-все-все" и "Марсианские хроники", а в категории "Музыка" — песня "Давеча" группы "Насекомые" и вторая сюита Баха.Произведению может быть присвоен жанр из списка предустановленных (например, "Сказка", "Рок" или "Артхаус").Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

#### Доступный функционал

- Для аутентификации используются JWT-токены.
- У неаутентифицированных пользователей доступ к API только на уровне чтения.
- Создание объектов разрешено только аутентифицированным пользователям.На прочий фунционал наложено ограничение в виде административных ролей и авторства.
- Управление пользователями.
- Получение списка всех категорий и жанров, добавление и удаление.
- Получение списка всех произведений, их добавление.Получение, обновление и удаление конкретного произведения.
- Получение списка всех отзывов, их добавление.Получение, обновление и удаление конкретного отзыва.  
- Получение списка всех комментариев, их добавление.Получение, обновление и удаление конкретного комментария.
- Возможность получения подробной информации о себе и удаления своего аккаунта.
- Фильтрация по полям.

#### Документация к API доступна по адресу [http://127.0.0.1:8000/redoc/] после запуска сервера с проектом

#### Запуск проекта в dev-режиме

- Склонируйте репозиторий:  
```bash
git clone <название репозитория>
```    

#### Создайте виртуальное окружение

- Установите виртуальное окружение:  
- Linux/macOS

```bash
python3 -m venv venv
```

- Windows

```python
python -m venv venv
```


#### Активация виртуального окружения

выполните команду:
- Linux/macOS

```bash
source venv/bin/activate
```

- Windows

```bash
source venv/Scripts/activate
```

Обновите pip:
```bash
python -m pip install --upgrade pip
```
- Установите зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
- Перейдите в папку api_yamdb/api_yamdb.
- Примените миграции:   
```bash
python manage.py migrate
```
- Загрузите тестовые данные:  
```bash
python manage.py load_csv_data
```
- Выполните команду:   
```bash
python manage.py runserver
```

#### Примеры некоторых запросов API

Регистрация пользователя:  
``` POST /api/v1/auth/signup/ ```  
Получение данных своей учетной записи:  
``` GET /api/v1/users/me/ ```  
Добавление новой категории:  
``` POST /api/v1/categories/ ```  
Удаление жанра:  
``` DELETE /api/v1/genres/{slug} ```  
Частичное обновление информации о произведении:  
``` PATCH /api/v1/titles/{titles_id} ```  
Получение списка всех отзывов:  
``` GET /api/v1/titles/{title_id}/reviews/ ```   
Добавление комментария к отзыву:  
``` POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/ ```    

#### Полный список запросов API находятся в документации