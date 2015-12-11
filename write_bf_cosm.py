# only select between lin or log
# and best-fit -> bf

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

#--------------------------------------------- 

bff  = ['bf', 'bf_b20']
lnum =  R0_files()

for bf in bff:
  for redz in redzz:
    for _,num in enumerate(lnum):
	file  = files_name(data_type, bin_type, redz)
    
        commd = """
         ./cosmomc %s_INI_%s%i.ini
        """%(bf, file, num)
        os.system(commd)
        time.sleep(3)

