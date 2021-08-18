from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Album, Photo, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class AlbumSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateField(read_only=True)
    author = serializers.ReadOnlyField(source='author.id')
    count_of_photos = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = '__all__'

    def get_count_of_photos(self, album):
        count = Photo.objects.filter(album=album).count()
        return count


class PhotoListSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='tag'
    )

    class Meta:
        model = Photo
        fields = '__all__'


class PhotoCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(), write_only=True)

    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data):
        tag_names = validated_data.pop('tags')
        titles = tag_names[0].split(', ')
        instance = super().create(validated_data)
        tags = []
        for title in titles:
            tag = Tag.objects.get_or_create(tag=title)
            tags.append(tag[0].pk)
        instance.tags.set(tags)
        return instance
