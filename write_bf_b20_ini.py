# only select between lin or log
# and b_2 = 0
# and uncommet b20
import os, sys, time


        #lin or log, sim or mocks
if len(sys.argv) > 2:
    which ='%s'%(sys.argv[1])
    what  ='%s'%(sys.argv[2])
    if len(sys.argv) > 3:
      redzz = ['%s'%(sys.argv[3])]
    else:
      if 'sim' in which:
         redzz = ['0.25','0.40']
      elif 'mocks' in which:
         redzz = ['steps_','']
else:
    print 'select sim/mocks  lin1:log / bin:rebin1  [0.25,0.40]/[steps_,]'

	#empty or b20
b20 = '_b20'

dir_data = 'lrgdata-final/mocks_lrg/sim_reshaped/'
dir_chains = 'chains/Mocks/'

#---------------------------
lnum =  2 , 3, 4,  5,  6,  10, 20

if 'sim' in which:
    if 'lin_bin1' in what:
        lnp  =  134, 132, 130, 128, 126, 118, 98
    elif 'lin_rebin1' in what:
        lnp = 26, 24, 24, 22, 22, 18, 12
    elif 'lin_bin2' in what:
	lnp  = 76, 76, 74, 74, 72, 68, 58
    elif 'lin_rebin2' in what:
	lnp = 26, 24, 24, 22, 22, 18, 12
    elif 'log_bin1' in what:
        lnp = 102, 90, 82, 74, 70, 54, 34
    elif 'log_rebin1' in what:
        lnp = 22, 18, 18, 16, 16, 12, 8

elif 'mocks' in which:
    if 'lin1' in what:
        lnp  =  134, 132, 130, 128, 126, 118, 98
    elif 'rebin1' in what:
        lnp = 28, 28, 28, 28, 28, 28, 28
else:
    print 'error'



if 'lin' in what:
   averr = 0.5
elif 'rebin' in what:
   averr = 1.0
else:
   averr = 0.0



for redz in redzz:
  if 'sim' in which: 
      file = which +'_'+ what + '_z'+ redz+ '_norsd_np0.001_nRT10_r0'
  elif 'mocks' in which:
      file = which +'_RST_'+ redz + what + '_DM1_r0'
  else:
      print 'error'


	#number of files
  for n in range(0,len(lnum)):
   num = lnum[n] 
   np  = lnp[n]

	# read best fit values
   if 'sim' in which:
      file_bf = 'stats/Re_sim_%s_z%s_norsd_np0.001_nRT10_r0%i_ups.likestats'%(what,redz,num)
   elif 'mocks' in which:
      file_bf = 'stats/Re_%s_RST_%s%s_DM1_r0%i_ups.likestats'%(which, redz,what, num)

   bf_lines = open(file_bf,'r').readlines()
   i=0
   bf = []
   for lines in bf_lines:
       if i> 2:
          vals = lines.split()[0:]
          bf.append(float(vals[1]))
       i+=1 


   with open('bf%s_INI_%s%i.ini'%(b20, file, num), 'w') as f:


     params_sim = """
param[omegabh2] = 0.022 0.022 0.022 0 0
param[omegach2] =0.1172 0.1172 0.1172 0 0
param[theta] = 1.0422 1.0422 1.0422 0 0
param[ns] = 0.965 0.965 0.965 0 0
     """
     params_mock = """
param[omegabh2] = 0.02214 0.02214 0.02214 0 0
param[omegach2] =0.1189 0.1189 0.1189 0 0
param[theta] = 1.04003 1.04003 1.04003 0 0
param[ns] = 0.96 0.96 0.96 0 0
     """

     if 'sim' in which:
        f.write(params_sim+'\n\n')
     elif 'mocks' in which:
        f.write(params_mock+'\n\n')


     bf_input = """
param[LRGa] = %2.3f %2.3f %2.3f 0.001 0.001
#param[LRGb] = %1.3f %1.3f %1.3f 0.001 0.001
param[LRGb] = 0 0 0 0 0
#param[ns] = 0.965 0.965 0.965 0 0
param[logA] = %1.3f %1.3f %1.3f 0.001 0.001
     """%(bf[0],bf[0]-0.001,bf[0]+0.001, bf[1], bf[1]-0.001, bf[1]+0.001, bf[3],bf[3]-0.001, bf[3]+0.001 )
     f.write(bf_input+'\n\n')

     ini_input = """
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
action = 0

#these are just small speedups for testing
get_sigma8=T

#Uncomment this if you don't want 0.06eV neutrino by default
#num_massive_neutrinos=3
#param[mnu] = 0 0 0 0 0

use_upsilon= 99
best_fit = bestfit/best_%s_fit_z%s_R0%i%s.dat
  
#-------------------------------------##
samples = 8

use_Ups = T
use_mock = T
use_coyote = T
use_XiAB = T
aver   = %1.2f


#upsilon_option (2) Xi, (1) Xicorr, (3) FFT_Pk, (0) FFT_Coyo
upsilon_option = 0
     """%(what,redz, num,b20,averr)
     f.write(ini_input+'\n\n')
     f.write('file_root = ' + dir_chains + 'bf_b20_' +'Re' + file + str(num) + '_ups\n')  
     f.write('mock_file = ' + dir_data   + 'new_'+ file + str(num) + '_ups.dat\n')
     f.write('mock_cov  = ' + dir_data   + 'new_'+ file + str(num) + '_cov.dat\n')

     f.write('R0_gg = %i.0\n'%(num))
     f.write('R0_gm = %i.0\n'%(num))

     if 'sim' in which:
         f.write('z_gg  = %s\n'%(redz))
         f.write('z_gm  = %s\n'%(redz))
     elif 'mocks' in which:
         f.write('z_gg  = 0.267\n')
         f.write('z_gm  = 0.274\n')

     if 'lin' in what:
        f.write('use_diag = T\n')
     elif 'rebin' in what:
        f.write('use_diag = F\n')

     f.write('mock_NP = %i\n'%(np))
     f.write('mock_gg = %i\n'%(np//2))
 

