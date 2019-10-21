# Analyze RNA localization in smFISH images from the liver
We provide an analyze workflow to calculate **spatial expression gradients**
in single molecule FISH (smFISH images).

IN this readme, we provide only a brief overview. A detailed description
with detailed step-by-step instructions can be found in the dedicated
<a href="https://muellerflorian.github.io/walesky-rna-loc-liver/" target="_blank">**documentation.**</a>


# TODO
Small dataset to test

# System requirements
1. Analysis requires Matlab to perform detection of individual RNA molecules.
 Expression gradients are determined with ImJoy (imjoy.io), which runs best on
 the latest version of Google chrome.


2. Version of software has been tested on

# Install guide

Code has been tested on Mac OS (Mojave) on a Mac Pro (late 2010).

## FISH-quant
You can obtain the latest version of FISH-quant
<a href="https://bitbucket.org/muellerflorian/fish_quant" target="_blank">**here.**</a>

Installation instruction are provided. Installation time is rapid and requires only
to download the most recent version.

## ImJoy
The provided workflow requires the installation of the ImJoy plugin engine, which
has to be installed only once and takes several minutes.

Installation links to all plugins are provided and installation time for each plugin
is in the range of several minutes for the first install.


# Demo
We provide an example data-set, with detailed instructions for how
data has to be provided, and then step-by-step instructions for how to perform
the analysis. Demo data also contains the expected results, which should be obtained
in a few minutes.

# Instructions for use
The provided instructions for the demo data are directly applicable for new data.