import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Wtp",
    version="0.0.6",
    author="Carlos Niquini",
    description="Whatsapp chat analyzer with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carlosniquini/Wtp",
    packages=setuptools.find_packages(),
    install_requires=[
   'matplotlib',
   'numpy'
    ],
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)