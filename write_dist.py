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

name = 'distparams'
chain_dir = 'chains/Mocks/'


#--------------------------------------------

lnum =  2, 3, 4,  5,  6,  10, 20

	# Don't change this line unless modify disparams
txt='file_root=chains/Sim_rmin_gt_R0/Rmin_70_sim_z0.25_norsd_np0.001_nRT10_r02_ups'

print txt

for redz in redzz:
 for n in range(0,len(lnum)):
   num = lnum[n]
   
   if 'sim' in which:
      txt_new = 'file_root=%s/Re_%s_%s_z%s_norsd_np0.001_nRT10_r0%i_ups'%(chain_dir,which,what,redz, num)
   elif 'mocks' in which:
      txt_new = 'file_root=%sRe_%s_RST_%s%s_DM1_r0%i_ups'%(chain_dir,which,redz,what, num)
   else:
      print 'error' 

   f1 = open(name+'.ini', 'r')
   f2 = open(name+'_%s_%s%i.ini'%(what, redz, num), 'w')
   for line in f1:
      f2.write(line.replace(txt, txt_new))
   f1.close()
   f2.close()


   commd = """
    ./getdist %s_%s_%s%i.ini
   """%(name,what,redz,num)
   os.system(commd)
   time.sleep(0.2)

