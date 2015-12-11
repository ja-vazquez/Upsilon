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

#--------------------------

#extra     = extra()

lnum =  R0_files()
dir_chains = chain_dir(data_type)

for redz in redzz:
    file  = files_name(data_type, bin_type, redz)
     
    for _, num in enumerate(lnum): 
	file_num_extra = '%s%i%s'%(file, num, extra)
        wq_input = """
mode: bycore
N: 1
threads: 1
hostfile: auto
job_name: %s
command: |
     source ~/.bashrc;
     OMP_NUM_THREADS=%%threads%% mpirun -hostfile %%hostfile%% ./cosmomc INI_%s.ini > %slogs/INI_%s.log 2>%slogs/INI_%s.err
        """%(file_num_extra, file_num_extra, dir_chains, file_num_extra, dir_chains, file_num_extra)

        with open('wq_%s.ini'%(file_num_extra), 'w') as f:
            f.write(wq_input)

