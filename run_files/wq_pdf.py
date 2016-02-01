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
         redzz = ['DM1','DM2']
else:
   print 'select sim/mocks  lin2/rebin2  [0.25,0.40]/[DM1]'

#---------------------------------------

if 'sim' in which:
    lnum  = 2, 3, 4, 5, 6, 10, 20
    if 'lin2' in what:
        extra = '_lin_bin2'
    elif 'rebin2' in what:
        extra = '_lin_rebin2'
elif 'mocks' in which:
    lnum  =  2, 3, 4, 5, 6, 10
    if 'lin2' in what:
        extra = '_lin2'
    elif 'rebin2' in what:
        extra = '_rebin2'

for redz in redzz:
 if 'sim' in which:
     file = 'sim'+ extra+ '_z'+redz +'_norsd_np0.001_nRT10_r0'
 elif 'mocks' in which:
     file = 'mocks' + extra + '_' + redz + '_pi100_r0'

 for n in range(0,len(lnum)):
  num = lnum[n]
  commd = """
  python stats/Re_%s%i_ups_tri.py 
  """%(file, num)
  os.system(commd)
  time.sleep(0.1)
