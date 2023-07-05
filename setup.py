from setuptools import setup, find_packages

setup(
    name="pyracetimegg",
    version="2.2.0",
    packages=find_packages(),
    install_requires=["Pillow>=9.5.0", "requests>=2.31.0", "tzdata"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
