
# smFISH images
This is a collection of analysis tools to study RNA localization from single
molecule FISH (smFISH) images.

We provide different analysis workflows (listed in the banners).
For each we specify the required installations, and detailed Instructions
for how run these workflows and what results are typically obtained.

## Tools
We use a different open-source software packages, and detail their usage in
the documentation of each workflow.
### FISH-quant: RNA detection
[**FISH-quant**](https://bitbucket.org/muellerflorian/fish_quant/) is a Matlab toolbox to
localize RNAs in 3D from smFISH images.

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/fq-screenshot.png" width="600px"></img>

### ImJoy
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
