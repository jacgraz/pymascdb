import warnings
"""
Miscellaneaous auxiliary functions


TODO: Make sure that all functions here are integrated in  api.py
IMPORTANT: keep up to date with eventual name change of variables


"""


####--------------------------------------------------------------------------.
#######################
#### Snowflake class ## 
#######################
def get_snowflake_class_name_dict(method='Praz2017'):
    """
    Get hydrometeor class ID from label name according to a given hydrometeor classif method.

    Parameters
    ----------
    method : str, optional
        hydro class method. 
        The default is 'Praz2017' based on https://amt.copernicus.org/articles/10/1335/2017/.

    Returns
    -------
    dict : TYPE
        DESCRIPTION.

    """
    if method == 'Praz2017':
        dict = {
                'small_particle':1,
                'columnar_crystal':2,
                'planar_crystal':3,
                'aggregate':4,
                'graupel':5,
                'columnar_planar_combination':6,    
               }
    else:
        raise ValueError("Snowflake class dictionary not available for method {}.".format(method))

    return dict

def get_snowflake_class_name_colors_dict(method='Praz2017'):
    if method == 'Praz2017':
        dict = {'small_particle':'forestgreen', 
                'columnar_crystal': 'darkblue',
                'planar_crystal': 'red',  
                'aggregate': 'orange',  
                'graupel': 'yellow', 
               'columnar_planar_combination': 'gray',
               }
    else:
        raise ValueError("Snowflake class dictionary not available for method {}.".format(method))
    
    return dict

def get_snowflake_class_id_dict(method='Praz2017'):    
    dict = get_snowflake_class_name_dict(method=method)
    dict = {v: k for k, v in dict.items()} 
    return dict

def get_snowflake_class_id_colors_dict(method='Praz2017'):    
    colors_dict = get_snowflake_class_name_colors_dict(method=method)
    name_dict = get_snowflake_class_name_dict(method=method)
    dict = {name_dict[k]: v for k, v in colors_dict.items()} 
    return dict

####--------------------------------------------------------------------------.
####################
#### Riming class ## 
####################
def get_riming_class_name_dict(method='Praz2017'):
    """
    Get riming class ID from riming name
    according to a given hydrometeor classif method

    Input:

        method: hydro class method. Default Praz2017 based on
        https://amt.copernicus.org/articles/10/1335/2017/

    """
    if method == 'Praz2017':
        dict = {
                'undefined':0,
                'unrimed':1,
                'rimed':2,
                'densely_rimed':3,
                'graupel-like':4,
                'graupel':5
               }
    else:
        raise ValueError("Riming class dictionary not available for method {}.".format(method))

    return dict

def get_riming_class_name_colors_dict(method='Praz2017'):
    if method == 'Praz2017':
        dict = {'undefined': "forestgreen",
                'unrimed': 'darkblue',
                'rimed': 'red',  
                'densely_rimed': "orange",
                'graupel-like': "yellow",
                'graupel': "gray", 
                }
    else:
        raise ValueError("Riming class dictionary not available for method {}.".format(method))
    
    return dict
    
def get_riming_class_id_dict(method='Praz2017'):
    dict = get_riming_class_name_dict(method=method)
    dict = {v: k for k, v in dict.items()} 
    return dict

def get_riming_class_id_colors_dict(method='Praz2017'):    
    colors_dict = get_riming_class_name_colors_dict(method=method)
    name_dict = get_riming_class_name_dict(method=method)
    dict = {name_dict[k]: v for k, v in colors_dict.items()} 
    return dict

####--------------------------------------------------------------------------.
#####################
#### Melting class ## 
#####################
def get_melting_class_name_dict(method='Praz2017'):
    # TODO : doc string as above (and adapt class names ;) 
    if method == 'Praz2017':
        dict = {'undefined': 0,  # TODO: UPDATE 
                'dry': 1,
                'melting':2,
               }
    else:
        raise ValueError("Melting class dictionary not available for method {}.".format(method))

    return dict

def get_melting_class_name_colors_dict(method='Praz2017'):
    if method == 'Praz2017':
        dict = {'undefined': "forestgreen",
                'dry': 'darkblue',
                'melting': 'orange',  
                }
    else:
        raise ValueError("Melting class dictionary not available for method {}.".format(method))
    
    return dict

def get_melting_class_id_dict(method='Praz2017'):
    dict = get_melting_class_name_dict(method=method)
    dict = {v: k for k, v in dict.items()} 
    return dict

def get_melting_class_id_colors_dict(method='Praz2017'):    
    # TODO : doc string as above 
    colors_dict = get_melting_class_name_colors_dict(method=method)
    name_dict = get_melting_class_name_dict(method=method)
    dict = {name_dict[k]: v for k, v in colors_dict.items()} 
    return dict

