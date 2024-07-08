from http import HTTPStatus
import datetime

from django.urls import reverse
from pytest_django.asserts import assertRedirects
import pytest

from news.models import Comment, News

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)  # Получаем ссылку на нужный адрес.
    response = client.get(url)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK

@pytest.mark.django_db
def test_detail_news_availability_for_anonymous_user(client, news):
    url = reverse('news:detail', args=(news.id, ))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


<<<<<<< HEAD
@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('id_for_args')),
        ('news:delete', pytest.lazy_fixture('id_for_args')),
    ),
)
def test_pages_to_edit_delete_for_author(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK
=======
# Обозначаем, что тесту нужен доступ к БД. 
# Без этой метки тест выдаст ошибку доступа к БД.
@pytest.mark.django_db
def test_empty_db():
    news_count = News.objects.count()
    # В пустой БД никаких заметок не будет:
    assert news_count == 0 
>>>>>>> 2727f31e895430c8faf4840d1809e9a6707fa6b4


@pytest.mark.parametrize(
    'name, args',
    (
<<<<<<< HEAD
        ('news:edit', pytest.lazy_fixture('id_for_args')),
        ('news:delete', pytest.lazy_fixture('id_for_args')),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
=======
        ('news:detail', pytest.lazy_fixture('id_for_args')),
        ('news:edit', pytest.lazy_fixture('id_for_args')),
        ('news:delete', pytest.lazy_fixture('id_for_args')),
        # ('notes:add', None),
        # ('notes:success', None),
        # ('notes:list', None),
    ),
)
# Передаём в тест анонимный клиент, name проверяемых страниц и args:
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    # Теперь не надо писать никаких if и можно обойтись одним выражением.
>>>>>>> 2727f31e895430c8faf4840d1809e9a6707fa6b4
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)