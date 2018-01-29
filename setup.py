from setuptools import setup

with open('requirements.txt') as f:
    REQUIRES = f.readlines()

setup(
    name='taffrail',
    packages=['taffrail'],
    version='0.1',
    install_requires=REQUIRES,
    description='An aggregate API client for Kubernetes metrics',
    author='Taffrail',
    author_email='',
    url='https://github.com/taffrailmetrics/taffrail',
    keywords=['Kubernetes', 'logging', 'metrics'],
    classifiers=[],
)
