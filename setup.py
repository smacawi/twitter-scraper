import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitter-scraper",
    version="0.0.1",
    author="amr-amr",
    description="A package to scrape live tweets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smacawi/twitter-scraper",
    packages=setuptools.find_packages(),
    install_requires=[
        'tweepy>=3.7.0',
        'dataset=>1.1.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)