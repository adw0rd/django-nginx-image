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

Now, add two sections called ``server``:

1. The cache server ``www.example.org``, which will got to the second server and receive changed image.
2. The image server ``image.example.org``, which can to resize and to crop a images.

Client request ➡ ``www.example.org`` ➡ ``image.example.org`` (resize/crop a image)
      ⬉ ``www.example.org`` (save image to cache) ⬋

Add to the configuration file of ``Nginx``::

    http {

        proxy_cache_path <STORAGE_ROOT>/nginx/cache levels=1:2 keys_zone=<CACHE_NAME>:10m max_size=1G;
        
        server {
            listen 80;
            server_name www.example.org;
            
            location ~* ^/resize/([\d\-]+)/([\d\-]+)/(.+)$ {
                proxy_pass http://image.example.org/resize/$1/$2/$3;
                proxy_cache <CACHE_NAME>;
                proxy_cache_key "$host$document_uri";
                proxy_cache_valid 200 1d;
                proxy_cache_valid any 1m;
                proxy_cache_use_stale error timeout invalid_header updating;
            }
            
            location ~* ^/crop/([\d\-]+)/([\d\-]+)/(.+)$ {
                proxy_pass http://image.example.org/crop/$1/$2/$3;
                proxy_cache <CACHE_NAME>;
                proxy_cache_key "$host$document_uri";
                proxy_cache_valid 200 1d;
                proxy_cache_valid any 1m;
                proxy_cache_use_stale error timeout invalid_header updating;
            }
        }
        
        server {
            listen 80;
            server_name image.example.org;
            
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
        }
    }

Where, "STORAGE_ROOT" is the path to root of media- and static- directories.
For example I have in my ``settings.py``::

    STORAGE_ROOT = "/storage/kinsburg_tv"
    MEDIA_ROOT = os.path.join(STORAGE_ROOT, "media")
    STATIC_ROOT = os.path.join(STORAGE_ROOT, "static")

And "CACHE_NAME" is the arbitrarily name, example: "my_project_cache".

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

