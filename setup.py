from setuptools import find_packages, setup
import pathlib

DIR = pathlib.Path(__file__).parent
README = (DIR / 'README.md').read_text()

setup(
    name='simpleLogger',
    packages=find_packages(exclude='tests'),
    version='0.1.0',
    description='A simple logging library for Python that uses decorators to provide logging,'
                ' exception handling, and type-checking.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='',
    author='Yash Kiran Chitre',
    author_email='ychitr2@uic.edu',
    license='MIT',
    include_package_data=True,
    install_requires=['pyyaml', 'psutil'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'matplotlib'],
    test_suite='tests',
)
