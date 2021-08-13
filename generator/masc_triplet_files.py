from datetime import datetime, timedelta
import sys
import fnmatch
import os

import numpy as np
from scipy import io as sio
import pandas as pd

import pyarrow as pa
import pyarrow.parquet as pq
import zarr
from numcodecs import Blosc

from mat_files import masc_mat_file_to_dict,masc_mat_triplet_to_dict,triplet_images_reshape
from weather_data import blowingsnow

sys.path.insert(1,'/home/grazioli/CODES/python/py-masc-3D-GAN-eval')
from gan3d_lib import gan3d 



def files_in_dir_recursive(top, pattern="*", include_dir=True):
    for (root, dirs, files) in os.walk(top):
        match_files = (fn for fn in files if 
            fnmatch.fnmatchcase(fn, pattern))
        if include_dir:
            match_files = (os.path.join(root,fn) for fn in match_files)
        for fn in match_files:
            yield fn


def find_matched(data_dir, min_files=3):
    files = {}
    for fn_full in files_in_dir_recursive(
        data_dir, pattern="*_flake_*_cam_?.mat"):

        fn = fn_full.split("/")[-1]
        fn = ".".join(fn.split(".")[:-1])
        fn_parts = fn.split("_")
        cam = int(fn_parts[-1])
        flake_id = int(fn_parts[-3])
        timestamp = "_".join(fn.split("_")[:2])
        time = datetime.strptime(timestamp, "%Y.%m.%d_%H.%M.%S")

        key = (time,flake_id)
        if key not in files:
            files[key] = {}
        files[key][cam] = fn_full

    print(len(files))
    files = {k: files[k] for k in files if len(files[k])>=min_files}
    print(len(files))

    delete_keys = []
    for (i,k) in enumerate(files):
        if i%1000==0:
            print("{}/{}, {} deleted".format(i,len(files),len(delete_keys)))
        if any(not valid_file(files[k][c]) for c in files[k]):
            delete_keys.append(k)
    for k in delete_keys:
        del files[k]

    print(len(files))

    return files


def valid_file(fn, xhi_min=8.5, max_intens_min=0.03,
     min_size=8, max_size=2048):

    m = sio.loadmat(fn)

    xhi = m["roi"]["xhi"][0,0][0,0]
    if xhi < xhi_min:
        return False

    max_intens = m["roi"]["max_intens"][0,0][0,0]
    if max_intens < max_intens_min:
        return False

    shape = m["roi"]["data"][0,0].shape
    size = np.max(shape)

    if not (min_size <= size <= max_size):
        return False

    # Check if any nan in riming
    if np.isnan(m["roi"][0,0]['riming_probs'][0]).any():
        return False

    return True

def valid_triplet(triplet_files, min_size=10, max_ysize_var=1.5):
    mat = [sio.loadmat(triplet_files[i]) for i in range(3)]

    def get_size(m):
        shape = m["roi"]["data"][0,0].shape
        return shape[0]

    sizes = [get_size(m) for m in mat]
    largest = max(sizes)
    smallest = min(sizes)

    return (largest>=min_size) and (largest/smallest<=max_ysize_var)


def filter_triplets(files):
    return {k: files[k] for k in files if valid_triplet(files[k])}

