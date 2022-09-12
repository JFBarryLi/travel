from setuptools import setup, find_packages

setup(
    name='travel',
    author='Barry Li',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pytest==7.1.1',
        'rich==12.0.1',
        'nltk==3.7',
        'tensorflow==2.10.0',
        'transformers==4.21.2',
        'boto3==1.21.32',
        'geopy==2.2.0',
    ],
)
