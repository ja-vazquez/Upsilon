# Script to read Sukhdeep files and modify their format to a CosmoMC

import numpy as np
from Useful_data import *
from Useful_files import *
import pandas as pd



data_type = 'mocks'			    #sim, mocks,lowz
jackknife  = False                   #True


class Read_data:
    def __init__(self, data_type, bin_type, redz):
        info = Info_model(data_type, bin_type, redz)
        self.data_type =  data_type
        self.bin_type  = bin_type
        self.redz      = redz
        self.fname     = info.files_name()

        self.data_dir  = info.data_dir()
        self.njacks    = 100 if jackknife else 1

        self.dir_in  = '/Users/josevazquezgonzalez/Desktop/Ups/Git/Upsilon/data/'
        self.dir_out   = '/Users/josevazquezgonzalez/Desktop/Ups/Git/Upsilon/data/reshaped/'
        self.name_gg   = '_upsgg_cov.dat'
        self.name_gm   = '_upsgm_cov.dat'
        self.name_ups  = '_ups.dat'
        self.name_cov  = '_cov.dat'


        self.R0          = info.R0_files()
        self.first_point = 1         #select the range of points
        self.last_point  = 70
        self.first_line  = 1				#skip first line

 #if jackknife:
 #   name_ups = '_jk%i'%(i) + name_ups
 #   name_cov = '_jk%i'%(i) + name_cov


    def reshape_tables(self, R0):
        file_in  = self.dir_in + self.fname + str(R0)
        file_out = self.dir_out + self.fname + str(R0)
        
        fdata = pd.read_csv(file_in + self.name_ups,
                            sep='\s+', skiprows=[0], 
                            names = ['rp', 'upsgg', 'upsgg_err', 'upsgm', 'upsgm_err', 'upsmm', 'upsmm_err'])
      
        lups = len(fdata)
        pd_tmp = pd.concat([fdata[['rp', 'upsgg']], fdata[['rp', 'upsgm']]]).fillna(0) 
        pd_tmp['all'] = pd_tmp['upsgg'] + pd_tmp['upsgm']
        
        pd_tmp[['rp', 'all']].to_csv(file_out + self.name_ups,
                            header=None, index= None, sep='\t', float_format='%15.7e')
        
        

        table1 = np.loadtxt(file_in + self.name_gg)
        table2 = np.loadtxt(file_in + self.name_gm)
        
        new_table1 = table1[self.first_line: lups, self.first_line: lups]
        new_table2 = table2[self.first_line: lups, self.first_line: lups]    
    
        row, col = new_table1.shape
        zero= '0 '*row
        
        
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

        print '*** rows =',row*2, 'cols = ', col*2, 'R0 =', R0 
        
    

if __name__ == '__main__':

    if True:
       data_type = 'mocks'
       bin_type  = 'rebin1'
       redzz     = ['singlesnap'] #,'allsnap', 'evol']


    for redz in redzz:
        Ini = Info_model(data_type, bin_type, redz)
        Rdata= Read_data(data_type, bin_type, redz)
        for R0_points in Ini.R0_files():
            if True:
                Rdata.reshape_tables(R0_points)