def create_triplet_dataframes(triplet_files, out_dir,campaign_name='EPFL'):
    """
    Put in a dataframe the descriptors of the images for each cam

    """

    c0=[]
    c1=[]
    c2=[]
    tri=[]

    for (i,k) in enumerate(sorted(triplet_files.keys())):
        if i%10000 == 0:
            print("{}/{}".format(i,len(triplet_files)))
        triplet = triplet_files[k]

        # Create and increment the data frames
        c0.append(masc_mat_file_to_dict(triplet[0]))
        c1.append(masc_mat_file_to_dict(triplet[1]))
        c2.append(masc_mat_file_to_dict(triplet[2]))
        tri.append(masc_mat_triplet_to_dict(triplet,campaign=campaign_name))

        """
        if i == 0:
            c0=pd.DataFrame(masc_mat_file_to_dict(triplet[0]),index=[0])
            c1=pd.DataFrame(masc_mat_file_to_dict(triplet[1]),index=[0])
            c2=pd.DataFrame(masc_mat_file_to_dict(triplet[2]),index=[0])
            tri=pd.DataFrame(masc_mat_triplet_to_dict(triplet,campaign=campaign_name),index=[0])
        else:
            c0 = pd.concat([c0, pd.DataFrame(masc_mat_file_to_dict(triplet[0]),index=[0])], axis=0).reset_index(drop=True)
            c1 = pd.concat([c1, pd.DataFrame(masc_mat_file_to_dict(triplet[1]),index=[0])], axis=0).reset_index(drop=True)
            c2 = pd.concat([c2, pd.DataFrame(masc_mat_file_to_dict(triplet[2]),index=[0])], axis=0).reset_index(drop=True)
            tri= pd.concat([tri,pd.DataFrame(masc_mat_triplet_to_dict(triplet,campaign=campaign_name),index=[0])], axis=0).reset_index(drop=True)
        """

    c0 = pd.DataFrame.from_dict(c0)
    c1 = pd.DataFrame.from_dict(c1)
    c2 = pd.DataFrame.from_dict(c2)
    tri = pd.DataFrame.from_dict(tri)

    # Write tables
    table = pa.Table.from_pandas(c0)
    pq.write_table(table, out_dir+campaign_name+'_cam0.parquet')

    table = pa.Table.from_pandas(c1)
    pq.write_table(table, out_dir+campaign_name+'_cam1.parquet')

    table = pa.Table.from_pandas(c2)
    pq.write_table(table, out_dir+campaign_name+'_cam2.parquet')

    table = pa.Table.from_pandas(tri)
    pq.write_table(table, out_dir+campaign_name+'_triplet.parquet')

def create_triplet_image_array(triplet_files, out_dir,campaign_name='EPFL',dim_in=1024,chunks_n=16):

    """
    Create an image array of (resized) triplet. Store on disk for each campaign
    
    """

    # Define the output array (data flushed directly)
    compressor=Blosc(cname='zstd', clevel=2, shuffle=Blosc.BITSHUFFLE)
    z1 = zarr.open(out_dir+campaign_name+'.zarr', mode='w',
        shape = [len(triplet_files),dim_in,dim_in,3],compressor=compressor,
        dtype='u1',chunks=[chunks_n,dim_in,dim_in,3]  ) # Size N files, 1024, 1024, 3 

    for (i,k) in enumerate(sorted(triplet_files.keys())):
        if i%10000 == 0:
            print("{}/{}".format(i,len(triplet_files)))

        triplet = triplet_files[k]
        z1[i,:,:,:] = triplet_images_reshape(triplet,newshape=[dim_in,dim_in])


def add_gan3d_to_parquet(triplet_parquet,gan3d_folder):

    """
    Add GAN3D mass and volume to triplet files
    """

    ganfile  = gan3d_folder+'masc_3D_print_grids.nc'
    mascfile = gan3d_folder+'masc_3D_print_triplets.nc'

    # Get the gan3d files
    g3d = gan3d(ganfile=ganfile,mascfile=mascfile)

    # Read the parquet file
    table = pd.read_parquet(triplet_parquet)
    flake_uid = table.datetime.apply(lambda x: x.strftime('%Y%m%d%H%M%S'))+'_'+table.flake_id.apply(str)

    # Get GAN time in proper format and fill the precooked vector
    mass = np.asarray(table['3dgan_mass'])
    vol  = np.asarray(table['3dgan_vol_ch'])
    r_g  = np.asarray(table['3dgan_r_g'])

    for i in range(len(g3d.time)):
        tt = timestamp=datetime.utcfromtimestamp(g3d.time[i]).strftime("%Y%m%d%H%M%S")+'_'+str(g3d.particle_id[i])
        try:
            mass[(np.where(flake_uid == tt))]=g3d.mass_1d[i]
            vol[(np.where(flake_uid == tt))]=g3d.V_ch[i]
            r_g[(np.where(flake_uid == tt))]=g3d.r_g[i]
        except:
            print("Flake id: "+tt+" not in the database") 

    table['3dgan_mass']   =  mass
    table['3dgan_vol_ch'] =  vol
    table['3dgan_r_g']    =  r_g

    # Store table and overwrite
    table = pa.Table.from_pandas(table)
    pq.write_table(table, triplet_parquet)

