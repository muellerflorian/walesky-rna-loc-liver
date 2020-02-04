# -*- coding: utf-8 -*-

# IMPORTS
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import os
import numpy as np
import json
from skimage import io
from scipy import ndimage
from skimage.io import imread, imsave

from fqa import toolbox

# Turn off warnings occuring when saving images
import warnings
warnings.filterwarnings("ignore", message=".*(is a low contrast image)")



def folder_scan_process(folder_root,region_labels,log_msg_callback = None,log_prog_callback=None):
    ''' Scan folders an process when annotation file is present'''

    # Recursive search of specified directory
    folders_proc = []
    for root, dirnames, filenames in os.walk(folder_root):
        for filename in filenames:
            if filename == "annotation.json" :
                folders_proc.append(root)

    for folder_process in folders_proc:
        toolbox.log_message(f'\n\n Processing folder: {folder_process}',callback_fun=log_msg_callback)
        process_folder(folder_process,region_labels,log_msg_callback=log_msg_callback,log_prog_callback=log_prog_callback)



def process_folder(folder_process,region_labels,log_msg_callback = None,log_prog_callback=None):
    '''
    Process folder containing FQ analysis results and an ImJoy annotation.
    '''

    # Open annotations and create masks
    annotation_file = os.path.join(folder_process,"annotation.json")
    data_json, img_size = toolbox.read_annotation(annotation_file)

    # Note that coordinates are exchanged and y flipped
    for feat_idx, feat in enumerate(data_json['features']):
        label = feat['properties']['label']

        if label == region_labels[0]:
            toolbox.log_message(f'Annotation for first region ({region_labels[0]}) found',callback_fun=log_msg_callback)
            cv_pos = np.squeeze(np.asarray(feat['geometry']['coordinates']))
            cv_pos[:,[0, 1]] = cv_pos[:,[1, 0]]
            cv_pos[:,0] = -1*cv_pos[:,0]+img_size[0]
            reg1_mask = toolbox.make_mask(cv_pos,img_size)

        elif label == region_labels[1]:
            toolbox.log_message(f'Annotation for second region ({region_labels[1]}) found',callback_fun=log_msg_callback)
            pl_pos = np.squeeze(np.asarray(feat['geometry']['coordinates']))
            pl_pos[:,[0, 1]] = pl_pos[:,[1, 0]]
            pl_pos[:,0] = -1*pl_pos[:,0]+img_size[0]
            reg2_mask = toolbox.make_mask(pl_pos,img_size)

    ### Make masks and measure distance of P.L. to C.V.

    # Assemble distance map: outside positive, inside negative
    reg1_mask_distTrans_inside = ndimage.distance_transform_edt(reg1_mask)
    reg1_mask_distTrans_outside = ndimage.distance_transform_edt(~reg1_mask.astype(bool))

    reg1_mask_distTrans = np.copy(reg1_mask_distTrans_outside)
    reg1_mask_distTrans[reg1_mask_distTrans_inside>0] = -reg1_mask_distTrans_inside[reg1_mask_distTrans_inside>0]

    # Center of mass of region 2 (portal lobe)
    reg2_com      = np.asarray(ndimage.measurements.center_of_mass(reg2_mask.astype(bool))).astype('int')
    reg2_distReg1 = reg1_mask_distTrans[reg2_com[0],reg2_com[1]]


    # Loop over all FQ result files
    for file in os.listdir(folder_process):
        if '_spots_' in file:

            file_open = os.path.join(folder_process,file)
            toolbox.log_message(f'\n Opening FQ file: {file_open}',callback_fun=log_msg_callback)

            # Get information (path, file name) to save results
            drive, path_and_file = os.path.splitdrive(file_open)
            path, file = os.path.split(path_and_file)
            file_base, ext = os.path.splitext(file)

            path_save = os.path.join(drive,path, 'analysis__exprGradient')
            toolbox.log_message(f'Results will be saved in folder: {path_save}',callback_fun=log_msg_callback)
            if not os.path.isdir(path_save):
                os.makedirs(path_save)

            fq_dict = toolbox.read_FQ_matlab(file_open)
            spots_all = toolbox.get_rna(fq_dict)
            spots_pos = spots_all[:,[16, 17]].astype('int')

            # Open FISH image
            file_FISH_img = os.path.join(folder_process,fq_dict['file_names']['smFISH'])
            toolbox.log_message(f'Reading FISH image: {file_FISH_img}',callback_fun=log_msg_callback)
            img_FISH  = imread(file_FISH_img)

            ## Generate density plots
            name_save = os.path.join(path_save, '_summary_density__' + file_base +  '.png')
            img_density,img_density_outline,img_outline = toolbox.calc_expression_density_plot(fq_dict ,img_size,name_save=name_save,log_msg_callback=log_msg_callback,log_prog_callback=log_prog_callback)

            #Save density image
            imsave(os.path.join(path_save, 'img_density__' + file_base +  '.tif'),img_density)
            imsave(os.path.join(path_save, 'img_density_outline__' + file_base +  '.tif'),img_density_outline)
            imsave(os.path.join(path_save, 'img_outline__' + file_base +  '.tif'),img_outline)


            ### Distance measurements

            # Distance of all RNAs to region 1, RNAs inside the region have negative values
            RNAdist = reg1_mask_distTrans[spots_pos[:,0],spots_pos[:,1]]

            # Renormalize distance map and RNA distances
            reg1_mask_distTrans_norm = np.divide(reg1_mask_distTrans,reg2_distReg1)
            RNAdist_norm = np.divide(RNAdist,reg2_distReg1)

            # Bins for histogram
            RNAdist_norm_max = np.amax(RNAdist_norm)
            RNAdist_norm_min = np.amin(RNAdist_norm)
            bins=np.arange(np.around(RNAdist_norm_min,1)-0.1,RNAdist_norm_max+0.1,0.1)
            width = 0.8 * (bins[1] - bins[0])
            center = (bins[:-1] + bins[1:]) / 2

            # Histogram of RNA distances
            count_RNA, bins = np.histogram(RNAdist_norm, bins=bins,density=False)

            # Renormalize considering how many pixels are really in the actual image
            count_pix = np.diff(list(map(lambda threshold: np.sum(reg1_mask_distTrans_norm <= threshold),bins)))

            # Renormalize RNA counts with respect to area
            count_RNA_normArea = count_RNA/count_pix

            # Renormalize to have sum 1
            hist_sum = np.nansum(count_RNA_normArea)*((bins[1] - bins[0]))
            count_RNA_normSum = np.divide(count_RNA_normArea,hist_sum)

            # Summarize all histograms
            hist_all = np.stack((center,count_RNA_normSum,count_RNA,count_pix),axis=1)

            # Save file with histogram
            np.savetxt(os.path.join(path_save, 'hist_expression__' + file_base +  '.txt'), hist_all, fmt='%f \t %f \t %f \t %f',header='Dist_norm [um]\tCOUNTS_RAW\tCOUNTS_NORM_sum\tPIXEL_COUNTS')

            # Plot results and save figure

            # PLOT ROI and center of mass
            fig1, ax = plt.subplots(3,2,num='dist_enrich')
            fig1.set_size_inches((15,12))

            # Plot image with region of interest and reference point
            img1 = ax[0][0].imshow(img_FISH,cmap="hot")
            plt.sca(ax[0][0])   # set current axis
            plt.title('Region 1 (green) and 2 (blue)')
            ax[0][0].plot(pl_pos[:,1], pl_pos[:,0], '-b')
            ax[0][0].plot(cv_pos[:,1], cv_pos[:,0], '-g')
            ax[0][0].scatter(reg2_com[1],reg2_com[0],color='b')
            ax[0][0].get_xaxis().set_visible(False)
            ax[0][0].get_yaxis().set_visible(False)
            toolbox.colorbar(img1)

            # Plot image with region of interest and reference point
            img1 = ax[0][1].imshow(img_density,cmap="hot")
            plt.sca(ax[0][1])   # set current axis
            plt.title('Region 1 (green) and 2 (blue)')
            ax[0][1].plot(pl_pos[:,1], pl_pos[:,0], '-b')
            ax[0][1].plot(cv_pos[:,1], cv_pos[:,0], '-g')
            ax[0][1].scatter(reg2_com[1],reg2_com[0],color='b')
            ax[0][1].get_xaxis().set_visible(False)
            ax[0][1].get_yaxis().set_visible(False)
            toolbox.colorbar(img1)


            # Plot distance map and pixel distance histogram
            img3 = ax[1][0].imshow(reg1_mask_distTrans_norm,cmap="hot")
            plt.sca(ax[1][0])
            plt.title('Renormalized distance from region 1')
            ax[1][0].plot(pl_pos[:,1], pl_pos[:,0], '-b')
            ax[1][0].plot(cv_pos[:,1], cv_pos[:,0], '-g')
            ax[1][0].scatter(reg2_com[1],reg2_com[0],color='b')
            ax[1][0].get_xaxis().set_visible(False)
            ax[1][0].get_yaxis().set_visible(False)
            toolbox.colorbar(img3)

            ax[1][1].bar(center, count_pix, align='center', width=width)
            ax[1][1].set_xlabel('Distance [pixel]')
            ax[1][1].set_ylabel('# pixel')
            ax[1][1].title.set_text('Histogram of all pixel distances')


            # Plot histograms
            ax[2][0].bar(center, count_RNA, align='center', width=width)
            ax[2][0].set_xlabel('Distance [pixel]')
            ax[2][0].set_ylabel('# RNAs')
            ax[1][0].title.set_text('Histogram without normalization')

            ax[2][1].bar(center, count_RNA_normSum, align='center', width=width)
            ax[2][1].set_xlabel('Normalized distance')
            ax[2][1].set_ylabel('Expression level [a.u.]')
            ax[2][1].title.set_text('Histogram: normalized with area and sum 1')

            fig1.tight_layout(h_pad=0.2)
            plt.draw()

            plt.savefig(os.path.join(path_save, '_summary_gradient_' + file_base +  '.png'),dpi=200)
            plt.close()

    toolbox.log_message(f'Finished processing data!',callback_fun=log_msg_callback)


