from http import HTTPStatus

from django.urls import reverse
from django.conf import settings
from pytest_django.asserts import assertRedirects, assertFormError
import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News

pytestmark = pytest.mark.django_db

COMMENT_TEXT = "Комментарий"

FORM_DATA = {
    'text': COMMENT_TEXT
}

NEW_COMMENT_TEXT = "Новый текст комментария"


def test_anonymous_user_can_create_comment(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
    # предварительно подготовленные данные формы с текстом комментария.     
    author_client.post(url, data=FORM_DATA)
    # Считаем количество комментариев.
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_user_cant_use_bad_words(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    # Формируем данные для отправки формы; текст включает
    # первое слово из списка стоп-слов.
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    # Отправляем запрос через авторизованный клиент.
    response = author_client.post(url, data=bad_words_data)
    # Проверяем, есть ли в ответе ошибка формы.
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    # Дополнительно убедимся, что комментарий не был создан.
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, news, comment):
    news_url = reverse('news:detail', args=(news.id,))  # Адрес новости.
    url_to_comments = news_url + '#comments'  # Адрес блока с комментариями.
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    # Считаем количество комментариев в системе.
    comments_count = Comment.objects.count()
    # Ожидаем ноль комментариев в системе.
    assert comments_count == 0


def test_author_can_edit_comment(author_client, news, comment):
    news_url = reverse('news:detail', args=(news.id,))  # Адрес новости.
    url_to_comments = news_url + '#comments'  # Адрес блока с комментариями.
    edit_url = reverse('news:edit', args=(comment.id,)) 
    FORM_DATA['text'] = NEW_COMMENT_TEXT
    # Выполняем запрос на редактирование от имени автора комментария.
    response = author_client.post(edit_url, data=FORM_DATA)
    # Проверяем, что сработал редирект.
    assertRedirects(response, url_to_comments)
    # Обновляем объект комментария.
    comment.refresh_from_db()
    # Проверяем, что текст комментария соответствует обновленному.
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_delete_comment_of_another_user(author_client, not_author, news):
    comment = Comment.objects.create(  # Создаём объект комментария.
        author=not_author,
        news=news,
        text='Комментарий',
    )
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(delete_url)
    # Проверяем, что вернулась 404 ошибка.
    assert response.status_code == HTTPStatus.NOT_FOUND
    # Убедимся, что комментарий по-прежнему на месте.
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_user_cant_edit_comment_of_another_user(author_client, not_author, news):
    comment = Comment.objects.create(  # Создаём объект комментария.
        author=not_author,
        news=news,
        text='Комментарий',
    )
    edit_url = reverse('news:edit', args=(comment.id,))
    FORM_DATA['text'] = NEW_COMMENT_TEXT
    response = author_client.post(edit_url, data=FORM_DATA)
    # Проверяем, что вернулась 404 ошибка.
    assert response.status_code == HTTPStatus.NOT_FOUND
    # Обновляем объект комментария.
    comment.refresh_from_db()
    # Проверяем, что текст остался тем же, что и был.
    assert comment.text == COMMENT_TEXT
