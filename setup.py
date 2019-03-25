try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='Document Your Code',
    version='1.0',
    py_modules=['dyc'],
    install_requires=[
        'click==7.0',
        'pyyaml'
        ],
    entry_points = {
        'console_scripts': ['dyc=dyc.dyc:main'],
    }
)