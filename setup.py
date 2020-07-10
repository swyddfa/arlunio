import os

from setuptools import find_packages
from setuptools import setup

info = {}
version = os.path.join("arlunio", "_version.py")

with open(version) as f:
    exec(f.read(), info)


def readme():
    with open("README.md") as f:
        return f.read()


required = ["attrs", "appdirs", "ipython", "numpy", "Pillow>=6.1.0"]
extras = {
    "dev": [
        "black",
        "flake8",
        "hypothesis",
        "jupyterlab",
        "pre-commit",
        "pytest",
        "pytest-cov",
        "sphinx-autobuild",
        "sphinx_rtd_theme",
        "sphobjinv",
        "towncrier",
        "tox",
    ],
    "doc": ["sphinx", "nbformat"],
    "examples": ["jupyterlab"],
    "testing": ["hypothesis"],
}

extras["all"] = list(
    {item for name, items in extras.items() if name != "dev" for item in items}
)

setup(
    name="arlunio",
    version=info["__version__"],
    project_urls={
        "Documentation": "https://www.arlun.io/docs/",
        "Source": "https://github.com/swyddfa/arlunio",
        "Tracker": "https://github.com/swyddfa/arlunio/issues",
    },
    description="Drawing and animating with a blend of Python and mathematics.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Swyddfa Developers",
    author_email="swyddfa.dev@gmail.com",
    license="MIT",
    packages=find_packages(".", exclude=["tests*"]),
    include_package_data=True,
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Multimedia :: Graphics",
    ],
    entry_points={
        "console_scripts": ["arlunio = arlunio.cli.__main__:main"],
        "sphinx.builders": ["nbtutorial = arlunio.doc", "nbgallery = arlunio.doc"],
        "arlunio.cli.commands": [
            "repl = arlunio.cli.repl:Repl",
            "tutorial = arlunio.cli.tutorial:Tutorial",
        ],
    },
)