def process_file(file_open, img_size):
    """
    Analyzes the specified file.
    """

    # Get information (path, file name) to save results
    drive, path_and_file = os.path.splitdrive(file_open)
    path, file = os.path.split(path_and_file)
    file_base, ext = os.path.splitext(file)

    path_save = os.path.join(path, 'analysis_exprdensity')
    if not os.path.isdir(path_save):
        os.makedirs(path_save)

    # Some infos
    print('\n=== Processing file')
    print(file)

    # Open FQ results file
    fq_dict = read_FQ_matlab(file_open)
    spots_all = get_rna(fq_dict)

    # Generate density plots
    print('\n===  Generating density plots')
    img_density,img_density_outline,img_outline = calc_expression_density_plot(fq_dict ,img_size,flag_plot=True)
    plt.figure('density_plt')
    plt.savefig(os.path.join(path_save, 'summary_density__' + file_base +  '.png'),dpi=600)
    plt.close('density_plt')

    # Save density image
    print('-- Saving density plots')

    io.imsave(os.path.join(path_save, 'img_density__' + file_base +  '.tif'),img_density)
    io.imsave(os.path.join(path_save, 'img_density_outline__' + file_base +  '.tif'),img_density_outline)
    io.imsave(os.path.join(path_save, 'img_outline__' + file_base +  '.tif'),img_outline)

    # Select roi
    print('\n=== Select region for calculation of reference point')
    # FROM https://github.com/jdoepfert/roipoly.py
    fig, (ax1) = plt.subplots()
    ax1.imshow(img_density,cmap="hot")
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    MyROI = roipoly(roicolor='g')
    plt.draw()
    plt.close()

    # Analyze distance distribution
    print('==  Analyzing distance distribution')
    ROImask = MyROI.getMask(img_density)
    ROIcom  = ndimage.measurements.center_of_mass(ROImask)
    fq_dict['ref_pos'] = {'com' : ROIcom, 'x':MyROI.allxpoints,'y':MyROI.allypoints}

    hist_all = calc_dist_enrichment(ROIcom,spots_all[:,[16, 17]],img_size,img_density=img_density,flag_plot=True)
    plt.figure('dist_enrich')
    plt.savefig(os.path.join(path_save, 'summary_expgradient__' + file_base +  '.png'),dpi=600)
    plt.close('dist_enrich')

    # Save file with histogram
    np.savetxt(os.path.join(path_save, 'hist_expression__' + file_base +  '.txt'), hist_all, fmt='%10d \t %10d \t %10f \t %10f',header='Dist [um]\tCOUNTS_RAW\tCOUNTS_norm_area\tCOUNTS_NORM_pixel')

    # Save everything to json to be reloaed later if needed
    file_json = os.path.join(path_save, 'fqdict_' + file_base +  '.json')
    with open(file_json,'w') as fp:
        json.dump(fq_dict, fp, cls=NumpyEncoder)
