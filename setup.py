from setuptools import setup, find_packages

setup(
    name="cacheusagesimulator",
    version="0.1.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=[x for x in open("requirements.txt", "r").read().splitlines()]
)
