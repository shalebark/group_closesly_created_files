from setuptools import setup, find_packages

setup(
    name='group_closely_created_files',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click>=8.0',
    ],
    tests_require=[
        'pytest',
        'pytest-xdist',
        'pytest-mock'
    ],
    entry_points={
        'console_scripts': [
           'group-close-files=group_closely_created_files.cli:cli'
        ]
    }
)
