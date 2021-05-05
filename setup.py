from setuptools import find_packages, setup

setup(
    name='simpleLogger',
    packages=find_packages(exclude=('tests')),
    version='0.1.0',
    description='My first Python library',
    author='Yash Kiran Chitre',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)