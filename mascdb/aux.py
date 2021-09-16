import warnings
"""
Miscellaneaous auxiliary functions


TODO: Make sure that all functions here are integrated in  api.py
IMPORTANT: keep up to date with eventual name change of variables


"""

def get_label_name_dict(method='Praz2017'):
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
        dict ={
            'small_particle':1,
            'columnar_crystal':2,
            'planar_crystal':3,
            'aggregate':4,
            'graupel':5,
            'columnar_planar_combination':6,    
        }
    else:
        warnings.warn("Dictionary not available for given hydro-class method: " + method)

    return dict


def get_label_id_dict(method='Praz2017'):    
    """
    Get hydrometeor label name form class ID
    according to a given hydrometeor classif method

    Input:

        method: hydro class method. Default Praz2017 based on
        https://amt.copernicus.org/articles/10/1335/2017/


    """
    if method == 'Praz2017':
        dict ={
            1:'small_particle',
            2:'columnar_crystal',
            3:'planar_crystal',
            4:'aggregate',
            5:'graupel',
            6:'columnar_planar_combination',    
        }
    else:
        warnings.warn("Dictionary not available for given hydro-class method: "+method)

    return dict

def get_riming_name_dict(method='Praz2017'):
    """
    Get riming class ID from riming name
    according to a given hydrometeor classif method

    Input:

        method: hydro class method. Default Praz2017 based on
        https://amt.copernicus.org/articles/10/1335/2017/


    """

    if method == 'Praz2017':
        dict ={
            'unrimed':1,
            'rimed':2,
            'densely_rimed':3,
            'greupel-like':4,
            'graupel':5
        }
    else:
        warnings.warn("Dictionary not available for given  method: "+method)

    return dict

def get_riming_id_dict(method='Praz2017'):
    """
    Get riming name from riming id
    according to a given hydrometeor classif method

    Input:

        method: hydro class method. Default Praz2017 based on
        https://amt.copernicus.org/articles/10/1335/2017/


    """

    if method == 'Praz2017':
        dict ={
            1:'unrimed',
            2:'rimed',
            3:'densely_rimed',
            4:'graupel-like',
            5:'graupel'
        }
    else:
        warnings.warn("Dictionary not available for given method: "+method)

    return dict



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
             'sym_P0':            '-',
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
             'riming_id':          'class',
             'riming_id_prob':     '-',
             'riming_name':        'class string',
             'riming_deg_level':   '-',
             'melting_id':         'boolean',
             'melting_prob':       '-',
             'snowflake_class_name':'class string',
             'snowflake_class_id':  'class',
             'snowflake_class_id_prob': '-',

             'fallspeed':          'm s**-1',
             'campaign':           '-',
             'latitude':           'deg_north',
             'longitude':          'deg_east',
             'altitude':           'm',
             'quality_xhi_flake':  '-',


             'gan3d_mass':         'kg',
             'gan3d_vol_ch':       'm**3',
             'gan3d_gyration':     'm',

             'bs_nor_angle':       '-',
             'bs_mix_ind':         '-',
             'bs_precip_type':     'class string',

             'env_T':              'deg C',
             'env_P':              'hPa',
             'env_DD':             'deg',
             'env_FF':             'm s**-1',
             'env_RH':             '%'
             }
    return units

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
    variables = ['riming_name',
                 'riming_id',
                 'riming_id_prob', 
                 'riming_deg_level', 
                 'melting_id',
                 'melting_prob', 
                 'snowflake_class_name', 
                 'snowflake_class_id',
                 'snowflake_class_id_prob',
                 ]
    return variables

def get_vars_class_ids(): 
   variables = ['riming_id',
                'melting_id',   
                'snowflake_class_id',
               ]
   return variables

def get_vars_class_names():
    variables = ['riming_name',
                'snowflake_class_name', 
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
                'skel_perim_ratio', 'skel_area_ratio', 'sym_P0', 'sym_P1', 'sym_P2',
                'sym_P3', 'sym_P4', 'sym_P5', 'sym_P6', 'sym_Pmax_id',
                'sym_P6_max_ratio', 'sym_mean', 'sym_std', 'sym_std_mean_ratio',
                'intensity_mean', 'intensity_max', 'contrast', 'intensity_std',
                'hist_entropy', 'local_std', 'local_intens', 'lap_energy', 'wavs',
                'complexity', 'har_energy', 'har_contrast', 'har_corr', 'har_hom',
                'roi_centroid_X', 'roi_centroid_Y', 'roi_width', 'roi_height',
                'Dmax_ori', 'Dmax_90', 'D90_r', 
                ]
    return variables 
  
 


    
    
       
 