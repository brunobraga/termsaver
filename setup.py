import os
import platform

import setuptools

from termsaverlib import constants

# if platform.system() == 'FreeBSD':
#     man_dir = 'man'
# else:
#     man_dir = 'share/man'

# data_files = [(os.path.join('share', 'locale', lang, 'LC_MESSAGES'),
#                 [os.path.join('locale', lang, 'LC_MESSAGES',
#                 'termsaver.mo')]) for lang in os.listdir('locale')]
# data_files.append((os.path.join(man_dir, 'man1'), ['doc/termsaver.1']))
# data_files.append(('etc/bash_completion.d',
#                    ['completion/termsaver-completion.bash']))
# data_files.append(('share/zsh/site-functions', ['completion/_termsaver']))


long_desc = open("README.md").read()
required = ['argparse', 'pillow', 'requests'] # Comma seperated dependent libraries name

setuptools.setup(
    name="termsaver",
    version=constants.App.VERSION,
    author="Bruno Braga",
    author_email="bruno@brunobraga.net",
    license="Apache License v2",
    description="Simple text-based terminal screensaver.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://www.github.com/brunobraga/termsaver",
    packages = [
        'termsaverlib',
        'termsaverlib.plugins',
        'termsaverlib.screen',
        'termsaverlib.screen.base',
        'termsaverlib.screen.helper',
    ],
    # project_urls is optional
    project_urls={
        "Bug Tracker": "https://github.com/brunobraga/termsaver/issues",
    },
    keywords=['command-line', 'terminal', 'screensaver'],
    # data_files=data_files,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'termsaver = termsaver:main'
        ]
    },
    install_requires=required,
    python_requires=">=3.6",
)