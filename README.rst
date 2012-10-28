django-nginx-image
========================

.. image:: http://adw0rd.com/media/uploads/django_nginx_image.jpg
    :align: right

Resizing and cropping images via Nginx, and cache the result 

    pip install django-nginx-image

For more details see:
------------------------

* http://github.com/adw0rd/django-nginx-image - the GitHub repository
* http://pypi.python.org/pypi/django-nginx-image - the PyPI page


Settings:
------------------------

Add to ``settings.py``::

    INSTALLED_APPS = (
        'nginx_image',
    )

Add to the configuration file of ``Nginx``::

    location ~* ^/resize/([\d\-]+)/([\d\-]+)/(.+)$ {
        alias <STORAGE_ROOT>/$3;
        image_filter resize $1 $2;
        image_filter_buffer 2M;
        error_page 415 = /empty;
    }

    location ~* ^/crop/([\d\-]+)/([\d\-]+)/(.+)$ {
        alias <STORAGE_ROOT>/$3;
        image_filter crop $1 $2;
        image_filter_buffer 2M;
        error_page 415 = /empty;
    }

    location = /empty {
        empty_gif;
    }

Where, "STORAGE_ROOT" is the path to root of media- and static- directories.
For example I have in my ``settings.py``::

    STORAGE_ROOT = "/storage/kinsburg_tv"
    MEDIA_ROOT = os.path.join(STORAGE_ROOT, "media")
    STATIC_ROOT = os.path.join(STORAGE_ROOT, "static")

Using:
------------------------

In the templates can be used as follows::

    {% load nginx_image %}
    
    Proportionally resize a image, based on the width and the height:
        {% thumbnail user.profile.avatar 130 130 %}

    Proportionally resize a image, based on the width:
        {% thumbnail user.profile.avatar 130 '-' %}
        {% thumbnail user.profile.avatar 130 0 %}
        {% thumbnail user.profile.avatar 130 %}

    Proportionally resize a image, based on the height:
        {% thumbnail user.profile.avatar '-' 130 %}
        {% thumbnail user.profile.avatar 0 130 %}

    Crop a image:
        {% thumbnail user.profile.avatar 130 130 crop=1 %}
        {% thumbnail user.profile.avatar 130 0 crop=1 %}
        {% thumbnail user.profile.avatar 0 130 crop=1 %}


Convert:
-------------

Unfortunaly, **ngx_http_image_filter_module** only supports JPEG, GIF and PNG, so you have to convert BMP to JPG::

    ./manage.py nginx_image_converter -i /storage/project/media -o /storage/project/newmedia

Available options::

    -i SOURCE, --source=SOURCE
                        Source directory with pictures
    -o DESTINATION, --destination=DESTINATION
                        Destination directory for save the pictures
    -q QUALITY, --quality=QUALITY
                        Percentage of quality for images in JPG
    -e, --change-extension
                        Change extension to "jpg"
