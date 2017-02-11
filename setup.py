import os

from setuptools import setup


requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(requirements_path) as fp:
    requirements = list(fp)


setup(
    name='flango',
    version='0.0.1',
    packages=['flango'],
    install_requires=requirements,
    url='https://github.com/theY4Kman/flango',
    license='MIT',
    author='Zach "theY4Kman" Kanzler',
    author_email='they4kman@gmail.com',
    description='Flask-like interface for Django'
)
