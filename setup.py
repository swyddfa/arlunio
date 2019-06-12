import os
from setuptools import setup, find_packages

version = os.path.join("stylo", "_version.py")

with open(version) as f:
    exec(f.read())


def readme():
    with open("README.md") as f:
        return f.read()


required = ["attr", "numpy", "Pillow", "Click", "matplotlib"]
extras = {"dev": ["tox"], "examples": ["jupyterlab"]}


setup(
    name="stylo",
    version=__version__,
    project_urls={
        "Documentation": "https://stylo.readthedocs.io/en/latest",
        "Source": "https://github.com/swyddfa/stylo",
        "Tracker": "https://github.com/swyddfa/stylo/issues",
    },
    description="Drawing and animating with a blend of Python and mathematics.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Alex Carney",
    author_email="alcarneyme@gmail.com",
    license="MIT",
    packages=find_packages(".", exclude=["tests"]),
    package_data={
        "stylo.cli.scripts": ["*.sh"],
        "stylo.tutorial": ["*.ipynb", "**/*.ipynb"],
    },
    python_requires=">=3.6",
    install_requires=required,
    extras_require=extras,
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
        "console_scripts": ["stylo = stylo.__main__:cli"],
        "stylo.cli.commands": ["tutorial = stylo.cli.tutorial:register"],
        "stylo.parameters": [
            "x = stylo.parameters:xs",
            "y = stylo.parameters:ys",
            "r = stylo.parameters:rs",
            "t = stylo.parameters:ts",
        ],
        "stylo.shapes": [
            "Circle = stylo.shapes:Circle",
            "Ellipse = stylo.shapes:Ellipse",
            "Square = stylo.shapes:Square",
        ],
    },
)
