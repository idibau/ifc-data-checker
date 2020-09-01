"""setup"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ifc-data-checker-dfringeli",  # Replace with your own username
    version="0.0.2",
    author="Dominik Fringeli",
    author_email="dominik.fringeli@students.fhnw.ch",
    description="The IFC Data Checker can validate rules on an ifc model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idibau/ifc-data-checker",
    packages=setuptools.find_packages(),
    py_modules=["checker"],
    install_requires=['pyyaml', 'jsonschema'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console"
    ],
    python_requires='>=3.8',
)
