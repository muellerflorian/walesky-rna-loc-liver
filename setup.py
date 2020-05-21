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
    'roipoly',
    'pandas',
    'tqdm'
]

REQUIRES_STABLE = [
    'numpy==1.18.2',
    'scikit-image==0.16.2',
    'scipy==1.4.1',
    'matplotlib==3.2.1',
    'nested_lookup==0.2.21',
    'read-roi==1.5.2',
    'roipoly==0.5.2',
    'pandas==1.0.3',
    'tqdm==4.43.0'
]

setup(
    name='rnaloc',
    version='0.1.0',
    description='Python code to post-process FISH-quant analysis results.',
    url='https://github.com/muellerflorian/walesky-rna-loc-liver',
    author='Florian MUELLER',
    author_email='muellerf.research@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='==3.7.6',
    install_requires=REQUIRES_STABLE,
    zip_safe=False)
