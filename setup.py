from setuptools import setup, find_packages

setup(
    name='travel',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pytest==7.1.1',
        'rich==12.0.1',
        'nltk==3.7',
    ],
)
