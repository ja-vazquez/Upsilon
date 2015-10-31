# only select between lin or log
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

dir_chains = 'chains/Mocks/'

#--------------------------

lnum = 2, 3, 4, 5, 6, 10, 20


for redz in redzz:
 if 'sim' in which:
     file = which +'_'+ what + '_z'+redz+'_norsd_np0.001_nRT10_r0'
 elif 'mocks' in which:
     file = which +'_RST_'+ redz + what + '_DM1_r0'
 else:
     print 'error'
     
#------------------------------

 for n in range(0,len(lnum)):
  num = lnum[n]

  wq_input = """
mode: bycore
N: 9
threads: 3
hostfile: auto
job_name: %s%i.ini
command: |
     source ~/.bashrc;
     OMP_NUM_THREADS=%%threads%% mpirun -hostfile %%hostfile%% ./cosmomc INI_%s%i.ini > %slogs/INI_%s%i.log 2>%slogs/INI_%s%i.err
  """%(file, num, file, num, dir_chains, file, num, dir_chains, file, num)

  with open('wq_%s%i.ini'%(file, num), 'w') as f:
       f.write(wq_input)

