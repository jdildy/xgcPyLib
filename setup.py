from setuptools import setup, find_packages
import site
import sys



if __name__ == "__main__": 
    sys.path += site.getsitepackages()

    s = setup(
    name = 'xgc-analysis-library',
    version = '0.1.0',
    description = 'Data Analysis Library for Computation and Visualization',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/jdildy/xgcPyLib.git', 
    packages = find_packages(),
    classifiers= [
    ],
    python_requires = '>=3.6',
    install_requires = [],
    entry_points = {},
    )
