import requests
import StringIO

from django.core.files import File

from PIL import Image, ImageOps, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImagesFilters:
    @classmethod
    def ret(cls, photo, image):
        buffer_ = StringIO.StringIO()
        extension = photo.s3_url.name.split('.')[-1].upper()
        extension = 'JPEG' if extension == 'JPG' else extension
        image.save(buffer_, extension)
        return File(buffer_)

    @classmethod
    def to_width(cls, photo, width):
        im = cls._open_image(photo)
        height = int((im.size[1] / float(im.size[0])) * width)
        im = im.resize((width, height), Image.ANTIALIAS)
        return cls.ret(photo, im)

    @classmethod
    def thumbnail(cls, photo, width, height):
        size = (width, height)

        im = cls._open_image(photo)
        im.thumbnail(size, Image.ANTIALIAS)
        image_size = im.size

        thumb = ImageOps.fit(im, size, Image.ANTIALIAS, (0.5, 0.5))
        return cls.ret(photo, thumb)

    @classmethod
    def _open_image(cls, photo):
        if photo.s3_url.name and hasattr(photo.s3_url, 'name') and photo.s3_url.name.startswith('http'):
            response = requests.get(photo.s3_url.name)
            image = StringIO.StringIO(response.content)
            im = Image.open(image)
        else:
            im = Image.open(photo.s3_url)

        return im