####--------------------------------------------------------------------------.
############################
#### Precipitation Class ###
############################
def get_precip_class_name_dict(method='Schaer2020'):
    # TODO : doc string as above (and adapt class names ;) 
    if method == 'Schaer2020':
        dict = {
                'undefined': 0,
                'precip': 1,
                'mixed': 2, 
                'blowing_snow': 3,
               }
    else:
        raise ValueError("Precipitation class dictionary not available for method {}.".format(method))

    return dict

def get_precip_class_name_colors_dict(method='Praz2017'):
    if method == 'Schaer2020':
        dict = {'undefined': "forestgreen",
                'precip': 'darkblue',
                'mixed': 'orange',  
                'blowing_snow': 'yellow',  
                }
    else:
        raise ValueError("Precipitation class dictionary not available for method {}.".format(method))
    
    return dict

def get_precip_class_id_dict(method='Schaer2020'):
    dict = get_precip_class_name_dict(method=method)
    dict = {v: k for k, v in dict.items()} 
    return dict

def get_precip_class_id_colors_dict(method='Schaer2020'):    
    colors_dict = get_precip_class_name_colors_dict(method=method)
    name_dict = get_precip_class_name_dict(method=method)
    dict = {name_dict[k]: v for k, v in colors_dict.items()} 
    return dict


####--------------------------------------------------------------------------.
####################### 
#### Campaign Utils ###
#######################
def get_campaign_colors_dict():
    d_c = {'APRES3-2016': "forestgreen",
           'APRES3-2017': "lightgreen",
           'Davos-2015': 'darkblue',
           'Davos-2019': 'lightblue',
           'Valais-2016': 'turquoise',
           'ICEPOP-2018': "violet",
           'PLATO-2019': "pink",
           'Jura-2019': "orange",
           'POPE-2020': "yellow", 
           'ICEGENESIS-2021': "red",
           }
    return d_c

def get_campaign_names():
    # TODO : doc string as above (and adapt class names ;) 
    l = list(get_campaign_colors_dict().keys())
    return l

####--------------------------------------------------------------------------.
##############
#### Units ###
##############

def get_units():
    """
    Get a dictionary with the units of the variables contained in the databases
    """

    units = {'datetime':      'datetime',
             'index':         '-',
             'flake_id':      '-',
             'flake_number_tmp':'-',
             'pix_size':      'm',
             'quality_xhi':   '-',

             'n_roi'   :      '-',
             'area'    :      'm**2',
             'perim'   :      'm',
             'Dmean'   :      'm',
             'Dmax'    :      'm',   
             'eq_radius':     'm',
             'area_porous':   'm**2',
             'area_porous_r': '-',
             'ell_fit_A':     'm',
             'ell_fit_B':     'm',
             'ell_fit_area':  'm**2',
             'ell_fit_ori':   'deg',
             'ell_fit_ecc':   '-',
             'compactness':   '-',
             'ell_in_A':     'm',
             'ell_in_B':     'm',
             'ell_in_area':  'm**2',
             'ell_out_A':     'm',
             'ell_out_B':     'm',
             'ell_out_area':  'm**2',
             'roundness':     '-',
             'p_circ_out_r':  '-',
             'rectangularity':'-',
             'bbox_width':    'm',
             'bbox_len':      'm',
             'rect_perim_ratio':  '-',
             'rect_aspect_ratio': '-',
             'rect_eccentricity': '-',
             'solidity':          '-',
             'convexity':         '-',
             'hull_n_angles':     '-',
             'p_circ_r':          '-',
             'frac_dim_boxcounting': '-',
             'frac_dim_theoretical': '-',
             'nb_holes':             '-',
             'skel_N_ends':       '-',
             'skel_N_junc' :      '-',
             'skel_perim_ratio':  '-',
             'skel_area_ratio':   'pix**-1',
             'sym_P1':            '-',
             'sym_P2':            '-',
             'sym_P3':            '-',
             'sym_P4':            '-',
             'sym_P5':            '-',
             'sym_P6':            '-',
             'sym_Pmax_id':       '-',
             'sym_P6_max_ratio':  '-',
             'sym_mean':         'pix',
             'sym_std':          'pix',
             'sym_std_mean_ratio': '-',
             'intensity_mean':     '-',
             'intensity_max':      '-',
             'contrast':           '-',
             'intensity_std':      '-',
             'hist_entropy':       '-',
             'local_std':          '-',
             'local_intens':       '-',
             'lap_energy':         '-',
             'wavs':               '-',
             'complexity':         '-',
             'har_energy':         '-',
             'har_contrast':       '-',
             'har_corr':           '-',
             'har_hom':            '-',
             'roi_centroid_X':     'pix',
             'roi_centroid_Y':     'pix',
             'roi_width':          'pix',
             'roi_height':         'pix',
             'Dmax_ori':           'deg',
             'Dmax_90':            'm',
             'D90_r':              '-',
             'riming_class_id':    'class',
             'riming_class_prob': '-',
             'riming_class_name':  'class string',
             'riming_deg_level':   '-',
             'melting_class_id':   'boolean',
             'melting_class_name': 'class_string',
             'melting_prob':       '-',
             'snowflake_class_name':'class string',
             'snowflake_class_id':  'class',
             'snowflake_class_prob': '-',

             'fallspeed':          'm s**-1',
             'campaign':           '-',
             'latitude':           'deg_north',
             'longitude':          'deg_east',
             'altitude':           'm',
             'flake_quality_xhi':  '-',
             'flake_Dmax':         'm',


             'gan3d_mass':         'kg',
             'gan3d_volume':       'm**3',
             'gan3d_gyration':     'm',

             'bs_nor_angle':       '-',
             'bs_mix_ind':         '-',
             'bs_precipitation_class': 'class string',

             'env_T':              'deg C',
             'env_P':              'hPa',
             'env_DD':             'deg',
             'env_FF':             'm s**-1',
             'env_RH':             '%'
             }
    return units


