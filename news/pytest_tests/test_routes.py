from http import HTTPStatus

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
# Указываем имя изменяемого параметра в сигнатуре теста.
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)  # Получаем ссылку на нужный адрес.
    response = client.get(url)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK


# @pytest.mark.parametrize(
#     'name',
#     ('notes:list', 'notes:add', 'notes:success')
# )
# def test_pages_availability_for_auth_user(not_author_client, name):
#     url = reverse(name)
#     response = not_author_client.get(url)
#     assert response.status_code == HTTPStatus.OK 

# Два нижних теста не нужны - просто для иллюстрации и на всякий случай..
# def test_note_exists(note):
#     notes_count = Note.objects.count()
#     # Общее количество заметок в БД равно 1.
#     assert notes_count == 1
#     # Заголовок объекта, полученного при помощи фикстуры note,
#     # совпадает с тем, что указан в фикстуре.
#     assert note.title == 'Заголовок'


# # Обозначаем, что тесту нужен доступ к БД. 
# # Без этой метки тест выдаст ошибку доступа к БД.
# @pytest.mark.django_db
# def test_empty_db():
#     notes_count = Note.objects.count()
#     # В пустой БД никаких заметок не будет:
#     assert notes_count == 0 

# @pytest.mark.parametrize(
#     'parametrized_client, expected_status',
#     # Предварительно оборачиваем имена фикстур 
#     # в вызов функции pytest.lazy_fixture().
#     (
#         (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
#         (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
#     ),
# )
# @pytest.mark.parametrize(
#     'name',
#     ('news:edit', 'news:delete'),
# )
# def test_pages_availability_for_different_users(
#         parametrized_client, name, news, expected_status
# ):
#     url = reverse(name, args=(news.id,))
#     response = parametrized_client.get(url)
#     assert response.status_code == expected_status

# @pytest.mark.parametrize(
#     'name, args',
#     (
#         ('news:detail', pytest.lazy_fixture('id_for_args')),
#         ('news:edit', pytest.lazy_fixture('id_for_args')),
#         ('news:delete', pytest.lazy_fixture('id_for_args')),
#         # ('notes:add', None),
#         # ('notes:success', None),
#         # ('notes:list', None),
#     ),
# )
# # Передаём в тест анонимный клиент, name проверяемых страниц и args:
# def test_redirects(client, name, args):
#     login_url = reverse('users:login')
#     # Теперь не надо писать никаких if и можно обойтись одним выражением.
#     url = reverse(name, args=args)
#     expected_url = f'{login_url}?next={url}'
#     response = client.get(url)
#     assertRedirects(response, expected_url)