from setuptools import setup, find_packages

setup(
    name='taiga-cli',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'taiga=taiga_cli.main:main',
        ],
    },
    install_requires=[],
    description='CLI tool for taiga.io',
    author='Dhaby Xiloj',
    author_email='dxiloj@deltatracking.com',
    url='https://github.com/dhabyx/taiga-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
