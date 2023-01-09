"""
setup.py file
"""

# import the setuptools module
import setuptools

# name of the package
name = "reserving_dashboard_update"

# version of the package
version = "0.0.1"

# author of the package
author = "Andy Weaver"

# author email of the package
author_email = "andrew_weaver@cinfin.com"

# description of the package
description = "This package is used to update the reserving dashboard."

# long description of the package
long_description = "This package is used to update the reserving dashboard."

# long description content type of the package
long_description_content_type = "python"

# url of the package
url = " "

# packages of the package
packages = setuptools.find_packages()

# classifiers of the package
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

# python requires of the package
python_requires = ">=3.6"

# install requires of the package
install_requires = [
    "pandas",
    "numpy",
    "openpyxl",
    "pyodbc"
]

# entry points of the package
entry_points = {
    "console_scripts": [
        "reserving_dashboard_update = reserving_dashboard_update.__main__:main"
    ]
}

# call the setup function
setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url=url,
    packages=packages,
    classifiers=classifiers,
    python_requires=python_requires,
    install_requires=install_requires,
    entry_points=entry_points
)
