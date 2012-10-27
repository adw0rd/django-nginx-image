from setuptools import setup, find_packages
from nginx_image import __version__

long_description = ""
try:
    readme = open("README.rst")
    long_description = str(readme.read())
    readme.close()
except:
    pass

setup(
    name='django-nginx-image',
    version=__version__,
    description="Resizing and cropping images via Nginx, and cache the result",
    long_description=long_description,
    keywords='django, nginx, image, resize, crop, cache',
    author='Mikhail Andreev',
    author_email='x11org@gmail.com',
    url='http://github.com/adw0rd/django-nginx-image',
    license='BSD',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['setuptools', ],
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
