"""
Setup script.
"""

from setuptools import setup, find_packages

# Package abstract dependencies
REQUIRES = [
    'numpy',
    'scikit-image',
    'scipy',
    'matplotlib',
    'nested_lookup',
    'read-roi',
    'roipoly'
]

setup(
    name='fqa',
    version='0.1.2',
    description='Python code to post-process FISHquant analysis results.',
    url='https://github.com/muellerflorian/FISHquant-Analyst',
    author='Florian MUELLER',
    author_email='muellerf.research@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6.0',
    install_requires=REQUIRES,
    zip_safe=False)
