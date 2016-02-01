


def file_choice(data_type):
	#Select the type of file to analyze
    if 'sim' in data_type:
       bin_type = 'lin_bin1'                #lin or log / bin or rebin
       redzz = ['0.25','0.40']
       dir  = 'sim_results/'

    elif 'mocks' in data_type:
       bin_type = 'lin1'                    #lin1 or rebin1
       redzz = ['steps_','']
       dir  = 'mock_results/'

    elif 'lowz' in data_type:
       bin_type = 'log1_rebin'              #log1 or log1_rebin
       redzz = ['z1'] #, 'z1', 'z2']
       dir = 'lowz_results/'

    return bin_type, redzz, dir



def files_name(data_type, bin_type, redz):
	#select the file's name
     if 'sim' in data_type:
        file_name = data_type +'_'+ bin_type +'_z'+ redz +'_norsd_np0.001_nRT10_r0'
     elif 'mocks' in data_type:
        file_name = data_type +'_RST_'+ redz + bin_type + '_DM1_r0'
     elif 'lowz' in data_type:
        file_name =  redz + '_' + bin_type + '_r0'
     else:
        print 'error'    
    
     return file_name


def R0_files():
    lnum = 2, 3, 4, 5, 6, 10
    return lnum

