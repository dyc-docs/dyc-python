from setuptools import setup


setup(
    name='Document Your Code',
    version='1.0',
    py_modules=['dyc'],
    install_requires=[
        'click==7.0',
        ],
    entry_points = {
        'console_scripts': ['dyc=dyc.dyc:main'],
    }
)