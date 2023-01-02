from setuptools import setup, find_packages

__version__ = "dev"

setup(
    name="kaggle_cli_wrapper",
    version=__version__,
    url="https://github.com/sunny1401/kaggle_utils",
    author="Sunny Joshi",
    suthor_email="sunnyjoshi1401@gmail.com",
    packages=find_packages(),
    install_requires=[
        "kaggle",
        "pandas"
    ]
)
