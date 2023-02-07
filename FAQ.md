# Frequently Asked Questions

Q: A receive the error "AttributeError: module 'collections' has no attribute 'MutableMapping'.

A: Your system likely has an out of date essential package, like pip, wheel, or setuptools. Try upgrading them with the following command: `pip install --upgrade pip wheel setuptools requests`

Q: After installing `termsaver` I get a `command not found` error.

A: Depending on your distro, your packages might have been installed to ~/.local/bin. Please add this path to your PATH. e.g. `export PATH=$PATH:/home/<user>/.local/bin`

If you have a question that is not answered here, please submit an issue on GitHub and we'll be happy to add it if applicable.