from setuptools import setup, find_packages

setup(
    name="pyracetimegg",
    version="2.1.0",
    packages=find_packages(),
    install_requires=["Pillow", "requests", "tzdata"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
