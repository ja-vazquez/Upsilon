# only select between lin or log
import os, sys, time
from Useful import *

        #lin or log, sim or mocks
if len(sys.argv) > 2:
    data_type ='%s'%(sys.argv[1])
    bin_type  ='%s'%(sys.argv[2])
    if len(sys.argv) > 3:
        redzz = ['%s'%(sys.argv[3])]
    if len(sys.argv) > 4:
	extra ='%s'%(sys.argv[4])
else:
    print_message()


#----------------------------------------------------------------------

dir_chains = chain_dir(data_type)
dir_data   = 'lrgdata-final/mocks_lrg/sim_reshaped/'

#extra     = extra()
name_root =  '_ups'
name_ups  =  '_ups.dat'
name_cov  =  '_cov.dat'
#--------------------------------------------------------------------------


lnum =  R0_files() 
lnp  = number_of_points(data_type, bin_type)
if len(lnum) != len(lnp):  sys.exit("Error: check number of files")


averr = 0.0 if 'rebin' in bin_type else 0.5
#------------------------------------------------------------------


for redz in redzz:
    file  = files_name(data_type, bin_type, redz)

    for n, num in enumerate(lnum):  
	np  = lnp[n]
	file_num_extra = '%s%i%s'%(file, num, extra)
       
 
        with open('INI_%s.ini'%(file_num_extra), 'w') as f:
           ini_input = Text_ini_file() + Text_ini_file2()  
	   best_fit  = """\nbest_fit = bestfit/best_%s.dat"""%(file_num_extra)
	   aver      = """\naver   = %1.2f"""%(averr)
           f.write(ini_input + best_fit + aver + '\n')
    

           if 'sim' in data_type:
              f.write(params_cosmo('params_sim') + '\n\n')
	      f.write('z_gg  = %s\n'%(redz))
	      f.write('z_gm  = %s\n'%(redz))
           else:
              f.write(params_cosmo('params') + '\n\n') 
	      f.write('z_gg  = %s\n'%(z_mean(data_type, redz)))
	      f.write('z_gm  = %s\n'%(z_mean(data_type, redz)))

           f.write('R0_gg = %i.0\n'%(num))
           f.write('R0_gm = %i.0\n'%(num))

           if 'rebin' in bin_type:
              f.write('use_diag = F\n')
           else:
              f.write('use_diag = T\n')

           f.write('mock_NP = %i\n'%(np))
           f.write('mock_gg = %i\n'%(np//2))

           f.write('file_root = ' + dir_chains + file_num_extra + name_root + '\n')  
           f.write('mock_file = ' + dir_data   + file_num_extra + name_ups  + '\n')
           f.write('mock_cov  = ' + dir_data   + file_num_extra + name_cov  + '\n')

 


