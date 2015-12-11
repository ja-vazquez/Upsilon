# only select between lin or log

import os, sys, time
from Useful import *

        #lin or log, sim or mocks
  
data_type = 'lowz'

bin_type, redzz, dir = file_choice(data_type)

#----------------------------------
lnum  = R0_files()

for i in range(100):
  extra = '_jk%i'%(i)
  for bin in bin_type:
     for redz in redzz:
        file = files_name(data_type, bin, redz)
        for num  in lnum: 
           commd = """
             python write_ini.py %s %s %s %s
             python write_wq.py %s %s %s %s
             nohup wq sub  wq_%s%i%s.ini &
           """%(data_type, bin, redz, extra, data_type, bin, redz, extra, file, num, extra)
           os.system(commd)
           time.sleep(0.5) 

