
import os, sys, time
from Ups_data import Info_model
import Ups_latex as lf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



class Ini_file(Info_model):
    def __init__(self, data_type, bin_type, redz, jack = False):
        Info = Info_model(data_type, bin_type, redz, jackknife=jack)

        self.data_type  = data_type
        self.bin_type   = bin_type
        self.redz       = redz
        self.jackknife  = jack
        self.fname      = Info.files_name()


        self.data_dir   = Info.data_dir()        
        self.dir_in     = 'data_upsilon/' + self.data_dir
        self.dir_data   = 'lrgdata-final/mocks_lrg/sim_reshaped/'
        self.dir_stats  = 'stats/'
        self.dir_bf     = 'bestfit/'
        self.dir_chains = 'chains/' + Info.chain_dir()
        
        self.name_root  = '_ups'
        self.name_ups   = '_ups.dat'
        self.name_cov   = '_cov.dat'
        self.name_dist  = 'distparams'
        self.name_gg    = '_upsgg_cov.dat'
        self.name_gm    = '_DS_gm_cov_cut.dat'        
        self.name_jk    = '_jk_stats.dat'

        self.aver       = 0.0
        self.first_point= 1
        self.last_point = 70
        self.first_line = 1
        self.z_mean     = Info.z_mean()            

	self.full_cov   = 'log'                                
        self.R0         = Info.R0_files()
        self.npoints    = Info.number_of_points()
        if len(self.R0)!= len(self.npoints):  sys.exit("Error: check number of files")
        self.R0_points  = zip(self.R0, self.npoints)
        
        
        self.write_pars = ['sigma8', 'LRGa', 'LRGb']
        #Info_model.__init__(self, data_type, bin_type, redz)
        #print self.nada



        #reshape the files provided by Sukhdeep, in order to feed them to CosmoMC
    def reshape_tables(self, R0, jk=0):
        file_in  = self.dir_in   + self.fname + str(R0)
        file_ups = self.dir_in   + self.fname + str(R0)
        file_out = self.dir_data + self.fname + str(R0)
        if self.jackknife:
            file_ups   += '_jk{0:d}'.format(jk) 
            file_out  += '_jk{0:d}'.format(jk) 
         
         
	print file_ups + self.name_ups            
        fdata = pd.read_csv(file_ups + self.name_ups,
                            sep='\s+', skiprows=[0], 
                            names = ['rp', 'upsgg', 'upsgg_err', 'upsgm', 'upsgm_err', 'upsmm', 'upsmm_err', 'DS_gm', 'DS_gm_err'])
      
        lups = len(fdata)
        fdata_no_ggpoint = fdata[['rp', 'upsgg']][self.first_line:]
        fdata_no_gmpoint = fdata[['rp', 'DS_gm']][self.first_line:]
        pd_tmp = pd.concat([fdata_no_ggpoint, fdata_no_gmpoint]).fillna(0) 
        pd_tmp['all'] = pd_tmp['upsgg'] + pd_tmp['DS_gm']
	
           
        pd_tmp[['rp', 'all']].to_csv(file_out + self.name_ups,
                            header=None, index= None, sep='\t', float_format='%15.7e')
        
            #covariace matrix for gg and gm
        table1 = np.loadtxt(file_in + self.name_gg)
        table2 = np.loadtxt(file_in + self.name_gm)
        
        new_table1 = table1[self.first_line: lups, self.first_line: lups]
        new_table2 = table2[self.first_line: lups, self.first_line: lups]    
    
        row, col = new_table1.shape
        zero= '0 '*row
        
            # we leave it in this way for now
        with open(file_out + self.name_cov, 'w') as f:
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

        print '*** ups =', len(pd_tmp[['rp', 'all']]), 'cov = ', row*2, 'R0 =', R0 
        time.sleep(1.)        
        
        
        
        #Write .INI files 
    def write_ini(self, R0, nR0, jk=0, threads=3, action=0):
        full_name = self.fname + str(R0)        
        if self.jackknife: 
            full_name += '_jk{0:d}'.format(jk)
            
        print 'Ini', full_name

        with open('INI_{}.ini'.format(full_name), 'w') as f:
            f.write(lf.text_ini_file(threads = threads, action = action))
            f.write(lf.params_upsilon())
            f.write('use_upsilon= 98\n')
            f.write('samples  = 10000000\n')

            f.write('best_fit = {0:s}best_{1:s}.dat\n'.format(self.dir_bf, full_name))
            f.write('aver     = {0:1.1f}\n'.format(self.aver if self.full_cov in self.bin_type else 0))
            f.write(lf.params_cosmo(self.data_type) + '\n\n')

            f.write('z_gg     = {}   \n'.format(self.z_mean))
            f.write('z_gm     = {}   \n'.format(self.z_mean))

            f.write(lf.R0_params(R0, nR0) + '\n')
            f.write('use_diag = {0:s}\n\n'.format('F' if self.full_cov in self.bin_type else 'T'))

            f.write('file_root = ' + self.dir_chains + full_name + self.name_root + '\n')
            f.write('mock_file = ' + self.dir_data   + full_name + self.name_ups  + '\n')
            f.write('mock_cov  = ' + self.dir_data   + full_name + self.name_cov  + '\n')
	
            time.sleep(2.)


        #Once we have the MCchains, get best-fit values
    def write_bf(self, R0, run_bf=False):
        full_name = self.fname + str(R0)
        file_bf = self.dir_stats + full_name + self.name_root + '.likestats'
        
        names   = ['param','bestfit','lower1',
                   'upper1','lower2','upper2','name','other']

        lines   =  pd.read_csv(file_bf, names= names, sep='\s+', skiprows=[0,1], index_col='name')
        print 'bf', lines

        b1_bf   =  float(lines.ix['bias_1']['bestfit'])
        b2_bf   =  float(lines.ix['bias_2']['bestfit'])
        lna_bf  =  float(lines.ix['{\\rm{ln}}(10^{10}']['bestfit'])

        with open('bf_INI_{0:s}.ini'.format(full_name), 'w') as f:
            f.write('param[LRGa] = {0:2.3f} {1:2.3f} {2:2.3f} 0.001 0.001\n'.format(b1_bf, b1_bf-0.001, b1_bf+0.001))
            f.write('param[LRGb] = {0:1.3f} {0:1.3f} {0:1.3f} 0.001 0.001\n'.format(b2_bf, b2_bf-0.001, b2_bf+0.001))
            f.write('param[logA] = {0:1.3f} {0:1.3f} {0:1.3f} 0.001 0.001\n'.format(lna_bf,lna_bf-0.001,lna_bf+0.001))
            f.write('use_upsilon = 99\n')
            f.write('samples     = 8\n')

            f.write(lf.text_ini_file())
            f.write('best_fit = {0:s}best_{1:s}.dat\n'.format(self.dir_bf, full_name))
            f.write('aver     = {0:1.2f}\n'.format(self.aver if self.full_cov in bin_type else 0))
            f.write(lf.params_cosmo(self.data_type) + '\n\n')

            f.write('z_gg     = {}   \n'.format(self.z_mean))
            f.write('z_gm     = {}   \n'.format(self.z_mean))

            f.write(lf.R0_params(R0, nR0) + '\n')
            f.write('use_diag = {}\n\n'.format('F' if self.full_cov in self.bin_type else 'T'))

            f.write('file_root = ' + self.dir_chains + 'bf_'+ full_name + self.name_root + '\n')
            f.write('mock_file = ' + self.dir_data   + full_name + self.name_ups  + '\n')
            f.write('mock_cov  = ' + self.dir_data   + full_name + self.name_cov  + '\n')

        if run_bf:
            commd = './cosmomc bf_INI_{}.ini'.format(full_name)
            os.system(commd)
            time.sleep(3.)



        #Plot best-fit model along with data and errorbars
    def plot_bf(self, R0):
        full_name = '{0:s}best_{1:s}{2:d}.dat'.format(self.dir_bf, self.fname, R0)
	
        names = ['r', 'obs', 'sig', 'theo']
        lines = pd.read_table(full_name, names=names, sep='\s+')
        split_lines = []
        for nm in names:
           split_lines.append(np.array_split(lines[nm], 2))

        fig = plt.figure(figsize=(15,6))
        ax = fig.add_subplot(1,2,1)
        ax.errorbar(split_lines[0][0], split_lines[1][0], yerr=split_lines[2][0], fmt='+')
        ax.plot(split_lines[0][0], split_lines[3][0])
        plt.xlabel('r')
        plt.ylabel('gg')
        ax.set_title('{0:s}, R0={1:d}'.format(self.redz, R0))
        plt.legend(loc="upper right")

        ax2 = fig.add_subplot(1,2,2)
        ax2.errorbar(split_lines[0][1], split_lines[1][1], yerr=list(split_lines[2][1]), fmt='+')
        ax2.plot(split_lines[0][1], split_lines[3][1])
        plt.xlabel('r')
        plt.ylabel('gm')
        ax2.set_title('{0:s}, R0={1:d}'.format(self.redz, R0))
        plt.legend(loc="upper right")

        plt.tight_layout()
        plt.savefig(full_name.replace('.dat','') + ".jpg")
        plt.show()




        #Analyze the chains
    def write_dist(self, R0, run_dist=False):
        txt='file_root=chains/Sim_rmin_gt_R0/Rmin_70_sim_z0.25_norsd_np0.001_nRT10_r02_ups'
        full_name = '{0:s}{1:d}'.format(self.fname, R0)
        print 'distpars', full_name

        txt_new = 'file_root=' + self.dir_chains + full_name + self.name_root
        f1 = open(self.name_dist + '.ini', 'r')
        f2 = open(self.name_dist + '_{}.ini'.format(full_name), 'w')

        for line in f1:
            f2.write(line.replace(txt, txt_new))
        f1.close()
        f2.close()

        if run_dist:
            commd = """./getdist {0:s}_{1:s}.ini""".format(self.name_dist, full_name)
            os.system(commd)
            time.sleep(0.5)




        #Write a bunch of files that will run everything in the BNL cluster
    def write_wq(self, R0, jk=0, run_wq=False, nodes=12, threads=3):
        full_name = self.fname + str(R0)        
        if self.jackknife: 
            full_name += '_jk{0:d}'.format(jk)
        print 'wq', full_name

        with open('wq_{0:s}.ini'.format(full_name), 'w') as f:
            f.write('mode: bycore\n')
            f.write('N: {0:d}\n'.format(nodes))
            f.write('threads: {0:d}\n'.format(threads))
            f.write('hostfile: auto\n')
            f.write('job_name: {0:s}\n'.format(full_name))
            f.write('command: |\n')
            f.write('     source ~/.bashrc; \n')
            f.write('     OMP_NUM_THREADS=%threads% mpirun -hostfile %hostfile% '
                    './cosmomc INI_{name:s}.ini > {dir:s}logs/INI_{name:s}.log 2>{dir:s}logs/INI_{name:s}.err'.format(name=full_name, dir=self.dir_chains))

        if run_wq:
            commd="""nohup wq sub wq_{0:s}.ini &""".format(full_name)
            os.system(commd)
            time.sleep(2.)



        #Collect chisq from all the models
    def write_chisq(self, R0):
        full_name = '{0:s}{1:d}'.format(self.fname, R0)
        file_chisq = self.dir_chains + full_name + self.name_root + '.minimum'

        with open(file_chisq, 'rb') as f:
            for line in f:
                if 'chi-sq    =' in line:
                    best_fit_line = line

        bf = float(best_fit_line.strip().split('=')[-1])
        with open('chisq_' + self.fname + '.dat', 'a') as f:
            f.write('{0:d} \t {1:f} \n'.format(R0, bf))



        #Collect info from the 100 jacknives
    def write_jk(self, R0, jk):
        full_name = self.fname + str(R0) + '_jk{0:d}'.format(jk)  + '_ups.minimum' 
        read_jk = pd.read_csv(self.dir_chains + full_name,
                                names = ['npar', 'value', 'name', 'latex', 'other'],
                                skiprows=[0,1,2], sep='\s+', index_col=['name'])
         
                               
        write_jk       = read_jk.ix[self.write_pars, ['value']].T  
        write_jk['jk'] = jk        
        write_jk.to_csv(self.fname + self.name_jk, mode='a', index=None, sep='\t', header=None)




    def plot_jk(self, R0):
        jks = ['jk']
        self.write_pars.extend(jks)
        jk_stat = pd.read_csv(self.fname + self.name_jk, names = self.write_pars,  sep='\s+')
        
            # just test
        fig = plt.figure(figsize=(15,6))
        ax1 = fig.add_subplot(1,3,1)
        ax2 = fig.add_subplot(1,3,2)
        ax3 = fig.add_subplot(1,3,3)
        ax = [ax1, ax2, ax3]
        for i,x in zip(self.write_pars, ax):
            if i is not 'jk':
                print i, jk_stat[i].mean(), '+/-', jk_stat[i].std()*10.
                jk_stat.plot.scatter(x='jk', y=i, ax=x)
        plt.show()
        





