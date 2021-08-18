import json
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from app.models import Album, Photo, Tag

client = APIClient()


@pytest.fixture
def user_data():
    u = {
        'username': 'TestUser',
        'password': 'testpasswdwithsalt'
    }

    return u


@pytest.fixture
def create_user(db, django_user_model, user_data):
    def make_user(**kwargs):
        kwargs['username'] = user_data['username']
        kwargs['password'] = user_data['password']
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, user_data):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        resp = client.post('/api/v1/login/', user_data)
        token = json.loads(resp.content)
        return token, user

    return make_auto_login


@pytest.mark.django_db
class TestUserView:

    def test_registration(self, client, user_data):
        r = client.post('/api/v1/register/', user_data)
        assert r.status_code == 201

    def test_login(self, client, user_data, create_user):
        user = create_user()
        resp = client.post('/api/v1/login/', user_data)
        json_resp = json.loads(resp.content)
        key = list(json_resp.keys())[0]
        assert resp.status_code == 200
        assert key == 'token'
        assert user.is_authenticated is True


@pytest.mark.django_db
class TestALbumViews:

    def test_list(self, auto_login_user):
        raw_token, user = auto_login_user()
        token = raw_token['token']
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        r = client.get('/api/v1/albums/')
        assert r.status_code == 200

    def test_retrieve(self, auto_login_user):
        raw_token, user = auto_login_user()
        token = raw_token['token']
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        album = Album.objects.create(title='Gallery', author=user)
        resp = client.get('/api/v1/albums/{}/'.format(album.pk))
        assert resp.status_code == 200


class TestPhotoViews:
    def test_list(self, auto_login_user):
        raw_token, user = auto_login_user()
        token = raw_token['token']
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        resp = client.get('/api/v1/photos/')
        assert resp.status_code == 200

    def test_retrieve(self, auto_login_user):
        raw_token, user = auto_login_user()
        token = raw_token['token']
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        img = SimpleUploadedFile('test_image.jpg',
                                 content=open(
                                     f"{Path().absolute()}/app/tests/image_folder/image.jpg",
                                     'rb').read(), content_type='image/jpeg')
        album = Album.objects.create(title='Gallery', author=user)
        photo = Photo.objects.create(title='Flowers', photo=img, album=album)
        tag = Tag.objects.create(tag='Travel')
        photo.tags.add(tag)
        resp = client.get('/api/v1/albums/{}/'.format(photo.pk))
        assert resp.status_code == 200
