# Tools
We use a different open-source software packages, and detail their usage in
the documentation of each workflow.

## FISH-quant: RNA detection
[**FISH-quant**](https://bitbucket.org/muellerflorian/fish_quant/) is a Matlab toolbox to
localize RNAs in 3D from smFISH images.

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/fq-screenshot.png" width="600px"></img>

## ImJoy
[**ImJoy**](https://imjoy.io/docs/#/) is image processing platform with an easy
 to use interface. Some important features

 2. Specific functionality is provided by plugins, which can be installed with simple links. Available 
    plugins are listed in the plugin list on the left part of the interface. Depending on the implementation 
    plugins are either executed directly by pressing on their name, or a simple interface can be displayed when
    pressing on the arrow down symbol. 
 3. ImJoy can have several workspaces. Each workspace can contain multiple plugins and is often
    dedicated to a specific data processing task. Workspaces can be selected from little puzzle symbol in the upper left part of the interface.
 
   <img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/imjoy-interface.png" width="600px"></img>

### Installing plugins
We provide links to install the different ImJoy plugins. These installation links also specify
in which **ImJoy workspaces** the plugin will be installed. 

If you press on the installation link, the ImJoy web app will open and display a
dialog asking if you want to install the specified plugin. To confirm, press the `install` button.

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/annotor_install.png" width="400px"></img>

Once installed, ImJoy remembers the workspaces and plugins and you simply have to
open the ImJoy app and select the workspace [https://imjoy.io/#/app](https://imjoy.io/#/app)


### Running Python plugins

Some of the provided plugins use code written in Python. In order for ImJoy this code, it can connect 
either to a **ImJoy plugin engine** or a **Jupyter notebook**. Either option requires a one-time installation.

##### Plugin engine
The plugin engine has to be **installed** only once, but **launched** each time you work with ImJoy.

Please note, that the Python engine might not work well under Windows. 
Here, we recommend using a Jupyter notebook instead.

For more information for how to install and use the plugin engine,
please consult the [ImJoy documentation](https://imjoy.io/docs/#/user-manual?id=python-engine).


##### Jupyter notebook
ImJoy can also connect to a Jupyter notebook to run Python code. 

We recommend an installation with [Miniconda with Python 3.7](https://docs.conda.io/en/latest/miniconda.html).

Once you installed Miniconda, open and Anaconda terminal and create a computational environment (named `rna-loc-liver` for these workflows). Note that you only need to do this once:
    
```
conda create -n rna-loc-liver python=3.7 jupyter
```

Once you have this environment, you can activate it and start an Jupyter Kernel, to which ImJoy can connect. 
This you have to do each time, you want to use a Jupyter engine in ImJoy.

1. **Activate the environment**:
    ```
    conda activate rna-loc-liver
    ```
2. **Start Jupyter notebook**. In order to process your data, navigate to the folder containing your 
   data and start the notebook from there. Note that for security reasons, that from within a Jupyter 
   notebook you can only see folder (and its subfolders) from which it was started. 
    ```
    jupyter notebook --NotebookApp.allow_origin='*' --no-browser
    ```
    Copy the provided URL including the token:, somehting like `http://127.0.0.1:8889/?token=16126ce8b02ee35103200c46d71b3f946bfb408d1cae0f68`
3. In ImJoy, press on the rocket symbol in the upper right corner, select `Add Jupyter-Engine` 
    and past the URL from the step above. 
4. You can now connect your plugin to this Juypyter Kernel, by clicking on the puzzle symbol 
    next to the plugin name, and selecting the Juypyter Notebook as engine.      


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