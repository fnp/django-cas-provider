import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-cas-provider',
    version='24.6',
    description='A "provider" for the Central Authentication Service (http://jasig.org/cas)',
    author='(Chris Williams), Sebastian Annies',
    author_email='(chris@nitron.org), sebastian.annies@googlemail.com',
    url='https://github.com/castlabs/django-cas-provider',
    packages=find_packages(exclude=['cas_provider_examples']),
    include_package_data=True,
    license='MIT',
    long_description=read('README.rst'),
    zip_safe=False,
    install_requires=[
        'Django>=2.0,<5.1',
        'lxml',
        ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
    ]
)
