# only select between lin or log
# and best-fit -> bf
import os, sys, time
from Useful import *


        #lin or log, sim or mocks
if len(sys.argv) > 2:
    data_type ='%s'%(sys.argv[1])
    bin_type  ='%s'%(sys.argv[2])
    if len(sys.argv) > 3:
       redzz  = ['%s'%(sys.argv[3])]
else:
    print_message()

#--------------------------------------------

name_dist = 'distparams'
name_root = '_ups'

chain_dir = chain_dir(data_type)
lnum      = R0_files()
extra     = extra()
 
	# Don't change this line unless modify disparams
txt='file_root=chains/Sim_rmin_gt_R0/Rmin_70_sim_z0.25_norsd_np0.001_nRT10_r02_ups'

for redz in redzz:
   for _, num in enumerate(lnum): 
      file    = files_name(data_type, bin_type, redz)
      file_num_extra = '%s%i%s'%(file, num, extra)
 
      txt_new = 'file_root=' + chain_dir  + file_num_extra + name_root

      f1 = open(name_dist + '.ini', 'r')
      f2 = open(name_dist + '_%s.ini'%(file_num_extra), 'w')
      for line in f1:
         f2.write(line.replace(txt, txt_new))
      f1.close()
      f2.close()


      commd = """./getdist %s_%s.ini"""%(name_dist, file_num_extra)
      os.system(commd)
      time.sleep(0.5)

