# only select between lin or log

import os, sys, time

#Check Useful.py for info

data_type = 'lowz' 
bin_type  = 'log1' 
redz      = 'z2' 

Plot_all = True

#---------------------------------------------------

commd0 = """
cd bestfit/
rm best_%s_fit_%s*.dat
rm best_sigma8_%s_%s*.dat
cd ..
"""%(bin_type,redz,bin_type,redz)

commd = """
python write_dist.py %s %s %s
python write_bf_ini.py %s %s %s
"""%(data_type,bin_type, redz, data_type,bin_type, redz)

commd2 = """
python write_bf_b20_ini.py %s %s %s
"""%(data_type, bin_type, redz)

commd3 = """
python write_bf_cosm.py  %s %s %s
python write_s8.py %s %s %s
python write_plot_s8.py %s %s %s
"""%(data_type,bin_type, redz, data_type,bin_type, redz, data_type,bin_type, redz)

commd4 = """
python write_plot_bf.py %s %s %s
"""%(data_type,bin_type, redz)


#os.system(commd0)
#time.sleep(0.5)

os.system(commd)
time.sleep(0.5)

if (Plot_all):
  os.system(commd2)
  time.sleep(0.5)

os.system(commd3)
time.sleep(0.5)

if (Plot_all):
  os.system(commd4)
  time.sleep(0.5)
