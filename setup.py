from setuptools import setup, find_packages

setup(
    name='taffrail',
    packages=find_packages(),
    include_package_data=True,
    version='0.2',
    description='An aggregate metrics python client for Kubernetes',
    author='Taffrail',
    author_email='',
    url='https://github.com/taffrailmetrics/taffrail',
    keywords=['Kubernetes', 'logging', 'metrics'],
    classifiers=[],
)
