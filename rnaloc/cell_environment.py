# -*- coding: utf-8 -*-

# IMPORTS
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import ndimage
import matplotlib.pyplot as plt
from skimage.io import imread

from rnaloc import toolbox


# Function definition
def process_folder(path_scan, 
                   region_label, 
                   bin_prop,
                   annotation_file='annotation.json',
                   output_path='acquisition>>analysis',
                   callback_log=None,
                   callback_status=None,
                   callback_progress=None):
    """[summary]
    TODO: add docstring
    Parameters
    ----------
    path_scan : [type]
        [description]
    annotation_file : str, optional
        [description], by default 'annotation.json'
    """

    # Print all input parameters
    toolbox.log_message(f"Function (process_folder) called with: {str(locals())} ", callback_fun=callback_log)

    # Created bins for histogram
    bins_hist = np.arange(bin_prop[0], bin_prop[1], bin_prop[2])
    bins_width = 0.8 * (bins_hist[1] - bins_hist[0])
    bins_center = (bins_hist[:-1] + bins_hist[1:]) / 2

    for p_annotation in path_scan.rglob(f'*{annotation_file}*'):

        # Get sample path
        path_sample = p_annotation.parents[0]
        toolbox.log_message(' ', callback_fun=callback_log)
        toolbox.log_message(f'>> Analyzing {p_annotation}', callback_fun=callback_log)

        # Open annotation
        file_read = path_sample / annotation_file
        if not p_annotation.is_file():
            print(f'Annotation not found: {p_annotation}')
            return

        data_json, img_size = toolbox.read_annotation(p_annotation)

        # Calculate distance transform for each annotated cell
        # Note that coordinates are exchanged and y flipped
        n_regs = 0
        toolbox.log_message(f'  [Create distance maps]: Loop over regions with label: {region_label}', callback_fun=callback_log)      

        if callback_status:
            callback_status(f'  [Create distance maps]: Loop over regions with label: {region_label}')

        n_feats = len(data_json['features'])
        
        for feat_ind, feat in enumerate(tqdm(data_json['features'], total=n_feats)): 
            label = feat['properties']['label']

            if callback_progress:
                callback_progress(feat_ind/n_feats)

            if label == region_label:
                reg_pos = np.squeeze(np.asarray(feat['geometry']['coordinates']))
                reg_pos[:, [0, 1]] = reg_pos[:, [1, 0]]
                reg_pos[:, 0] = -1*reg_pos[:, 0]+img_size[0]
                mask_loop = toolbox.make_mask(reg_pos, img_size)

                dist_nuc = ndimage.distance_transform_edt(np.logical_not(mask_loop))
                
                if n_regs == 0:
                    dist_mat = np.copy(dist_nuc.astype('uint16'))
                    reg_masks = np.copy(mask_loop.astype('bool'))
                else:
                    dist_mat = np.dstack((dist_mat, dist_nuc.astype('uint16')))
                    reg_masks = np.dstack((reg_masks, mask_loop.astype('bool')))

                n_regs += 1

        toolbox.log_message(f'   Number of annotated regions: {n_regs}', 
                            callback_fun=callback_log)    

        if n_regs == 0:
            toolbox.log_message(f'WARNING.\nNO regions with label {region_label} found. Is this label correct?',
                                callback_fun=callback_log) 
            continue

        # Loop over all FQ result files
        for p_fq in path_sample.glob('*_spots_*'):

                toolbox.log_message(f' \nOpening FQ file: {p_fq}', callback_fun=callback_log)

                # Get information (path, file name) to save results
                file_base = p_fq.stem

                # Load FQ results file
                fq_dict  = toolbox.read_FQ_matlab(p_fq)
                spots_all = toolbox.get_rna(fq_dict)

                # XY positions in pixel
                if len(spots_all) == 0:
                    toolbox.log_message(f'No RNAs detected in this file.', callback_fun=callback_log)
                    continue
                else:
                    pos_rna = np.divide(spots_all[:, 0:2], fq_dict['settings']['microscope']['pix_xy']).astype(int)

                # Open FISH image
                file_FISH_img = path_sample / fq_dict['file_names']['smFISH']
                toolbox.log_message(f'  Reading FISH image: {file_FISH_img}',callback_fun=callback_log)
                img_FISH = imread(file_FISH_img)

                # Folder to save results
                path_save_base = toolbox.create_output_path(path_sample, output_path)
                toolbox.log_message(f' Results will be saved here: {path_save_base}', callback_fun=callback_log)

                path_save = path_save_base / 'analysis__cell_env' / file_base
                toolbox.log_message(f'  Results will be saved in folder: {path_save}',
                                    callback_fun=callback_log)

                if not path_save.is_dir():
                    path_save.mkdir(parents=True)

                path_save_details = path_save / 'per_region'
                if not path_save_details.is_dir():
                    path_save_details.mkdir(parents=True)

                # Matrix with distance to all nuclei: each RNA is one row
                rna_dist_regs_all = dist_mat[pos_rna[:, 0], pos_rna[:, 1], :]

                # Sort matrix with shortest distance in first column
                ind_closest_regs = np.argsort(rna_dist_regs_all, axis=1)  # Index with sorted distance to nuclei

                # Get for each RNA closest nuclei: index and distance
                dist_closest_regs = np.take_along_axis(rna_dist_regs_all, ind_closest_regs, axis=1)

                df_rna_dist = pd.DataFrame({'region_label': ind_closest_regs[:, 0],
                                            'dist': dist_closest_regs[:, 0]
                                            })

                df_hist_RNA_all = pd.DataFrame({'bins_center': bins_center})
                df_hist_PIX_all = pd.DataFrame({'bins_center': bins_center})
                df_hist_RNA_norm_all = pd.DataFrame({'bins_center': bins_center})

                toolbox.log_message(f' [Calculate expression gradients]: Loop over regions', callback_fun=callback_log) 

                if callback_status:
                    callback_status(f'[Calculate expression gradients]: Loop over regions')

                for i_reg in tqdm(range(0, n_regs)):
                    df_loop = df_rna_dist.loc[df_rna_dist['region_label'] == i_reg]

                    if callback_progress:
                        callback_progress(i_reg/n_regs)

                    # Distance transform
                    dist_mat_loop = dist_mat[:, :, i_reg]
                    reg_mask = reg_masks[:, :, i_reg]
                    dist_reg_pix = dist_mat_loop[~reg_mask.astype('bool')]

                    # Indices have to be inversed to access array
                    dist_reg_rna = df_loop['dist'].to_numpy()

                    # Calculate histograms
                    hist_counts_rna, bins = np.histogram(dist_reg_rna, bins_hist, density=False)
                    hist_counts_pix, bins = np.histogram(dist_reg_pix, bins_hist, density=False)

                    hist_counts_rna_norm = hist_counts_rna/hist_counts_rna.sum()
                    hist_counts_pix_norm = hist_counts_pix/hist_counts_pix.sum()

                    hist_counts_rna_norm2 = np.divide(hist_counts_rna_norm,hist_counts_pix_norm)
                    hist_counts_rna_norm2 = np.nan_to_num(hist_counts_rna_norm2)

                    # Histogram 
                    df_hist_RNA_all[f'reg_{i_reg}'] = hist_counts_rna
                    df_hist_PIX_all[f'reg_{i_reg}'] = hist_counts_pix
                    df_hist_RNA_norm_all[f'reg_{i_reg}'] = hist_counts_rna_norm2

                    # Histograms per image
                    df_hist = pd.DataFrame({'bins_center': bins_center,
                                            'counts_rna': hist_counts_rna,
                                            'counts_pix': hist_counts_pix,
                                            'counts_rna_': hist_counts_rna_norm2,
                                            })

                    df_hist.to_csv(path_save_details / f'histogram__reg_{i_reg}.csv',
                                   index=False)

                    # Generate plot
                    fig1, ax = plt.subplots(2, 3, num='Cell environment analysis')
                    fig1.set_size_inches((13, 6))

                    ax[0][0].imshow(img_FISH, cmap="hot")
                    ax[0][0].get_xaxis().set_visible(False)
                    ax[0][0].get_yaxis().set_visible(False)

                    ax[0][1].imshow(reg_mask, cmap="hot")
                    ax[0][1].get_xaxis().set_visible(False)
                    ax[0][1].get_yaxis().set_visible(False)

                    img_dist = ax[0][2].imshow(dist_mat_loop, cmap="hot")
                    ax[0][2].get_xaxis().set_visible(False)
                    ax[0][2].get_yaxis().set_visible(False)
                    toolbox.colorbar(img_dist)

                    ax[1][0].bar(bins_center, hist_counts_rna, align='center', 
                                 width=bins_width)
                    ax[1][0].set_xticks(bins_center)
                    ax[1][0].set_xticklabels(bins_center.astype(int), 
                                             rotation=90, ha='right')
                    ax[1][0].set_xlabel('Distance from region [pixel]')
                    ax[1][0].set_ylabel('# RNAs')
                    plt.xticks(rotation=30, ha='right')

                    ax[1][1].bar(bins_center, hist_counts_pix, align='center', 
                                 width=bins_width)
                    ax[1][1].set_xticks(bins_center)
                    ax[1][1].set_xticklabels(bins_center.astype(int), 
                                             rotation=90, ha='right')
                    ax[1][1].set_xlabel('Distance from region [pixel]')
                    ax[1][1].set_ylabel('# pixels')

                    ax[1][2].bar(bins_center, hist_counts_rna_norm2, 
                                 align='center', width=bins_width)
                    ax[1][2].set_xticks(bins_center)
                    ax[1][2].set_xticklabels(bins_center.astype(int), 
                                             rotation=90, ha='right')
                    ax[1][2].set_xlabel('Distance from region [pixel]')
                    ax[1][2].set_ylabel('Renormalized frequency')

                    plt.tight_layout()
                    plt.savefig(path_save_details / f'hist__reg_{i_reg}.png', dpi=200)

                    #plt.savefig(path_save / f'histogram_summary__reg_{i_reg}.png', 
                    #            dpi=200)
                    plt.close()

                # Save summary histograms
                # TODO: consider including the sample name into the name to save results
                df_hist_RNA_all.to_csv(path_save / f'histogram__RNA.csv',
                                       index=False)
                df_hist_PIX_all.to_csv(path_save / f'histogram__PIX.csv',
                                       index=False)
                df_hist_RNA_norm_all.to_csv(path_save / f'histogram__RNA_norm.csv',
                                            index=False)   

    toolbox.log_message(f'\nProcessing finished!', callback_fun=callback_log)

    if callback_status:
        callback_status(f'Processing finished!')

