from django import template
from django.db.models.fields.files import ImageFieldFile

register = template.Library()


@register.simple_tag
def thumbnail(image_url, width="-", height="-", crop=False):
    method = "crop" if crop else "resize"
    url = "/{method}/{w}/{h}".format(
        method=method,
        w=width if width else "-",
        h=height if height else "-")
    if isinstance(image_url, (ImageFieldFile, )):
        if hasattr(image_url, 'url'):
            url += image_url.url
    else:
        url += image_url
    return url
