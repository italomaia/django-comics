# -*- coding:utf-8 -*-
import sys
import setuptools

setuptools.setup(
    name="django-comics",
    version="0.3",
    packages=[
        "comics",
        "comics.templatetags",
    ],

    install_requires=[
        "django>1.2",
        "PIL",
        "markdown",
    ],

    author="Italo Maia",
    author_email="italo.maia@gmail.com",
    url="https://github.com/italomaia/django-comics",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Simple django comics solution",
    keywords="django comics",
    include_package_data=True,
)
