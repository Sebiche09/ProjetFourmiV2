import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="main",
    version="0.0.1",
    author="Vleminckx Sébastien",
    author_email="s.vleminckx@ephec.be",
    description="Une simulation de colonie de fourmis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sebiche09/ProjetFourmiV2/src/main.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