####--------------------------------------------------------------------------.
###########################
#### Dataframe columns  ###
###########################

def get_vars_gan3d():
    variables = ['gan3d_mass',
                 'gan3d_vol_ch', 
                 'gan3d_r_g',
                 ]
    return variables

def get_vars_env():
    variables = ['env_T',
                 'env_P',
                 'env_DD',
                 'env_FF',
                 'env_RH',
                 ]
    return variables

def get_vars_blowing_snow():
    variables = ['bs_nor_angle',
                 'bs_mix_ind',
                 'bs_precip_type',
                 ]
    return variables 

def get_vars_location(): 
    variables = ['datetime',
                 'campaign',
                 'latitude',
                 'longitude',
                 'altitude',
                ]
    return variables 

def get_vars_class(): 
    variables = ['riming_class_name',
                 'riming_class_id',
                 'riming_class_id_prob', 
                 'riming_deg_level', 
                 'melting_class_id',
                 'melting_class_name',
                 'melting_prob', 
                 'snowflake_class_name', 
                 'snowflake_class_id',
                 'snowflake_class_id_prob',
                 ]
    return variables

def get_vars_class_ids(): 
   variables = ['snowflake_class_id',
                'riming_class_id',
                'melting_class_id',   
               ]
   return variables

def get_vars_class_names():
    variables = ['snowflake_class_name', 
                 'riming_class_name',
                 'melting_class_name', 
                ]
    return variables


def get_vars_cam_info(): 
    variables = ['index', 
                 'datetime',
                 'flake_id', 
                 'flake_number_tmp',
                 'pix_size',
                 'cam_id',
                 'quality_xhi'
                 # event_id
                 # event_duration 
                ]
    return variables 

def get_vars_cam_descriptors(): 
    # TODO: Or to infer from self.cam0.columns - get_vars_cam_info() - get_vars_class()
    # --> So that works if people add stuff ... 
    variables = ['n_roi', 'area', 'perim', 'Dmean', 'Dmax', 'eq_radius',
                'area_porous', 'area_porous_r', 'ell_fit_A', 'ell_fit_B',
                'ell_fit_area', 'ell_fit_ori', 'ell_fit_a_r', 'ell_fit_ecc',
                'compactness', 'ell_in_A', 'ell_in_B', 'ell_in_area', 'ell_out_A',
                'ell_out_B', 'ell_out_area', 'roundness', 'p_circ_out_r',
                'rectangularity', 'bbox_width', 'bbox_len', 'rect_perim_ratio',
                'rect_aspect_ratio', 'rect_eccentricity', 'solidity', 'convexity',
                'hull_n_angles', 'p_circ_r', 'frac_dim_boxcounting',
                'frac_dim_theoretical', 'nb_holes', 'skel_N_ends', 'skel_N_junc',
                'skel_perim_ratio', 'skel_area_ratio', 'sym_P1', 'sym_P2',
                'sym_P3', 'sym_P4', 'sym_P5', 'sym_P6', 'sym_Pmax_id',
                'sym_P6_max_ratio', 'sym_mean', 'sym_std', 'sym_std_mean_ratio',
                'intensity_mean', 'intensity_max', 'contrast', 'intensity_std',
                'hist_entropy', 'local_std', 'local_intens', 'lap_energy', 'wavs',
                'complexity', 'har_energy', 'har_contrast', 'har_corr', 'har_hom',
                'roi_centroid_X', 'roi_centroid_Y', 'roi_width', 'roi_height',
                'Dmax_ori', 'Dmax_90', 'D90_r', 
                ]
    return variables 
  
 


    
    
       
 