def add_bs_to_parquet(triplet_parquet,file_bs,verbose=False):

    """
    Add Blowing Snow information to triplet files

    Input:

    triplet_parquet: parquet file with info about MASC triplets
    file_bs        : CSV file of blowing snow

    """

    # Read the parquet file
    table = pd.read_parquet(triplet_parquet)
    flake_uid = table.datetime.apply(lambda x: x.strftime('%Y%m%d%H%M%S'))+'_'+table.flake_id.apply(str)

    # Read the blowingsnow file
    bs  = blowingsnow(file_bs)

    # Fill the precooked vector 
    bs_nor_angle    = np.asarray(table['bs_nor_angle'])
    bs_mix_ind      = np.asarray(table['bs_mix_ind'])
    bs_precip_type  = table['bs_precip_type'].copy()

    # Ugly unefficent loop
    for i in range(len(flake_uid)):
        ID = flake_uid[i]

        try:
            condi = np.where(bs.flake_uid  == ID)[0][0]
            bs_nor_angle[i] = bs.df["Normalized_Angle"][condi]
            bs_mix_ind[i]   = bs.df["Flag_mixed"][condi]
        except:
            if verbose: print(ID+' blowing snow not available')
    

    # Fill also a precooked flag
    bs_precip_type[bs_nor_angle > 0.881]='blowing_snow'
    bs_precip_type[bs_nor_angle < 0.193]='precip'
    bs_precip_type[bs_mix_ind >= 0.0]='mixed'

    
    table['bs_nor_angle']   =  bs_nor_angle
    table['bs_mix_ind']     =  bs_mix_ind
    table['bs_precip_type'] = bs_precip_type

    # Store table and overwrite
    table = pa.Table.from_pandas(table)
    pq.write_table(table, triplet_parquet)

def add_weather_to_parquet(triplet_parquet,file_weather, verbose=False):
    """"
    Add weather data (from pre-compiled minute-scaled pickle) to the triplet file
    """
    # Read the parquet fileand get the time string
    table = pd.read_parquet(triplet_parquet)
    flake_uid = table.datetime.round('min') # Round to minute as weather info is in minute

    # Read the blowingsnow file
    env  = pd.read_pickle(file_weather)

    # Fill the precooked vectors of environmental info 
    T = np.asarray(table['env_T'])
    P = np.asarray(table['env_P'])
    DD = np.asarray(table['env_DD'])
    FF = np.asarray(table['env_FF'])
    RH = np.asarray(table['env_RH'])

    # Ugly unefficent loop
    for i in range(len(flake_uid)):
        ID = flake_uid[i]

        # Find the closest emvironmental info
        try: 
            index = env.index.searchsorted(ID)
            vec = env.iloc[index]
            T[i]   = vec["T"]
            P[i]   = vec["P"]
            DD[i]  = vec["DD"]
            FF[i]  = vec["FF"]
            RH[i]  = vec["RH"]
        except:
            if verbose:
                print("Cannot find environemntal information for this datetime: ")
                print(ID)
        
    table['env_T']   = T
    table['env_P']   = P
    table['env_DD']  = DD
    table['env_FF']  = FF
    table['env_RH']  = RH
    
    # Store table and overwrite
    table = pa.Table.from_pandas(table)
    pq.write_table(table, triplet_parquet)
    

def merge_triplet_dataframes(path,campaigns,out_path,out_name='all'):

    """
    Merge triplet dataframes into a single one.

    Input:
        path :        input path
        campaigns:    list of campaign names (parquet must exist)
        out_path:     out_path
        out_name:     string used in the output name        

    """

    # Dataframes
    databases=['cam0','cam1','cam2','triplet']

    for db in databases:
        print('Merging database: '+db)
        # Read the parquet files
        for i in range(len(campaigns)):
            print('Merging campaign: '+campaigns[i])
            if i == 0:
                df = pd.read_parquet(path+campaigns[i]+'_'+db+'.parquet')
            else:
                df = pd.concat([df, pd.read_parquet(path+campaigns[i]+'_'+db+'.parquet')], axis=0).reset_index(drop=True)
        
        # Write to file
        print('Writing output')
        table = pa.Table.from_pandas(df)
        pq.write_table(table, out_path+out_name+'_'+db+'.parquet')


