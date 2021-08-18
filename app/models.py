import os.path
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models

from app.validators import validate_file_size, validate_file_type

User = get_user_model()


class Photo(models.Model):
    title = models.CharField(max_length=256)
    photo = models.ImageField(upload_to='photos',
                              blank=True,
                              validators=[validate_file_size, validate_file_type])
    thumbnail = models.ImageField(upload_to='small_photos',
                                  blank=True,
                                  validators=[validate_file_size, validate_file_type])
    tags = models.ManyToManyField('Tag', blank=True)
    album = models.ForeignKey('Album', on_delete=models.NOT_PROVIDED)
    creation_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')
        super(Photo, self).save(*args, **kwargs)

    def make_thumbnail(self):

        image = Image.open(self.photo)
        if image.height > 150 or image.width > 150:
            image.thumbnail(settings.THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumb_extension == '.png':
            file_type = 'PNG'
        else:
            return False

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=256)
    creation_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    tag = models.CharField(max_length=256)

    def __str__(self):
        return self.tag
