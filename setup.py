import os

from setuptools import setup


ROOT_DIR = os.path.dirname(__file__)
requirements_path = os.path.join(ROOT_DIR, 'requirements.txt')
readme_path = os.path.join(ROOT_DIR, 'README.md')


def get_requirements():
    with open(requirements_path) as fp:
        return list(fp)


def get_readme():
    with open(readme_path) as fp:
        return fp.read()


setup(
    name='flango',
    version='0.0.2',
    packages=['flango'],
    install_requires=get_requirements(),
    url='https://github.com/theY4Kman/flango',
    license='MIT',
    author='Zach "theY4Kman" Kanzler',
    author_email='they4kman@gmail.com',
    description='Flask-like interface for Django',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
)
