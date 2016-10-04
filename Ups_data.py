
def print_message():
       print """select sim/mocks/lowz
                lin1:log / bin:rebin1 / lowz:z1:z2
                [0.25,0.40]/[steps_,]/[log1,log1_rebin]"""


    # Most of these parameters are given by Sukhdeep
    # so be careful as they may change
class Info_model:
    def __init__(self, data_type, bin_type, redz, jackknife=False):
        self.data_type = data_type
        self.bin_type  = bin_type
        self.redz      = redz
        self.jackknife = jackknife

	self.sim  = 'sim'
	self.mocks= 'mocks'
	self.lowz = 'lowz'

        self.nada = 'nothing'


        #select file's name
    def files_name(self):
        fname = {self.sim  : self.data_type    + '_' + self.bin_type + '_z' + self.redz + '_norsd_np0.001_nRT10_r0',
                 self.mocks: '{}'.format(self.redz) + '_r0',
                 self.lowz : self.redz + '_'   + self.bin_type + '_r0'}
        return fname[self.data_type]



        #select chains's folder
    def chain_dir(self):
        chdir = {self.sim  : 'Sim',
                 self.mocks: 'Mocks',
                 self.lowz : 'Lowz'}
        ch = chdir[self.data_type]

        if self.jackknife: ch += '_jk'
        return ch + '/'


        #select data's folder
    def data_dir(self):
        ddir = {self.sim  : 'sim_results/',
                self.mocks: 'mock_results/{0:s}/{1:s}/'.format(self.redz, self.bin_type),
                self.lowz : 'lowz_results/'
                }
        return ddir[self.data_type]



        # will read this number from a file later
    def R0_files(self):
        return 1, 1.5, 2, 3, 4, 5, 6, 10



        # will read this number from a file later
    def  number_of_points(self):
        data_type = self.data_type
        bin_type  = self.bin_type

        if self.sim in data_type:
            if 'lin_bin1' in bin_type:
                lnp = 102, 90, 82, 74, 70, 54, 34
            elif 'log_rebin1' in bin_type:
                lnp = 22, 18, 18, 16, 16, 12, 8

        elif self.mocks in data_type:
            if 'lin1' in bin_type:
                lnp  =  134, 132, 130, 128, 126, 118
            elif 'logre1' in bin_type:
                lnp = 28, 26, 24, 20, 18, 16, 16, 12

        elif self.lowz in data_type:
            if 'rebin' in bin_type:
                lnp =  28, 28, 28, 28, 28, 28
            else:
                lnp = 184, 164, 148, 136, 126, 100

        else:       print 'error'
        return lnp


        #select redshift
    def z_mean(self):
        if self.sim in self.data_type:
            return self.redz
        elif self.lowz in self.data_type:
            z = {'lowz': '0.27', 'z1': '0.21', 'z2': '0.31'}
            return z[self.redz]
        else:
            return '0.267'




if __name__ == '__main__':
    info = Info_model('nada')
    print info.name