def merge_triplet_image_array(path,campaigns,out_path,out_name='all',chunks_n=16):

    """
    Merge triplet image array into a single zarr output.

    Input:
        path :        input path
        campaigns:    list of campaign names (zarr must exist)
        out_path:     out_path
        out_name:     string used in the output name  
        chunks_n:     chunk size in number of images      

    """
    n_images=0 # Number of images

    # Get information on dimension (assuming all dims except first one are the same) 
    for i in range(len(campaigns)):
        fn=path+campaigns[i]+'.zarr'
        zz = zarr.open(fn,mode='r')
        n_images += zz.shape[0]

    # Create output Zarr
    compressor=Blosc(cname='zstd', clevel=2, shuffle=Blosc.BITSHUFFLE)
    z1 = zarr.open(out_path+out_name+'.zarr', mode='w',
         shape = [n_images,zz.shape[1],zz.shape[2],3],compressor=compressor,
         dtype='u1',chunks=[chunks_n,zz.shape[1],zz.shape[2],3]  ) # Size N files, 1024, 1024, 3 

    # Merge .zarr according to chunk size and write a new .zarr
    ii=0
    for i in range(len(campaigns)):
        fn=path+campaigns[i]+'.zarr'
        zz = zarr.open(fn,mode='r')

        n_ii = zz.shape[0]

        # Two increments: one as big as the chunk and one equal to 1 at the tail of the dataset
        j = 0
        j2= 0
        escape = False
        while (j < n_ii) and not(escape):
            # Update counter
            if ((n_ii-j) >=  chunks_n):
                inc = chunks_n
                j2 += inc  
                z1[ii:(ii+inc),:,:,:] = zz[j:(j+inc),:,:,:]
            else:
                inc = 1
                j2 += inc  
                z1[ii,:,:,:] = zz[j,:,:,:]
                if j2 == n_ii:
                    escape = True
            j   = j2
            ii += inc

            if ii%10000 == 0:
                print(ii)
                print('Merged')
        

        """
        for j in range(n_ii):
            z1[ii,:,:,:]=zz[j,:,:,:]
            ii += 1
        """


def process_all(masc_dir,campaign_name='EPFL'):
    # this runs all the processing to create a basic dataset of masc triplets and
    # m
    
    # Find triplets
    print('Finding matched triplets: ')
    triplet_files = find_matched(masc_dir)
    print(len(triplet_files))
    print('Valid triplets: ')
    triplet_files = filter_triplets(triplet_files)
    print(len(triplet_files))

    # Create triplet datasets (descriptors) of each campaign
    print('Creating triplet dataframe')
    create_triplet_dataframes(triplet_files,'/data/MASC_DB/',campaign_name=campaign_name)

    # Create triplet array of images using Zarr
    print('Creating database of images (zarr)')
    create_triplet_image_array(triplet_files,'/data/MASC_DB/',campaign_name=campaign_name,dim_in=1024)

    print("Hi")

#merge_triplet_image_array(['/home/grazioli/tmp/PLATO_images.zarr','/home/grazioli/tmp/ICEGENESIS_images.zarr'],'dummy')

campaigns=['Davos-2015','APRES3-2016','APRES3-2017','Valais-2016','ICEPOP-2018','PLATO-2019','Davos-2019','Jura-2019','POPE-2020','ICEGENESIS-2021']
merge_triplet_image_array('/data/MASC_DB/',campaigns,'/data/MASC_DB/',out_name='MASCdb')


for campaign in campaigns:
    print(campaign)
    # 0: Process data and triplets (basic)
    process_all('/data/'+campaign+'/',campaign_name=campaign)

    # 1: Add blowing snow to parquet
    print("Adding blowing snow")
    add_bs_to_parquet('/data/MASC_DB/'+campaign+'_triplet.parquet',
        '/data/MASC_DB/rawinput/'+campaign+'/bs/blowing_snow_triplet.csv',verbose=True)         # Add BS                                                     

    # 2: Add GAN3D to parquet
    print("Adding 3d-gan")
    add_gan3d_to_parquet('/data/MASC_DB/'+campaign+'_triplet.parquet','/data/'+campaign+'/')    # Add GAN3D

    # 3: Add Environemntal info to parquet
    print("Adding environmental information")
    add_weather_to_parquet('/data/MASC_DB/'+campaign+'_triplet.parquet',
        '/data/MASC_DB/rawinput/'+campaign+'/Weather/'+campaign+'.pickle',verbose=True) # Add weather

# Merge
merge_triplet_dataframes('/data/MASC_DB/',campaigns,'/data/MASC_DB/',out_name='MASCdb')
merge_triplet_image_array('/data/MASC_DB/',campaigns,'/data/MASC_DB/',out_name='MASCdb')



