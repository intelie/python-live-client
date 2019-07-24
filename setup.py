import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-live-client",
    version="0.0.3",
    author="Intelie",
    author_email="python@intelie.com",
    description="Intelie Live Client written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intelie/python-live-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aiocometd',
        'requests',
        'asyncio',
        'typing',
        'abc',
        'sys',
        'json',
        'socket',
        'logging'
    ]
)

