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

### FISH-quant for RNA detection
For more information, Please visit the dedicated section [**here**](rna-detection.md) 

### ImJoy Plugins
These plugins have to be installed only once, after installation they will be
available in the dedicated ImJoy workspace: **`liver-rna-loc`**

When pressing on the links below, ImJoy will open in your browser (best in Chrome) and
you will be asked to confirm the installation with a dialog as shown below. 
After confirmation, the plugin together with additional auxiliary plugins will be installed.

* `ImageAnnotator`: annotate your images.
<a href="https://imjoy.io/#/app?w=liver-rna-loc&plugin=oeway/ImJoy-Plugins:ImageAnnotator&upgrade=1" target="_blank">**Install from here.**</a>

* `CellEnvironment`: calculate expression gradient. <a href="https://imjoy.io/#/app?w=liver-rna-loc&plugin=muellerflorian/walesky-rna-loc-liver:CellEnvironment@stable&upgrade=1" target="_blank">**Install from here.**</a> Alternatively, you can also use the provided Jupyter notebook.

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/cell_env.png" width="600px"></img>

### Jupyter notebook
To perform the calculation of the expression gradients, we also provide a Jupyter notebook `cell_environment.ipynb`, which can be found on GitHub in the folder [`notebooks`](https://github.com/muellerflorian/walesky-rna-loc-liver/tree/master/notebooks).

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

## Analysis workflow

### 1. RNA detection with FQ
For more details, please consult the dedicated section [**here**](rna-detection.md) 

### 2. Annotation of cells.
For this workflow, all cells that should be analyze have to be manually annotated in ImJoy with one annotation
type. We recommend naming this annotation `Cells`, but other names can be used as well (but you have
to update the default value in the analysis scripts as described below).

For more details, please consult the dedicated section [**here**](imjoy-annotation.md)


### 3. Calculate density profiles
You can run this analysis either with the dedicated ImJoy plugin or the provided Jupyter notebook.
In either case, you need to have a local installation of Python. For more information consult the 
dedicated section [**here**](tools.md). 

#### Analysis in ImJoy
If you use **Imjoy**, you need to install the **Python plugin engine**. 
The first installation might take a bit of time, since the necessary Python environments
on the plugin engine are created.

Once installed, you will see in the plugin sidebar, where you can launch the analysis in a
few steps

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/cellEnv-plugin-dialog.png" width="250px"></img>

1. You have to analye the folder that should be processed. Click on the blue text
    `Press to define folder` to do so.

2. If needed, change the analysis parameters (see Table below), and press on blue text 
   `Press to run analysis`. 

        Option           | Type | Default     | Description
        ---------------- | ---- | ----------- | -----------
        `Region label`    | str  | `Cells` | Label of the annotated regions.
        `Annotation file` | str  | `annotation.json` | Name of the ImJoy annotation file.
        `Hist [min]`    | int  |  0 | Minimum value of histogram to summarize enrichment (in pixel).
        `Hist [max]`     | int  | 300 |Maximum value of histogram to summarize enrichment (in pixel).
        `Hist [bin]`     | int  | 50 | Bin size (in pixel).

3. The plugin will then analyse all sample folders containing an annotation file. 
   Progress can be monitored in the plugin log, accessible via the `i` next to the plugin name.

**Progress is reported** in the plugin log (accessible with the 'i' symbol
next to the plugin name) and the ImJoy progress bar.

#### With Jupyter notebook
Once you have your conda environment installed as described in the Overview section,
you can open the Jupyter notebook (`cell_environment.ipynb`, which can be found on 
GitHub in the folder `notebooks`.

You have to execute the first cell to import the analysis package.

The second cell allows you to

1.  Define the folder containing your data.
2.  Defining the parameters described above for the analysis. 

Executing the cell, will launch the analysis workflow as described above.


### 4. Generated result files

The function will create a number of result files, which are stored in the
subfolder `analysis__cell_env`. For each FQ result file, a separate subfolder 
with name of this file is created. In this folder the different histograms are 
summarized 

-   **`histogram__PIX.csv`**. Contains PIXEL histograms for all regions, e.g. 
    number of pixels in the defined equi-distant zones around the regions. 
    These values are used for renormalization. First column is the center of histogram bin (in pixel).

-   **`histogram__RNA.csv`**. Contains RNA counts per equi-distant zone for all regions.

-   **`histogram__RNA_norm.csv`**. Contains renormalized RNA counts per equi-distant 
    zone for all regions.

    
In this folder, results for **each region** are stored
Results files have the full name of the FQ file with the following prefixes

-   **`histogram__reg_i.csv`**, histograms for region `i`. 
    Contains the spatial expression gradient as a table:

    -   1st col: center of histogram bins (in pixel).
    -   2nd col: RNA counts
    -   3rd col: Pixel counts
    -   4th col: Normalize counts.

-   **`histogram_summary__reg_i.png`**, summary image of for region `i`. First row shows
    smFISH image, mask of region, distance transform (distance from region). Second row 
    shows the raw histograms for RNAs and pixels, as well as the renormalized histogram. 
