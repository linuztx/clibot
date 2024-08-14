from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="clibot",
    version="0.1.1",
    author="linuztx",
    author_email="linuztx@gmail.com",
    description = "An innovative command-line tool driven by powerful large language models, designed to accelerate task completion and maximize your productivity.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linuztx/clibot",
    packages=find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires='>=3.6',
    install_requires=[
        "openai==1.34.0",
        "requests==2.32.3",
    ],
    entry_points={
        'console_scripts': [
            'clibot=clibot.cli:main',
        ],
    },
)
