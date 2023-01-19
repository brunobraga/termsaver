import os
import platform

import setuptools

from termsaver.termsaverlib import constants

long_desc = open("README.md").read()
required = ['pillow', 'requests'] # Comma seperated dependent libraries name

setuptools.setup(
    name="termsaver",
    version=constants.App.VERSION,
    author="Bruno Braga",
    author_email="bruno@brunobraga.net",
    maintainer="Eddie Dover",
    maintainer_email="ed@eddiedover.dev",
    license="Apache License v2",
    description="Simple text-based terminal screensaver.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://www.github.com/brunobraga/termsaver",
    packages=setuptools.find_packages(where="."),
    # project_urls is optional
    project_urls={
        "Bug Tracker": "https://github.com/brunobraga/termsaver/issues",
    },
    keywords=['command-line', 'terminal', 'screensaver'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'termsaver = termsaver:entryPoint'
        ]
    },
    install_requires=required,
    python_requires=">=3.6",
)