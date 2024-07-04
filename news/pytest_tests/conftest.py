import datetime

import pytest

# Импортируем класс клиента.
from django.test.client import Client

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import Comment, News


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):  
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(  # Создаём объект новости.
        title='Заголовок',
        text='Текст новости',
        date=datetime.datetime.today
    )
    return news

@pytest.fixture
def comment(author):
    comment = Comment.objects.create(  # Создаём объект новости.
        author=author,
        news=news,
        text='Комментарий',
    )
    return comment


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания новости.
def id_for_args(news):  
    # И возвращает кортеж, который содержит id новости.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (news.id,)
