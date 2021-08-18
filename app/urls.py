from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from app.views import UserCreate, AlbumViewSet, PhotoViewSet

app_name = 'app'

router = routers.SimpleRouter()
router.register(r'albums', AlbumViewSet, basename='album-list')
router.register(r'photos', PhotoViewSet, basename='photo-list')

urlpatterns = router.urls
urlpatterns += [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
]
