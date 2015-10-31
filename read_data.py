# Script to read Sukhdeep files and modify their format to a CosmoMC
import numpy as np

which = 'mocks'			#sim or mocks

if 'sim' in which:	
   what = 'lin_bin1'		#lin or log / bin or rebin
   dir  = 'sim_results/'
elif 'mocks' in which:
   what = 'lin1'		#lin1 or rebin1
   dir  = 'mock_results/'
#------------------------------------------


file_dir  = 'sim_files/lowz_clustering_lensing/'+dir
dir_out   = 'sim_reshaped/'
name_gg   = '_upsgg_cov.dat'
name_gm   = '_upsgm_cov.dat'
name2     = '_ups.dat'

lnum  =  2, 3, 4, 5, 6, 10, 20

last_point = 70
fline = 1

#---------------------------------------------

if 'sim' in which:
    redzz = ['0.25','0.40']
elif 'mocks' in which:
    redzz = ['steps_',''] 
else:
    print 'error'


for redz in redzz:
 if 'sim' in which:
     file_name = which +'_'+ what +'_z'+ redz +'_norsd_np0.001_nRT10_r0'
 elif 'mocks' in which:
     file_name = which +'_RST_'+ redz + what + '_DM1_r0'
 else:
     print 'error'


#------------------------------------------------------


 for n in range(0,len(lnum)):
   num = lnum[n]

   fdata     = open(file_dir + file_name + str(num) + name2)
   file_read = fdata.readlines()
   lfile     = len(file_read)

   rp     = []
   ups_gg = []
   ups_gm = []

  
   for l in range(lfile):
	vals = file_read[l].split()
	if vals[0] != '#':
	   if (float(vals[0])< last_point): 
		rp.append(vals[0])
		ups_gg.append(vals[1])
		ups_gm.append(vals[3])
   lups =  len(ups_gg)
   fdata.close()

   i = 0	
   #new Format file
   with open(dir_out + 'new_' + file_name+str(num) + name2, 'w') as f:
        for l in range(fline, lups ):
   	    f.write(str(rp[l] + '\t' + ups_gg[l] + '\n'))
        for l in range(fline, lups ):
	    f.write(str(rp[l] + '\t' + ups_gm[l] + '\n'))		     	
	    i+=1
   print 'R0', num, 'len_file',i*2


   # New cov matrix
   table1 = np.loadtxt(file_dir + file_name + str(num) + name_gg)
   table2 = np.loadtxt(file_dir + file_name + str(num) + name_gm)

   new_table1 = table1[fline: lups, fline: lups]
   new_table2 = table2[fline: lups, fline: lups]

   row, col = new_table1.shape
   zero= '0 '*row


   with open(dir_out + 'new_' + file_name + str(num) + '_cov.dat', 'w') as f:
    for n in range(row):
        for m in range(col):
            f.write(str("%1.3e" %float(new_table1[n,m])) + ' ')
        f.write(zero)
        f.write('\n')
    
    for n in range(row):
        f.write(zero)
        for m in range(col):
            f.write(str("%1.3e" %float(new_table2[n,m])) + ' ')
        f.write('\n')

   print 'rows =',row*2, 'cols = ', col*2 


