# Cell environment
In this workflow, the spatial expression around cells is determined. For this, the user
can define different cells per image, and the expression profile along equidistant regions 
around these cells is calculated.

As input the workflow requires:

-   **FISH-quant**  results file: positions of RNAs.
-   **ImJoy** annotation files: positions of cells.

## Summary of analysis workflow

For each RNA, we determine the closest distance of an RNA to a membrane. For each cells, the number of 
close RNAs is summarized as a distance histogram. To account that for larger distances, the area that
can contain RNAs is larger, this histogram will be normalized, by this area.

## Required tools

### ImJoy Plugins
These plugins have to be installed only once, after installation they will be
available in the dedicated ImJoy workspace: **`liver-rna-loc`**

When pressing on the links below, ImJoy will open in your browser (best in Chrome) and
you will be asked to confirm the installation with a dialog as shown below. 
After confirmation, the plugin together with additional auxiliary plugins will be installed.

* `ImageAnnotator`: annotate your images.
<a href="https://imjoy.io/#/app?w=liver-rna-loc&plugin=oeway/ImJoy-Plugins:ImageAnnotator&upgrade=1" target="_blank">**Install from here.**</a>

* `CellEnvironment`: calculate expression gradient. <a href="https://imjoy.io/#/app?w=liver-rna-loc&plugin=muellerflorian/walesky-rna-loc-liver:CellEnvironment@stable&upgrade=1" target="_blank">**Install from here.**</a>

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/cell_env.png" width="600px"></img>

TODO: add plugin to GitHub. 

### Jupyter notebook
TODO: add notebook to GitHub. 
To perform the calculation of the expression gradients, we also provide a Jupyter notebook `cell_environment.ipynb`, which can be found
on GitHub in the folder [`notebooks`](https://github.com/muellerflorian/walesky-rna-loc-liver/tree/master/notebooks).

## Data

### Data organisation

This workflow requires that data is organised in the following away

1.  A parental folder contains all sample folders.
0.  Each sample (usually a field of view) is in a separate folder, e.g. named `Sample_1`, `Sample_2`, ....       Each sample folder can contain images of multiple channels.
0.  FQ result files are in the same folder. A folder can contain **multiple FQ results** for different channels.
0.  An annotation file with the outlines cells (`annotation.json`). See below
    for more details.


In the example below, a folder contains the annotations (`annotation.json`),
two different channels (`...(green).tif` and `...(red).tif` ), the FQ results
for the green channels `....txt`, and an annotation file (`annotation.json`).

Please note that you can have **only one annotation file per sample folder**. You
can create it by visualizing any of the channels, but the same annotations will be used
for each FQ results file in this folder.

```
├─ data_for_expression_gradient/
│  ├─ Sample_1
│  │  ├─ annotation.json
│  │  ├─ sample_1_green_outline_spots_181018.txt
│  │  ├─ sample_1_green.tif
│  │  ├─ sample_1_red.tif
│  ├─ Sample_2
│  │  ├─ ...
```

### Demo data
TODO: add demo data for cell environment analysis.

You can find already processed demo data
<a href="https://www.dropbox.com/s/qked91rbjwqs9cn/data_for_expression_gradient.zip?dl=0" target="_blank">**here.**</a>

TODO: upon publication, demo data will be moved to Zenodo.

## Analysis

### 1. RNA detection with FQ
Please consult the dedicated section [**here**](rna-detection.md) for more details.

### 2. Annotation of cells.
Please consult the dedicated section [**here**](imjoy-annotation.md) for more details.

For this workflow, you outline all cells that you want to analyze with one annotation type. 
We recommend naming this annotation `Cells`.


### 3. Calculate density profiles
You can run this analysis either with the provided code in the Jupyter notebook,
or use ImJoy.

#### With Jupyter notebook
Once you have your conda environment installed as described in the Overview section,
you can open the Jupyter notebook and analyze your data. You have to execute the first cell
to load the necessary code.

The second cell allows you to

1.  Define the folder containing your data.
2.  Defining the labels for the two annotated reference regions.

Executing the cell, will launch the analysis workflow. described above.

#### Analysis in ImJoy
If you use **Imjoy**, you need to install the **Python plugin engine**. 
The first installation might take a bit of time, since the necessary Python environments
on the plugin engine are created.

Once installed, you will see in the plugin sidebar, before using it, you have to specify
a few analysis parameters, as explained in the table below.


Option           | Type | Default     | Description
---------------- | ---- | ----------- | -----------
`Region label`    | str  | `Cells` | Label of the annotated regions.
`Annotation file` | str  | `annotation.json` | Name of the ImJoy annotation file.
`Hist [min]`    | int  |  0 | Minimum value of histogram to summarize enrichment (in pixel).
`Hist [max]`     | int  | 300 |Maximum value of histogram to summarize enrichment (in pixel).
`Hist [bin]`     | int  | 50 | Bin size (in pixel).


<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/cellenv-plugin-dialog.png" width="250px"></img>

Then you can press on the plugin name to execute the plugin. In a dialog, you will
be asked to specify a folder, please select the parental folder containing the different
sample folders. The plugin will then analyse all sample folders containing an
annotation file. The regions in this file will then be used to establish the spatial
expression gradient between these two regions.

**Progress is reported** in the plugin log (accessible with the 'i' symbol
next to the plugin name) and the ImJoy progress bar.

### 4. Created outputs

The function will create a number of result files, which are stored in the
subfolder `analysis__cell_env`. For each FQ result file, a separate subfolder 
with name of this file is created.

In this folder, results for **each region** are stored
Results files have the full name of the FQ file with the following prefixes

-   **histogram__reg_i.csv** (tab delimited text file), where i is a running index. 
    Contains the spatial expression gradient as a table:

    -   1st col: center of histogram bins
    -   2nd col: RNA counts
    -   3rd col: Pixel counts
    -   4th col: Normalize counts.

-   **histogram_summary__reg_i.png**, summary image of for region `i`. First row shows
    smFISH image, mask of region, distance transform (distance from region). Second row 
    shows the raw histograms for RNAs and pixels, as well as the renormalized histogram. 
