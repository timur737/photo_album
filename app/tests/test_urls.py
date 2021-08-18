import pytest
from django.urls import reverse


class TestURL:

    def test_url_not_authorized(self, client):
        album_url = '/api/v1/albums/'
        photo_url = '/api/v1/photos/'
        resp = client.get(album_url)
        assert resp.status_code == 401
        resp = client.get(photo_url)
        assert resp.status_code == 401

    def test_names_and_validate(self):
        url = reverse('app:album-list-list')
        assert url == '/api/v1/albums/'
        url = reverse('app:photo-list-list')
        assert url == '/api/v1/photos/'
        url = reverse('app:login')
        assert url == '/api/v1/login/'
        url = reverse('app:register')
        assert url == '/api/v1/register/'
