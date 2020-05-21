# RNA detection with FISH-quant

## FISH-quant
[**FISH-quant**](https://bitbucket.org/muellerflorian/fish_quant/) is a Matlab toolbox to
localize RNAs in 3D from smFISH images.

<img src="https://raw.githubusercontent.com/muellerflorian/walesky-rna-loc-liver/master/docs/img/fq-screenshot.png" width="600px"></img>


## Detection of individual RNAs

Below only a quick summary of the analysis steps is presented. For more details consult the <a href="https://bitbucket.org/muellerflorian/fish_quant/src/master/Documentation/FISH_QUANT_v3.pdf" target="_blank">**FQ manual.**</a>.

1.  Open FQ
2.  Set analysis folder to folder containing the image that should be analysed:
    `Menu Folder` > `Set root folder`)
3.  Open image that should be analysed.
4.  [Optional] Draw outline of embryo / cells / structure of interest. If you omit  t his step, RNAs will be detected in the entire image. 
    1.  Open dedicated interface: 	Button	`Define outlines`
    2.  Draw a new cell: Button	`New cell`
    3.  Save outline: Button	`Quick-save`
    4.  Return to main FQ: Button 	`Finished`
5.  Filter image (default filter with `LoG` works usually well).
6.  Inspect image. On the right part of the interface select `Filtered image`,
    disable `outline`, and double click on the image. This will show a maximum
    intensity projection of the filtered image in a separate window. Here, you can
    change the contrast and zoom. In order to determine an appropriate threshold
    in the next step, determine a generous range of intensities range corresponding
    to the individual RNA molecules.
7.  Set **pre-detection settings**. FQ will test how many RNAs are detected with a
    range of user-defined intensity thresholds (based on the manual inspection of
    the image from above).

    1. Open dedicated interface:	Button `Detect`
    0. In the user-dialog change the first two parameter: minimum and maximum
           threshold to test. We usually use a minimum value that’s somewhat lower
           than the lowest RNAs to also consider intensity value corresponding to background.
    0. FQ will calculate the number of detected RNAs for a range of values in
           this interval. Depending on the size of the image, this can take a little while. Once done, a plot with the number of detected RNAs as a function of the different thresholds is shown. If the specified range is not appropriate, it can be changed in this interface the computation be repeated.
    0. Ideally, this curve shows a plateau for a value range corresponding to a
           good detection threshold. If that’s not the case, a reasonable value
           corresponding to a visual assessment of what individual RNAs are should be chosen. A pre-detection with a given detection threshold can be perform and the results be inspected in a separate window.

      One other parameter that could be important to adjust is the **cropping region** around each RNA that is considered for analysis and fitting. Reducing this size allows sometimes to better detect closely spaced RNAs but at the cost of an  imprecision in the fit. For most applications a value of +/- 2 voxels in XY and Z are a good compromise.

8.  Once you are satisfied with the settings press on `Perform detection for all cells` to return the main window.
9.  Press button `Fit` to fit each detected spot with a 3D Gaussian function.
10. [Optional]. You can set threshold values for the different fitting parameters,
    e.g. remove spots with very small or very large standard deviations.
11. You can now save the detection settings: `[FQ] Main`>`Save`>`Save detection settings`.
    As a file-name specify `FQ__settings_MATURE.txt`
12. If you are satisfied with these detection results, you can save them directly:  `[FQ] Main`>`Save`>`Detection spots [All]`.


