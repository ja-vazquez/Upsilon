# only select between lin or log

import os, sys, time
from Useful import *


#----------------------------------

commd = """
rm INI_mocks*
rm INI_z*
rm bf_INI*
rm *hostfile
rm wq_l*
rm wq_mocks*
"""
os.system(commd)
time.sleep(0.5)
