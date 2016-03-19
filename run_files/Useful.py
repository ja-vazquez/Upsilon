
def extra():
   return ''


def chain_dir(data_type):
    dir = 'chains/'
    if 'sim' in data_type:
	dir += 'Sim_jk_b2/'
    elif 'mocks' in data_type:
        dir += 'Mocks_jk/'
    elif 'lowz' in data_type:
        dir += 'Lowz_jk/'
    return dir



def file_choice(data_type):
	#Select the type of file to analyze
    if 'sim' in data_type:
       bin_type = ['lin_rebin']                #lin or log / bin or rebin
       redzz = ['0.25'] #,'0.40']
       dir  = 'sim_results/'

    elif 'mocks' in data_type:
       bin_type = ['rebin1'] #,'rebin1',lin1]                    #lin1 or rebin1
       redzz = ['_steps_'] #'_steps_'
       dir  = 'mock_results/'

    elif 'lowz' in data_type:
       bin_type = ['log1_rebin']              #log1 or log1_rebin
       redzz = ['z1'] #, ['lowz''z1', 'z2']
       dir = 'lowz_results/'

    return bin_type, redzz, dir



def z_mean(data_type, redz):
     if 'lowz' in data_type:
	if 'lowz' in redz:
	    return '0.27'
	elif 'z1' in redz:
	    return '0.21'
	elif 'z2' in redz:
	    return '0.31'
     else:
 	return '0.27'



def files_name(data_type, bin_type, redz):
	#select the file's name
     if 'sim' in data_type:
        file_name = data_type +'_'+ bin_type +'_z'+ redz +'_norsd_np0.001_nRT10_r0'
     elif 'mocks' in data_type:
        file_name = data_type +'_RST'+ redz + bin_type + '_DM1_r0'
     elif 'lowz' in data_type:
        file_name = redz + '_' + bin_type + '_r0'
     else:
        print 'error'    
    
     return file_name



def R0_files():
    lnum =  2, 3, 4, 5, 6, 10
    return lnum



def  number_of_points(data_type, bin_type):
   if 'sim' in data_type:
      if 'lin_bin1' in bin_type:
          lnp  =  134, 132, 130, 128, 126, 118, 98
      elif 'lin_bin2' in bin_type:
          lnp  = 76, 76, 74, 74, 72, 68, 58
      elif 'lin_rebin' in bin_type:
	  lnp = 102, 90, 82, 74, 70, 54
      elif 'lin_rebin2' in bin_type:
          lnp = 26, 24, 24, 22, 22, 18, 12
      elif 'log_bin1' in bin_type:
          lnp = 102, 90, 82, 74, 70, 54, 34
      elif 'log_rebin1' in bin_type:
          lnp = 22, 18, 18, 16, 16, 12, 8

   elif 'mocks' in data_type:
      if 'lin1' in bin_type:
           lnp  =  134, 132, 130, 128, 126, 118
      elif 'rebin1' in bin_type:
           lnp = 28, 28, 28, 28, 28, 28
 
   elif 'lowz' in data_type:
      if 'rebin' in bin_type: 
           lnp = 28, 28, 28, 28, 28, 28
      else:
	   lnp = 184, 164, 148, 136, 126, 100

   else:       print 'error'
   return lnp


def print_message():
       print """select sim/mocks/lowz  
                lin1:log / bin:rebin1 / lowz:z1:z2  
                [0.25,0.40]/[steps_,]/[log1,log1_rebin]"""



def Text_ini_file():
	txt = """
#DEFAULT(batch1/CAMspec_defaults.ini)
#DEFAULT(batch1/lowl.ini)
#DEFAULT(batch1/lowLike.ini)
 
#planck lensing
#DEFAULT(batch1/lensing.ini)
#INCLUDE(batch1/BAO.ini)
#INCLUDE(batch1/HST.ini)
#INCLUDE(batch1/WMAP.ini)

#general settings
DEFAULT(batch1/common_batch1.ini)

#high for new runs
MPI_Max_R_ProposeUpdate = 30

propose_matrix=
#planck_covmats/base_planck_lowl_lowLike.covmat

start_at_bestfit =F
feedback=0
use_fast_slow = F

#sampling_method=7 is a new fast-slow scheme good for Planck
sampling_method = 1
dragging_steps  = 5
propose_scale = 2

indep_sample=0

use_clik= F
#MCMC = 0, JK =2
action = 2

#these are just small speedups for testing
get_sigma8=T

#Uncomment this if you don't want 0.06eV neutrino by default
#num_massive_neutrinos=3
#param[mnu] = 0 0 0 0 0


#-------------------------------------##

#not used now (both)
use_Ups = T
use_mock = T

use_coyote = T
use_XiAB = F

#if use_coyote = F :upsilon_option (2) Xi, (1) Xicorr, (3) FFT_Pk linear
#if use_coyote = T :upsilon_option (0) FFT_Coyo

upsilon_option = 0\n"""
	return txt 




def Text_ini_file2():
        txt = """
param[LRGa] = 1.55 1 2.5 0.02 0.02
#param[LRGb] = 0 0 0 0 0
param[LRGb] = 0.2 -2.5 2.5 0.05 0.05
param[logA] = 2.9 2.5 3. 0.05 0.05

use_upsilon= 98
samples = 10000000"""
	return txt



def params_cosmo(params):
   if 'params_sim' in params:
	txt = """
#Omega_m = 0.292, Omega_b h^2 = 0.022, h=0.69.
param[omegabh2] = 0.022 0.022 0.022 0 0
param[omegach2] =0.1172 0.1172 0.1172 0 0
param[theta] = 1.0422 1.0422 1.0422 0 0
param[ns] = 0.965 0.965 0.965 0 0"""


   else:
	txt = """
#h = 0.677, Omega_lamda= 0.692885, Omega_matter= 0.307115, 
#Omega_baryons= 0.048206, n=0.96
param[omegabh2] = 0.022140 0.022140 0.022140 0 0 
param[omegach2] = 0.118911 0.118911 0.118911 0 0 
param[theta] = 1.040042 1.040042 1.040042 0 0 
param[ns] = 0.96 0.96 0.96 0 0"""
	
   return txt






 
