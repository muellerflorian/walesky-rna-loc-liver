# Cell environment
In this workflow, the spatial expression around cells is determined. For this, the user
can define different cells per image, and the expression profile along equidistant regions 
around these cells is calculated.

As input the workflow requires:

-   **FISH-quant**  results file: created with the with FISH-quant.
-   **ImJoy** annotation files: annotations of the cells.

## Summary of analysis workflow

For each RNA, we determine the closest distance of an RNA to a membrane. For each cells, the number of 
close RNAs is summarized as a distance histogram. To account that for larger distances, the area that
can contain RNAs is larger, this histogram will be normalized, by this area.

## Required tools

### ImJoy Plugins
These plugins have to be installed only once, after installation they will be
available in the dedicated ImJoy workspace: **`liver-rna-loc`**

Pressing on the links below, will open ImJoy in your browser (best in Chrome) and
allow you to install the required plugins. You will be asked to confirm the installation
with a dialog as shown below. After confirmation, the plugins will be installed together with
additional auxiliary plugins.

* `ImageAnnotator`: annotate your images.
<a href="https://imjoy.io/#/app?w=liver-rna-loc&plugin=oeway/ImJoy-Plugins:ImageAnnotator&upgrade=1" target="_blank">**Install from here.**</a>

* `CellEnvironment`: calculate expression gradient. <a href="https://imjoy.io/#/app?w=liver-rna-loc&plugin=muellerflorian/walesky-rna-loc-liver:CellEnvironment@stable&upgrade=1" target="_blank">**Install from here.**</a>

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/exprdensity.png" width="600px"></img>

TODO: add plugin to GitHub. 

### Jupyter notebook
To perform the calculation of the expression gradients, we also provide a Jupyter notebook `cell_environment.ipynb`. This notebook can be found
in the folder [`notebooks`](https://github.com/muellerflorian/walesky-rna-loc-liver/tree/master/notebooks).

TODO: add notebook to GitHub. 

## Data

### Data organisation

This workflow requires that data is organised in the following away

1.  A parental folder contains all sample folders.
0.  Each sample (usually a field of view) is in a separate folder, e.g. named `Sample_1`, `Sample_2`, ....       Each sample folder can contain images of multiple channels.
0.  FQ result file are in the same folder. A folder can contain FQ results for different channels.
0.  An annotation file with the two reference regions (`annotation.json`). See below
    for more details.


In the example below, a folder contains the annotations (`annotation.json`),
two different channels (`...(green).tif` and `...(red).tif` ), the FQ results
for both channels `....txt`, and an annotation file (`annotation.json`).

Please note that you can have **only one annotation file per sample folder**. You
can generate it based on any of the channels, but the same file will be used
for all FQ results in this channel.

```
├─ data_for_expression_gradient/
│  ├─ Sample_1
│  │  ├─ annotation.json
│  │  ├─ sample_1_green_outline_spots_181018.txt
│  │  ├─ sample_1_green.tif
│  │  ├─ sample_1_red_outline_spots_181017.txt
│  │  ├─ sample_1_red.tif
│  ├─ Sample_2
│  │  ├─ ...
```

### Demo data
You can find already processed demo data
<a href="https://www.dropbox.com/s/qked91rbjwqs9cn/data_for_expression_gradient.zip?dl=0" target="_blank">**here.**</a>

TODO: add demo data for cell environment analysis.
TODO: upon publication, demo data will be moved to Zenodo.

## Analysis

### 1. RNA detection with FQ
Please consult the dedicated section [**here**](rna-detection.md) for more details.

### 2. Annotation of cells.
Please consult the dedicated section [**here**](imjoy-annotation.md) for more details.

For this workflow, you need one annotation type to outline all cells that you want to analyze. 
We recommend naming it `Cells`.


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
If you use **Imjoy**, you need to install the **Python plugin engine**. The first installation might take a bit of time, since the necessary Python environments
on the plugin engine are created.

Once installed, you will see in the plugin sidebar, before using it, you have to
specify the labels of the two reference regions. You can change the default labels
by pressing on the arrow down symbol next to the plugin name.

In the example below the labels `CV` and `PL` are defined for the first and second
region, respectively.

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/expGrad-plugin-dialog.png" width="250px"></img>

Then you can press on the plugin name to execute the plugin. In a dialog, you will
be asked to specify a folder, please select the parental folder containing the different
sample folders. The plugin will then analyse all sample folders containing an
annotation file. The regions in this file will then be used to establish the spatial
expression gradient between these two regions.

**Progress is reported** in the plugin log (accessible with the 'i' symbol
next to the plugin name) and the ImJoy progress bar.

Plugin creates results described in section 'Outputs'.

### 4. Created outputs

The function will create a number of result files, which are stored in the
subfolder ``. For this, it will create a new sub-folder called `analysis__exprGradient`.
Results files have the full name of the FQ file with the following prefixes

-   **_summary_density** (PNG file). Contains plots of expression density plots.
    Cells are filled with pixel values corresponding to their expression level.

-   **_summary_gradient** (PNG file). Contains summary plots for the spatial gradients
    between two the two reference points (the first plot shown on this page).

-   **hist_expression** (tab delimited text file). Contains the spatial expression
    gradient as a table:

    -   1st col: normalised distance,
    -   2nd col: normalised counts by number of pixels (4th col)
    -   3rd col: RNA counts
    -   4th col: number of pixels in the image within range (for normalisation)

-   **img_density** (16bit tif file). Contains the expression density plots. The pixel
    value of the cell corresponds to the number of RNAs in this cell. No outlines are
    shown. Files can be rendered with Fiji and an adequate look-up table.

-   **img_density_outline** (16 bit tif file). Contains the expression density plot
    and the cell outlines. The outlines of the cells are set to the maximum RNA count
    in the image. This guarantees that the outlines can be seen.

-   **img_outline** (8 bit image). Outlines of all cells in the image.
