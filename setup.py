try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="Document Your Code",
    version="0.0.1",
    author="Mohammad Albakri",
    author_email="mohammad.albakri93@gmail.com",
    packages=['dyc'],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dyc-docs/dyc-python.git",
    install_requires=[
        "click==7.0",
        "pyyaml==3.13"
        ],
    entry_points = {
        "console_scripts": ["dyc=dyc.dyc:main"],
    }
)