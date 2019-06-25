import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synology-toolset",
    version="0.1.2",
    author="Ed Garabito",
    author_email="eduardo@gottabegarabi.com",
    description="A Python API wrapper and toolset for interfacing with Synology NAS devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DazEdword/synology-toolset",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)