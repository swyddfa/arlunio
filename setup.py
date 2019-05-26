import os
from setuptools import setup, find_packages

version = os.path.join("stylo", "_version.py")

with open(version) as f:
    exec(f.read())


def readme():
    with open("README.md") as f:
        return f.read()


def requirements():
    with open("requirements.txt") as f:
        return f.read().split("\n")


setup(
    name="stylo",
    version=__version__,
    url="https://github.com/alcarney/stylo",
    description="Drawing and animating with a blend of Python and mathematics.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Alex Carney",
    author_email="alcarneyme@gmail.com",
    license="MIT",
    packages=find_packages(".", exclude=["tests"]),
    requires_python=">=3.6",
    install_requires=requirements(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Multimedia :: Graphics",
    ],
    entry_points={
        "stylo.parameters": [
            "x = stylo.parameters:xs",
            "y = stylo.parameters:ys",
            "r = stylo.parameters:rs",
            "t = stylo.parameters:ts",
        ],
        "stylo.shapes": [
            "Circle = stylo.shapes:Circle",
            "Square = stylo.shapes:Square",
        ],
    },
)
