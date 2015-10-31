import pylab 
import os, sys, time
import matplotlib.pyplot as plt


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

#-----------------------------

lnum = 2, 3, 4, 5, 6, 10, 20


for redz in redzz:
  for n in range(0,len(lnum)):

    R0 = lnum[n]

    dir = 'bestfit/'
    file = dir + 'best_%s_fit_z%s_R0%i'%(what,redz,R0)
    file2 = dir + 'best_%s_fit_z%s_R0%i_b20'%(what,redz,R0)

    pnames=open(file + '.dat').readlines()
    pnames2=open(file2 + '.dat').readlines()

    lpnames = len(pnames)

    gg_R, gm_R = [], []
    gg, gg_error, gg_fit = [], [], []
    gm, gm_error, gm_fit = [], [], []
    gg_b20_R, gg_b20_fit, gm_b20_fit, gm_b20_R = [], [], [], []
 
    for l in range(lpnames):
       vals    = pnames[l].split()[0:]
       if l < lpnames//2:
        gg_R.append( float(vals[0]))
        gg.append( float(vals[1]))
        gg_error.append( float(vals[2]))
        gg_fit.append( float(vals[3]))
       else:
        gm_R.append( float(vals[0]))
        gm.append( float(vals[1])) 
        gm_error.append( float(vals[2]))
        gm_fit.append( float(vals[3]))


    for l in range(lpnames):
       vals    = pnames2[l].split()[0:]
       if l < lpnames//2:
        gg_b20_R.append( float(vals[0]))
        gg_b20_fit.append( float(vals[3]))
       else:
	gm_b20_R.append( float(vals[0]))
        gm_b20_fit.append( float(vals[3]))


    fig =plt.figure(figsize=(15,6))
    ax = fig.add_subplot(1,2,1)

    ax.errorbar(gg_R, gg, yerr=gg_error,  fmt='+')
    ax.plot(gg_R, gg_fit, label = 'best_%s_fit'%(what))
    ax.plot(gg_b20_R, gg_b20_fit, label = 'best_%s_fit, b2=0'%(what))
    plt.xlabel('R')
    plt.ylabel('gg')
    ax.set_title('z=%s, R0=%i'%(redz,R0))
    plt.legend(loc="upper right")
    plt.xlim(2,82) 

    ax2 = fig.add_subplot(1,2,2)
    ax2.errorbar(gm_R, gm, yerr=gm_error,  fmt='+')
    ax2.plot(gm_R, gm_fit, label = 'best_%s_fit'%(what))
    ax2.plot(gm_b20_R, gm_b20_fit, label = 'best_%s_fit, b2=0'%(what))
    plt.xlabel('R')
    plt.ylabel('gm')
    ax2.set_title('z=%s, R0=%i'%(redz,R0))
    plt.legend(loc="upper right")
    plt.xlim(2,82)

    plt.tight_layout()
    pylab.savefig(file+".pdf")
plt.show()

