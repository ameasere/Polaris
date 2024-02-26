# this file contains some placeholders
# that are changed in a local copy if a release is made

import setuptools

README = 'README.md'  # the path to your readme file
README_MIME = 'text/markdown'  # it's mime type

with open(README, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polaris",
    version="1",
    author="ameasere",
    description="Open Source HSM Framework",
    url="https://github.com/ameasere/polaris",
    long_description=long_description,
    long_description_content_type=README_MIME,
    packages=setuptools.find_packages(),
    author_email="leigh@ameasere.com",
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent"
    ],
    install_requires=["cryptography", 
                      "psutil", 
                      "pyside6"
    ]
)
