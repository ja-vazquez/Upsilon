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
#--------------------------

lnum =  R0_files()

for redz in redzz:
  file  = files_name(data_type, bin_type, redz)
  for _, num in enumerate(lnum):
   file_num_extra = '%s%i'%(file, num)
        # read best fit values
   file_bf = 'stats/' + file_num_extra + '_ups.margestats'

   bf_lines = open(file_bf, 'r').readlines()
   i=0
   bf, sig1, sig2, sig3, sig4 = [], [], [], [], []
   for lines in bf_lines:
       if i> 2:
          vals = lines.split()[0:]
          bf.append(float(vals[1]))
 	  sig1.append(float(vals[3]))
	  sig2.append(float(vals[4]))
	  sig3.append(float(vals[6]))
 	  sig4.append(float(vals[7]))
       i+=1

   with open('bestfit/best_sigma8_%s.dat'%(file), 'a') as f:
	f.write("%i \t %2.6f \t %2.6f \t %2.6f \t %2.6f \t %2.6f \n"%(num, bf[2], bf[2]-sig1[2], sig2[2]-bf[2], bf[2]-sig3[2],  sig4[2] -bf[2] ))
