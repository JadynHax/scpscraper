from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

with open("requirements.txt", "r") as fh:
  requirements = fh.readlines()

setup(
    name="scpscraper",
    packages=['scpscraper'],
    version="0.1.1",
    license="MIT",
    author="JaonHax",
    author_email="jaonhax@gmail.com",
    description="A Python library designed for scraping data from the SCP wiki.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JaonHax/scp-scraper",
    keywords=["scp", "foundation", "webscraper", "tensorflow", "dataset"],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Development Status :: 3 - Alpha",
                 "Intended Audience :: Developers",
                 "Natural Language :: English",
                 "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ]
)
