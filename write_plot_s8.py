import pylab
import os, sys, time
import matplotlib.pyplot as plt
import matplotlib as mpl
from Useful import *

        #lin or log, sim or mocks
if len(sys.argv) > 2:
    data_type ='%s'%(sys.argv[1])
    bin_type  =['%s'%(sys.argv[2])]
    if len(sys.argv) > 3:
        redzz = ['%s'%(sys.argv[3])]
else:
      print_message()

bin_type =['log1_rebin', 'log1']
redzz = ['lowz', 'z1', 'z2']
#-----------------------------

dir = 'bestfit/'
colors = ['r', 'g','b','m']

for redz in redzz:
    j=0
    R0t, s8t, sig1t, sig2t, sig3t, sig4t=[],[],[],[],[],[]
    
    for bin_typ in bin_type:
       filen  = files_name(data_type, bin_typ, redz)	 
       file = dir + 'best_sigma8_%s.dat'%(filen) 
       s8_lines = open(file,'r').readlines()

       R0, s8, sig1, sig2, sig3, sig4 = [], [],[], [],[],[]
       for lines in s8_lines:
          vals = lines.split()[0:]
  	  R0.append(float(vals[0])+j)
          s8.append(float(vals[1]))
          sig1.append(float(vals[2]))
	  sig2.append(float(vals[3]))
	  sig3.append(float(vals[4]))
	  sig4.append(float(vals[5]))
       R0t.append(R0)
       s8t.append(s8)
       sig1t.append(sig1)
       sig2t.append(sig2)
       sig3t.append(sig3)
       sig4t.append(sig4)	
       j+=0.05

    fig =plt.figure(figsize=(15,6))
    ax = fig.add_subplot(1,1,1)
   
    
    for i in range(len(R0t)): 
       ax.errorbar(R0t[i], s8t[i], yerr=[sig3t[i], sig4t[i]], fmt='o',   ecolor=colors[i], label=bin_type[i])
       ax.errorbar(R0t[i], s8t[i], yerr=[sig1t[i], sig2t[i]], fmt='o',  ecolor=colors[i])
    #ax.grid(True)
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.grid(b=True, which='major', color='k', linewidth=1.0)
    ax.grid(b=True, which='minor', color='k', linewidth=0.5)
    plt.xlabel('R0')
    plt.ylabel('sigma8')
    #ax.set_xscale('log')
    plt.title('z = %s'%(redz))
    plt.legend(loc="upper right")
    plt.xlim(1,R0[-1]+2)
    pylab.savefig(dir+"best_sigma8_%s.pdf"%(filen))
plt.show()
