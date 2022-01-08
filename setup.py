import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pyboyenv-Kugge",
    version="0.0.1",
    author="Sofiane DJERBI",
    author_email="sofiane.djerbi38@gmail.com",
    description="Turn any gameboy game into a reinforcement learning environment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kugge/pyboyenv",
    project_urls={
        "Bug Tracker": "https://github.com/kugge/pyboyenv/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyboy",
        "gym"
    ],
    python_requires=">=3.6",
)
