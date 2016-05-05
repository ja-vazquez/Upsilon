import sys


def print_message():
       print """select sim/mocks/lowz
                lin1:log / bin:rebin1 / lowz:z1:z2
                [0.25,0.40]/[steps_,]/[log1,log1_rebin]"""


class Info_model:
    def __init__(self, data_type, bin_type, redz):
        self.data_type = data_type
        self.bin_type  = bin_type
        self.redz      = redz
        self.nada = 'nothing'


        #select file's name
    def files_name(self):
        fname = {'sim'  : self.data_type + '_' + self.bin_type + '_z' + self.redz + '_norsd_np0.001_nRT10_r0',
                  'mocks': 'mock_bigMD_RST_' + self.redz + '_' + self.bin_type + '_DM1_r0',
                  'lowz' : self.redz + '_' + self.bin_type + '_r0'}
        return fname[self.data_type]

        #select chains's folder
    def chain_dir(self):
        chdir = {'sim'  : 'Sim_jk_b2/',
                 'mocks': 'Mocks/',
                 'lowz' : 'Lowz/'}
        return chdir[self.data_type]


        # will read this number from a file later
    def R0_files(self):
        return 2, 3, 4, 5, 6, 10


        # will read this number from a file later
    def  number_of_points(self):
        data_type = self.data_type
        bin_type  = self.bin_type

        if 'sim' in data_type:
            if 'lin_bin1' in bin_type:
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
                lnp =  28, 28, 28, 28, 28, 28
            else:
                lnp = 184, 164, 148, 136, 126, 100

        else:       print 'error'
        return lnp



    def z_mean(self):
        #select redshift
        if 'sim' in self.data_type:
            return self.redz
        elif 'lowz' in self.data_type:
            z = {'lowz': '0.27', 'z1': '0.21', 'z2': '0.31'}
            return z[self.redz]
        else:
            return '0.267'






def Text_ini_file(threads = 3, action = 0):
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

#If zero set automatically
num_threads = {th:d}

indep_sample=0

use_clik= F
#MCMC = 0, JK =2
action = {ac:d}

#these are just small speedups for testing
get_sigma8=T

#Uncomment this if you don't want 0.06eV neutrino by default
#num_massive_neutrinos=3
#param[mnu] = 0 0 0 0 0


#-------------------------------------##

#none of the used for now 
use_Ups = T
use_mock = T

use_coyote = T
use_XiAB = F

#if use_coyote = F :upsilon_option (2) Xi, (1) Xicorr, (3) FFT_Pk linear
#if use_coyote = T :upsilon_option (0) FFT_Coyo

upsilon_option = 0\n\n""".format(th=threads, ac=action)
    return txt



def params_upsilon():
    txt = """
param[LRGa] = 1.8 1 2.5 0.02 0.02
#param[LRGb] = 0 0 0 0 0
param[LRGb] = 0.2 -2.5 2.5 0.01 0.01
param[logA] = 3.076 2.6 3.2 0.02 0.02
#param[logA] = 3.076 3.076 3.076 0 0
\n\n"""
    return txt




def R0_params(R0, nR0):
    txt="""
R0_gg    = %i.0
R0_gm    = %i.0
mock_NP  = %i
mock_gg  = %i
    """%(R0, R0, nR0, nR0//2)
    return txt






def params_cosmo(data_type):
    if 'sim' in data_type:
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



if __name__ == '__main__':
    info = Info_model('nada')
    print info.name
