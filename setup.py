from setuptools import setup

setup(
    name='urlshortapi',
    packages=['urlshortapi'],
    include_package_data=True,
    install_requires=[
        'flask',
        'boto3',
    ],
)