class Chisq:
    def __init__(self, data_type, bin_type, redzz):
        Info = Info_model(data_type, bin_type, redz)
        self.data_type= data_type
        self.bin_type = bin_type
        self.redzz     = redzz
        self.fname      = Info.files_name()

    def plot_chisq(self):
        chisq_all, R0_all =[], []
        for redz in self.redzz:
            file_name = 'chisq_' + self.fname + '.dat'
            lines     =  pd.read_csv(file_name, names= ['R0', 'chisq'], sep='\s+')

            chisq_all.append(lines['chisq'])
            R0_all.append(lines['R0'])

        fig = plt.figure(figsize=(15,6))
        ax = fig.add_subplot(1,1,1)
        for i, k in enumerate(self.redzz):
            ax.plot(R0_all[i], chisq_all[i], label = k)
        plt.xlabel('R0')
        plt.ylabel('Chisq')
        plt.title('chi-sq - Full covariance matrix')
        plt.legend(loc="upper right")
        plt.grid()
        plt.xlim([1,11])
        plt.savefig("chisq.jpg")
        plt.show()




if __name__=='__main__':

    mocks     = True
       
    MCMC      = True
    jack      = False
    chisq     = False

    if mocks:
       data_type = 'mocks'
       bin_type  = 'logre1'
       redzz     = ['singlesnap'] #,'allsnap', 'evol']
    else:
       data_type = 'lowz'
       bin_type  = 'log1_rebin'
       redzz     = ['lowz']

    
    for redz in redzz:
        Ini = Ini_file(data_type, bin_type, redz, jack= jack)
        for R0_points in Ini.R0_points:
            R0, nR0 = R0_points 
            for jk in np.arange(100 if jack else 1):
                if R0== 4: 
                   print R0_points, 'jk=', jk
                   if jack:
                      Ini.write_ini(R0, nR0, jk=jk,      threads=1, action=2)
                      Ini.write_wq(R0, jk=jk, run_wq=True, nodes=1, threads=1)
                      Ini.write_jk(R0, jk)
                      Ini.plot_jk(R0)
                   if MCMC:
                      Ini.reshape_tables(R0, jk=jk)
                      Ini.write_ini(R0, nR0, jk=jk)
                      #Ini.write_wq(  R0, jk=jk, run_wq  =True)
                      #Ini.write_dist(R0,        run_dist=True)
                      #Ini.write_bf(  R0,        run_bf  =True)
                      #Ini.plot_bf(   R0)              
                   if chisq:   
                      Ini.write_ini(R0, nR0,      threads=1, action=2)
                      Ini.write_wq(R0, run_wq=True, nodes=1, threads=1)
                      Ini.write_chisq(R0)
  
    if chisq:
        chi = Chisq(data_type, bin_type, redzz)
        chi.plot_chisq()



"""
reshape_tables -> clean and reshape files provided by Sukhdeep

write_ini  - > writes .INI files as the input of SimpleMC
write_wq   - > writes .wq files as the input to the BNL cluster
write_jk   - > cleans the 100 jk files for plotting
write_chisq- > collect chisqs from different R0 and models
write_dist - > once we have the MCchains, write files to analyzed them
write_bf   - > once analyzed the chians, get best-fit values

plot_bf    - > plot best-model along with data and errorbars
plot_jk    - > plots points for each jks and displays stats  
plot_chisq - > plots chisq for models and R0
"""

