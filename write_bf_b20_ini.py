# only select between lin or log
# and b_2 = 0
# and uncommet b20
import os, sys, time
from Useful import *

        #lin or log, sim or mocks
if len(sys.argv) > 2:
    data_type ='%s'%(sys.argv[1])
    bin_type  ='%s'%(sys.argv[2])
    if len(sys.argv) > 3:
        redzz = ['%s'%(sys.argv[3])]
else:
    print_message()

dir_chains = chain_dir(data_type)
dir_data = 'lrgdata-final/mocks_lrg/sim_reshaped/'

#--------------------------
extra     = extra()
name_root =  '_ups'
name_ups  =  '_ups.dat'
name_cov  =  '_cov.dat'


	#empty or b20
b20 = '_b20'

lnum =  R0_files()
lnp  = number_of_points(data_type, bin_type)

averr = 1.0 if 'rebin' in bin_type else 0.5
#------------------------------------------------------------------


for redz in redzz:
    file  = files_name(data_type, bin_type, redz)
    for n, num in enumerate(lnum):
        np  = lnp[n]
        file_num_extra = '%s%i%s'%(file, num, extra)

	# read best fit values
        file_bf = 'stats/' + file_num_extra + name_root + '.likestats'

        bf_lines = open(file_bf,'r').readlines()
        i, bf = 0, []
   
        for lines in bf_lines:
            if i> 2:
                vals = lines.split()[0:]
                bf.append(float(vals[1]))
            i+=1 


        with open('bf%s_INI_%s.ini'%(b20, file_num_extra), 'w') as f:
            bf_1 = "param[LRGa] = %2.3f %2.3f %2.3f 0.001 0.001\n"%(bf[0], bf[0]-0.001, bf[0]+0.001)
	    bf_2 = "param[LRGb] = %1.3f %1.3f %1.3f 0.001 0.001\n"%(bf[1], bf[1]-0.001, bf[1]+0.001)
	    bf_3 = "param[logA] = %1.3f %1.3f %1.3f 0.001 0.001\n"%(bf[3], bf[3]-0.001, bf[3]+0.001)
        
	    f.write(bf_1 + bf_2 + bf_3 +'\n')
	    #f.write("param[LRGb] = 0 0 0 0 0\n")	

            best_fit  = "best_fit = bestfit/best_%s%s.dat\n"%(file_num_extra, b20)
            aver      = "aver   = %1.2f\n"%(averr)

            f.write(Text_ini_file() + best_fit + aver + '\n')
            f.write('use_upsilon= 99\n')
            f.write('samples = 8\n\n')

            f.write('file_root = ' + dir_chains + 'bf_'  + file_num_extra + name_root + '\n')  
            f.write('mock_file = ' + dir_data	         + file_num_extra + name_ups + '\n')
            f.write('mock_cov  = ' + dir_data            + file_num_extra + name_cov + '\n')

            f.write('R0_gg = %i.0\n'%(num))
            f.write('R0_gm = %i.0\n'%(num))

            if 'sim' in data_type:
	        f.write(params_cosmo('params_sim') + '\n\n')
                f.write('z_gg  = %s\n'%(redz))
                f.write('z_gm  = %s\n'%(redz))
            else:
	        f.write(params_cosmo('params') + '\n\n')
                f.write('z_gg  = %s\n'%(z_mean(data_type, redz)))
                f.write('z_gm  = %s\n'%(z_mean(data_type, redz)))

            if 'rebin' in bin_type:
                f.write('use_diag = F\n')
            else:
                f.write('use_diag = T\n')

            f.write('mock_NP = %i\n'%(np))
            f.write('mock_gg = %i\n'%(np//2))
 
