
This is a collection of analysis tools to study RNA localization from single
molecule FISH (smFISH) images. These tools were developed in the **context of RNA
localization in liver**, but can likely be applied for different questions as well.

We provide different analysis workflows (listed in the banners above ).
For each we specify the required installations, and detailed Instructions
for how run these workflows and what results are typically obtained.

__General analysis workflow__

1. The tools require a very specific data organziation that we specify
2. RNA detection is performed with FISH-quant in Matlab.
3. Post-processing is performed with ImJoy plugins. 


## ImJoy plugins
Most of the workflows are implemented as **ImJoy plugins**, with a simple interface to
specify the different workflow parameters. We describe in a dedicated [section](tools-imjoy.md) how to **use ImJoy** and the **Plugin engine** to run these plugins. 

!!! abstract "Quick summary for how to connect ImJoy to Jupyter engine"
    1. Open **anaconda terminal**. 
    2. **Activate environment**: `conda activate rna-loc-liver`
    3. **Start Jupyter engine**: `imjoy --jupyter`
    4. **Connect** ImJoy to Jupyter Engine with 🚀 button.

We also provide **Jupyter notebooks** for these workflows, which we recommend only for more experienced Python users. 