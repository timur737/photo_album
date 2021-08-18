"""API Views"""
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from app.models import Album, Photo
from app.serializers import UserSerializer, AlbumSerializer, \
    PhotoListSerializer, PhotoCreateSerializer


class UserCreate(CreateAPIView):
    """User Create View"""
    serializer_class = UserSerializer
    queryset = get_user_model().objects

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(UserCreate, self).get_permissions()


class AlbumViewSet(viewsets.ModelViewSet):
    """Album ViewSet"""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('creation_date',)

    def list(self, request, *args, **kwargs):
        user = request.user
        albums = Album.objects.filter(author=user.id)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        album_data = request.data
        user = request.user
        new_album = Album.objects.create(title=album_data['title'], author=user)
        new_album.save()
        serializer = AlbumSerializer(new_album)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        album_object = self.get_object()
        album_data = request.data
        user = request.user
        album_object.title = album_data['title']
        album_object.author = user
        album_object.save()
        serializer = AlbumSerializer(album_object)
        return Response(serializer.data)


class PhotoViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """Photo Viewset"""
    permission_classes = (IsAuthenticated,)
    queryset = Photo.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('album', 'tags',)
    ordering_fields = ('creation_date', 'album')

    def get_serializer_class(self):
        if self.action == "create":
            return PhotoCreateSerializer
        else:
            return PhotoListSerializer
