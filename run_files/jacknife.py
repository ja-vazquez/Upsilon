

import numpy as np
from matplotlib import pyplot as plt
from Useful import *
import pylab

data_type = 'mocks'

dir_jk    = 'Jackknife/'
dir_chains = chain_dir(data_type)

bin_type, redzz, dir = file_choice(data_type)

for bin in bin_type:
   for redz in redzz:
     file_name  = files_name(data_type, bin, redz)
     with open(dir_jk + file_name + '_stats.dat', 'a') as g:
    
        lnum  = R0_files()
        s8T, b1T, b2T, H0T = [], [], [], []
        for R0 in lnum:
           s8t, b1t, b2t, H0t = [], [], [], []
           for i in range(100): 
               file = file_name + '%i_jk%i_ups.minimum'%(R0, i)
               output = file_name + '%i'%(R0)
               fdata = open(dir_chains + file, 'r').readlines()

               for lines in fdata:
                  line = lines.strip()
                  vals = line.split()[0:]
                  if vals:
                     if 'sigma8' in  vals[2]:  s8 = float(vals[1]) 
                     if 'LRGa' in vals[2]:     b1 = float(vals[1])
	             if 'LRGb' in vals[2]:     b2 = float(vals[1])
                     if vals[2] == 'H0':       H0 = float(vals[1])
               s8t.append(s8)
               b1t.append(b1)
               b2t.append(b2)
	       H0t.append(H0)
               with open(dir_jk + output + '.dat','a') as f:
                   f.write("%i \t %2.6f \t %2.6f \t %2.6f \n"%(i, s8, b1, b2))
   
           s8T.append(s8t)
           b1T.append(b1t)
           b2T.append(b2t)
	   H0T.append(H0t)  

           g.write("%i \t %2.6f \t %2.6f \t %2.6f \t %2.6f \t %2.6f \t %2.6f \n"%(R0, np.mean(s8t),
	     np.std(s8t),np.mean(b1t),np.std(b1t),np.mean(b2t), np.std(b2t)))
  	       #print np.mean(s8t), np.mean(b1t), np.mean(b2t)
 	       #print np.std(s8t),  np.std(b1t),  np.std(b2t)

        if True:
 		fig =pylab.figure(figsize=(14,7))
		ax = fig.add_subplot(2,3,1)
 		ax.plot(b1T[0], 'ro', label='R0 =2', color = 'b')
 		plt.legend()
 		ax2 = fig.add_subplot(2,3,2)
 		ax2.plot(b1T[1], 'ro', label='R0 =3', color = 'b')
 		plt.legend()
 		ax3 = fig.add_subplot(2,3,3)
 		ax3.plot(b1T[2], 'ro', label='R0 =4', color = 'b')
 		plt.title(file_name)
 		plt.legend()
 		ax4 = fig.add_subplot(2,3,4)
 		ax4.plot(b1T[3], 'ro', label='R0 =5', color = 'b')
 		plt.legend()
 		ax5 = fig.add_subplot(2,3,5)
 		ax5.plot(b1T[4], 'ro', label='R0 =6', color = 'b')
 		plt.legend()
 		ax6 = fig.add_subplot(2,3,6)
 		ax6.plot(b1T[5], 'ro', label='R0 =10', color = 'b')
 		plt.legend()
 		plt.savefig(dir_jk + file_name + '_b1.pdf')
 		plt.show()

