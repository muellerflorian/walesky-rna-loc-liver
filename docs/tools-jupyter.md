
## Jupyter notebooks
We also provide Jupyter notebooks for certain Python analysis workflows. These notebookd provide
an interactive interface to run analysis workflows. For more details, see any of the excellent 
introductions to Jupyter, e.g. [here](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/index.html) or [here](https://realpython.com/jupyter-notebook-introduction/)

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/jupyter-notebook.png" width="600px"></img>

To run these notebooks, we recommend using either [Miniconda with Python 3.7](https://docs.conda.io/en/latest/miniconda.html) or if you plan on using Python more, [Anaconda with Python 3.7](https://www.anaconda.com/distribution/).

We further recommend creating a **dedicated environment** for the Python code to install the code. You can do this from an anaconda terminal. To create and environment named `rna-loc-liver` containing jupyter type (you only have to do this once):

```
conda create -n rna-loc-liver python=3.7 jupyter
```

To install the analysis code (you only have to do this once):

1. **Activate the environment**:
    ```
    conda activate rna-loc-liver
    ```

0. **Install the analysis package** and all required packages
    ```
    pip install git+https://github.com/muellerflorian/walesky-rna-loc-liver
    ```

To open a notebook, open an anaconda terminal in the folder containing the notebook

1. **Activate the environment**:
    ```
    conda activate rna-loc-liver
    ```
0. Navigate to the folder containing the notebook you want to execute.
0. Launch the Jupyter notebook App. . 
    ```
    jupyter notebook
    ```
    This will launch a new browser window (or a new tab)showing the Notebook Dashboard, 
    a control panel that allows (among other things) to select which notebook to open.
    
    Make sure that the notebook is running in the specified environment (upper right
    corner of interface). If not change it from the menu "Kernel".

    Click on the name of the notebook that you want to open, and start processing your data.