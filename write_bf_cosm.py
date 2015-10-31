# only select between lin or log
# and best-fit -> bf

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

#--------------------------------------------- 

bff = ['bf','bf_b20']
lnum =  2 , 3, 4,  5,  6,  10, 20


for bf in bff:
  for redz in redzz:
    for n in range(0,len(lnum)):
     num = lnum[n]

     if 'sim' in which: 
         file = which +'_'+ what + '_z'+ redz+ '_norsd_np0.001_nRT10_r0'
     elif 'mocks' in which:
         file = which +'_RST_'+ redz + what + '_DM1_r0'
     else:
         print 'error'


     commd = """
      ./cosmomc %s_INI_%s%i.ini
     """%(bf, file, num)
     os.system(commd)
     time.sleep(3)

