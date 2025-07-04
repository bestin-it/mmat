from setuptools import setup, find_packages

setup(
    name="mmat",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add dependencies here, e.g.:
        # "PyYAML",
        # "requests",
        # "selenium", # Example for a browser environment
        # "puppeteer-python", # Example for a puppeteer environment
        # "argparse", # Included in standard library for Python 3.2+
    ],
    entry_points={
        "console_scripts": [
            "mmat=mmat.cli.main:main",
        ],
    },
    author="Artur Poniedziałek",
    author_email="artur.poniedzialek@bestin-it.com",
    description="Model-based Multi-Agent Testing Framework",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bestin-it/mmat",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6", # Specify your Python version requirement
)
