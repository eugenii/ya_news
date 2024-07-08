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


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('id_for_args')),
        ('news:delete', pytest.lazy_fixture('id_for_args')),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


# # ====================================================================================
# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     'name, args',
#     (
#         ('news:edit', pytest.lazy_fixture('id_for_args')),
#         ('news:delete', pytest.lazy_fixture('id_for_args')),
#     ),
# )
# def test_foreign_pages_to_edit_delete_for_author(author_client, not_author, name, args):
#     # comm = comment(not_author, news)
#     url = reverse(name, args=args)
#     response = author_client.get(url)
#     assert response.status_code == HTTPStatus.NOT_FOUND


#     # ============================
#     @pytest.fixture 
#     def comment(): 
#         return Comment.objects.create(text="Комментарий", user=user)
# # Тест проверяет доступность страницы def test_comment_id(comment): ids = comment.id assert ids == 1