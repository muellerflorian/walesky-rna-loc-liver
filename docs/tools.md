# Tools
We use a different open-source software packages, and detail their usage in
the documentation of each workflow.

## FISH-quant: RNA detection
[**FISH-quant**](https://bitbucket.org/muellerflorian/fish_quant/) is a Matlab toolbox to
localize RNAs in 3D from smFISH images.

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/fq-screenshot.png" width="600px"></img>

## ImJoy
[**ImJoy**](https://imjoy.io/docs/#/) is image processing platform with an easy
 to use interface powered by a Python engine running in the background. ImJoy plays a
central role in most analysis workflows.

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/imjoy-interface.png" width="600px"></img>

#### Working with ImJoy
We provide links to install the different ImJoy plugins in dedicated **ImJoy workspaces**.
Workspaces can be selected from little puzzle symbol in the upper left part of the
interface.

Most plugins require the **ImJoy Plugin Engine**, to perform computations in
Python. You will need to **install** it only once, but **launch** it each time
you work with ImJoy. For more information for how to install and use the plugin engine,
please consult the [ImJoy documentation](https://imjoy.io/docs/#/user-manual?id=python-engine).

Once installed, ImJoy remembers the workspaces and plugins and you simply have to
open the web app and select the appropriate workspace [https://imjoy.io/#/app](https://imjoy.io/#/app)

If you press on the installation link, the ImJoy web app will open and display a
dialog asking if you want to install the specified plugin. To confirm, press the `install` button.

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/annotor_install.png" width="400px"></img>


## Jupyter notebooks
We also provide Jupyter notebooks for certain Python analysis. To run these notebooks,
we recommend using [Anaconda with Python 3](https://www.anaconda.com/distribution/).

There are many introductions to Jupyter, e.g. [here](https://realpython.com/jupyter-notebook-introduction/).

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/jupyter-notebook.png" width="600px"></img>

We further recommend creating a **dedicated environment** for the Python code to install the code.

Note 1: that steps 1, 3, 4 below have to be done only once.
Note 2: each time you want to use Jupyter, you have to activate the environment (step 2),
and run the notebook (step 5).

You can do this from an anaconda terminal

1. Create the environment, , e.g. named `rna-loc-liver`
    ```
    conda create -n rna-loc-liver python=3.7
    ```

2. **Activate the environment**:
    ```
    conda activate rna-loc-liver
    ```

3. Install the **necessary packages to run Jupyter**
    ```
    conda install nb_conda
    ```

4. **Install the analysis package** and all required packages
    ```
    pip install git+https://github.com/muellerflorian/walesky-rna-loc-liver
    ```

5. Start the Jupyter notebook (best from within the folder containing the notebook).
    ```
    jupyter notebook
    ```
    Make sure that the notebook is running in the specified environment (upper right
    corner of interface). If not change it from the menu "Kernel".