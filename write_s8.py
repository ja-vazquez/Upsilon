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

#--------------------------

lnum =  2 , 3, 4,  5,  6,  10, 20


for redz in redzz:
  if 'sim' in which:
      file = which +'_'+ what + '_z'+ redz+ '_norsd_np0.001_nRT10_r0'
  elif 'mocks' in which:
      file = which +'_RST_'+ redz + what + '_DM1_r0'
  else: 
      print 'error'

        #number of files
  for n in range(0,len(lnum)):
   num = lnum[n]

        # read best fit values
   if 'sim' in which:
     file_bf = 'stats/Re_sim_%s_z%s_norsd_np0.001_nRT10_r0%i_ups.margestats'%(what,redz,num)
   elif 'mocks' in which:
     file_bf = 'stats/Re_%s_RST_%s%s_DM1_r0%i_ups.margestats'%(which,redz,what, num)

   bf_lines = open(file_bf,'r').readlines()
   i=0
   bf, sig1, sig2, sig3, sig4 = [], [], [], [], []
   for lines in bf_lines:
       if i> 2:
          vals = lines.split()[0:]
          bf.append(float(vals[1]))
 	  sig1.append(float(vals[3]))
	  sig2.append(float(vals[4]))
	  sig3.append(float(vals[6]))
 	  sig4.append(float(vals[7]))
       i+=1

   with open('bestfit/best_sigma8_%s_%s.dat'%(what,redz), 'a') as f:
	f.write("%i \t %2.6f \t %2.6f \t %2.6f \t %2.6f \t %2.6f \n"%(num, bf[2], bf[2]-sig1[2], sig2[2]-bf[2], bf[2]-sig3[2],  sig4[2] -bf[2] ))
