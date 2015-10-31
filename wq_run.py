# only select between lin or log

import os, sys, time

        #lin or log, sim or mocks
  
which = 'mocks'
whatt  = ['lin1'] #'lin_bin2','lin_rebin2']


#----------------------------------
lnum  = 2, 3, 4, 5, 6, 10, 20

for what in whatt:
  if 'sim' in which:
    redzz = ['0.25','0.40']

  elif 'mocks' in which:
    redzz = ['steps_','']
    
  else:
    print 'error'

  for redz in redzz:
    if 'sim' in which:
       file = which + '_' + what + '_z'+ redz +'_norsd_np0.001_nRT10_r0'
    elif 'mocks' in which:
       file = which + '_RST_' + redz + what + '_DM1_r0'
    else:
       print 'error' 

    for n in range(0,len(lnum)):
      num = lnum[n]
      commd = """
      python write_ini.py %s %s %s 
      python write_wq.py %s %s %s
      nohup wq sub  wq_%s%i.ini &
      """%(which, what, redz, which, what, redz, file, num)
      os.system(commd)
      time.sleep(0.1) 

