# only select between lin or log

import os, sys, time

which = 'mocks' #'sim'
what = 'lin1' #'log_rebin1'
redz = 'steps_' #'0.40'

Plot_all = True

#---------------------------------------------------

commd0 = """
cd bestfit/
rm best_%s_fit_z%s*.dat
rm best_sigma8_%s_%s*.dat
cd ..
"""%(what,redz,what,redz)

commd = """
python write_dist.py %s %s %s
python write_bf_ini.py %s %s %s
"""%(which,what, redz, which,what, redz)

commd2 = """
python write_bf_b20_ini.py %s %s %s
"""%(which, what, redz)

commd3 = """
python write_bf_cosm.py  %s %s %s
python write_s8.py %s %s %s
python write_plot_s8.py %s %s %s
"""%(which,what, redz, which,what, redz, which,what, redz)

commd4 = """
python write_plot_bf.py %s %s %s
"""%(which,what, redz)


os.system(commd0)
time.sleep(0.1)

os.system(commd)
time.sleep(0.1)

if (Plot_all):
  os.system(commd2)
  time.sleep(0.1)

os.system(commd3)
time.sleep(0.1)

if (Plot_all):
  os.system(commd4)
  time.sleep(0.1)
