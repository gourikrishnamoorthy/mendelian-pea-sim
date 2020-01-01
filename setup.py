import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Mendelian Pea',
    version='1.0',
    scripts=['run.py'],
    author="Gouri K",
    author_email="gouri.k@gmail.com",
    description="A Mendelian Pea Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL 2.0 License",
        "Operating System :: OS Independent",
    ],
)
