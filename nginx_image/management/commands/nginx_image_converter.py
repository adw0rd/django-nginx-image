import os
from PIL import Image
from optparse import make_option

from django.core.management.base import BaseCommand


NGX_HTTP_IMAGE_FILTER_MODULE_IS_SUPPORTS = ('JPEG', 'GIF', 'PNG', )


class Command(BaseCommand):
    help = "Recursively the source directory, finds the BMP files and convert them to JPG.\n"\
           "Example: ./manage.py nginx_image_converter -i /storage/project/media/ -o /storage/project/newmedia -q75"

    option_list = BaseCommand.option_list + (
        make_option(
            '-i',
            '--source',
            dest='source',
            type='str',
            help='Source directory with pictures'),
        make_option(
            '-o',
            '--destination',
            dest='destination',
            type='str',
            help='Destination directory for save the pictures'),
        make_option(
            '-q',
            '--quality',
            dest='quality',
            type='int',
            default=100,
            help='Percentage of quality for images in JPG'),
        make_option(
            '-e',
            '--change-extension',
            action="store_true",
            dest='change_extension',
            default=False,
            help='Change extension to "jpg"'),
    )

    def handle(self, **options):
        self.source_dir = options.get('source')
        self.destination_dir = options.get('destination')
        self.change_extension = options.get('change_extension')
        self.quality = options.get('quality')

        assert os.path.exists(self.source_dir)
        assert os.path.exists(self.destination_dir)

        for source_directory, dirnames, filenames in os.walk(self.source_dir):
            for filename in filenames:
                try:
                    image = Image.open(os.path.join(source_directory, filename).encode('utf-8'))
                except IOError:
                    continue
                if image.format.upper() in NGX_HTTP_IMAGE_FILTER_MODULE_IS_SUPPORTS:
                    continue
                self.convert(image, source_directory, filename)

    def convert(self, image, source_directory, filename):
        clean_filename, clean_ext = filename.rsplit('.', 1)
        clean_filepath = os.sep.join([part for part in source_directory.replace(self.source_dir, '').split(os.sep) if part])

        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        destination_directory = os.path.join(self.destination_dir, clean_filepath)
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        extension = 'jpg' if self.change_extension else clean_ext
        destination_filepath = os.path.join(destination_directory, '{}.{}'.format(clean_filename, extension))

        return image.save(destination_filepath.encode('utf-8'), 'JPEG', quality=self.quality)
