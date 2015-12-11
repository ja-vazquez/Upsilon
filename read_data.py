# Script to read Sukhdeep files and modify their format to a CosmoMC

import numpy as np
from Useful import *

data_type = 'mocks'			#sim, mocks,lowz


        #select type of file to anlayze
bin_type, redzz, dir = file_choice(data_type)

#------------------------------------------

file_dir  = 'sim_files/lowz_clustering_lensing/'+dir
dir_out   = 'sim_reshaped/'
name_gg   = '_upsgg_cov.dat'
name_gm   = '_upsgm_cov.dat'


lnum  =  R0_files()
first_point, last_point = 1 , 70	#select the range of points
fline = 1				#skip first line

#---------------------------------------------

for i in range(100):
 name_ups  = '_jk%i_ups.dat'%(i)
 name_cov  = '_jk%i_cov.dat'%(i)

 for redz in redzz:			 #select the file's name
   file_name = files_name(data_type, bin_type, redz)

   for num in lnum: 
       fdata    = open(file_dir + file_name + str(num) + name_ups)
       file_read = fdata.readlines()
    
       rp, ups_gg, ups_gm = [], [], []
  
       for l, _ in enumerate(file_read): 
	  vals = file_read[l].split()
	  if vals[0] != '#':
	      if (float(vals[0]) < last_point and float(vals[0]) > first_point): 
		  rp.append(vals[0])
		  ups_gg.append(vals[1])
		  ups_gm.append(vals[3])
       lups =  len(ups_gg)
       fdata.close()

       i = 0	
     	#new Format file
       with open(dir_out  + file_name + str(num) + name_ups, 'w') as f:
          for l in range(fline, lups ):
   	      f.write(str(rp[l] + '\t' + ups_gg[l] + '\n'))
          for l in range(fline, lups ):
	      f.write(str(rp[l] + '\t' + ups_gm[l] + '\n'))		     	
	      i += 1
       print redz, 'R0', num, 'len_file',i*2


     	# New cov matrix
       table1 = np.loadtxt(file_dir + file_name + str(num) + name_gg)
       table2 = np.loadtxt(file_dir + file_name + str(num) + name_gm)

       new_table1 = table1[fline: lups, fline: lups]
       new_table2 = table2[fline: lups, fline: lups]

       row, col = new_table1.shape
       zero= '0 '*row


       with open(dir_out +  file_name + str(num) + name_cov , 'w') as f:
          for n in range(row):
             for m in range(col):
                f.write(str("%1.3e" %float(new_table1[n,m])) + ' ')
             f.write(zero)
             f.write('\n')
    
          for n in range(row):
             f.write(zero)
             for m in range(col):
                f.write(str("%1.3e" %float(new_table2[n,m])) + ' ')
             f.write('\n')

       print '*** rows =',row*2, 'cols = ', col*2 


