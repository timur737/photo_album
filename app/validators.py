from django.conf import settings
from rest_framework.exceptions import ValidationError
from PIL import Image


def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value


def validate_file_type(photo):
    if photo:
        format_img = Image.open(photo.file).format
        photo.file.seek(0)
        if format_img in settings.VALID_IMAGE_FILETYPES:
            return photo
    raise ValidationError("The file format must be JPG, JPEG or PNG")
