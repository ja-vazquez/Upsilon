# Upsilon
Module to analize measurements of galaxy-galaxy weak lensing and galaxy clustering.
Calculation are based on [Rachel's paper](http://arxiv.org/abs/1207.1120v3).

Some of the improvements, compared to previous versions, are:

* The computation of the non-linear power spectrum up to k~1 h/Mpc using the 
        [Coyote emulator](http://www.hep.anl.gov/cosmology/CosmicEmu/emu.html). We may consider the [HMcode](https://github.com/alexander-mead/hmcode) later.
 
* To compute correlation fuctions, and speed things up, we have incorporated the fast fourier transform ([FFTLog](http://casa.colorado.edu/~ajsh/FFTLog/#motivation)). 
 
* For each set of cosmological parameters, we are now able to compute Non-linear corrections to the real space correlation function, as in Figure 3 of [arxiv:0911.4973](http://arxiv.org/abs/0911.4973). 

###Data
Data files for mocks/simulations provided by Sukhdeep are located
in [Bitbucket](https://bitbucket.org/sukhdeep89/lowz_clustering_lensing).

###Files 

``read_data.py`` is used to clean and give the appropiate format to the data provided by Sukhdeep: 
rezised the correlation function gg and gm, and
the covariance matrix considering only values up to 70 Mpc (also eliminating the first point).

* input options for simulations, mocks, lowz and/or jackknives 
can be found in the *Useful_data.py* file

``Upsilon_mock`` contains the main module. 
Some of the option (found in the *Useful.py* file) are: 

* *use coyote = F*  (standard option added by Anze in the previous paper), in which the Power spectrum is linear and the correlation function is computed as follows:
	* *upsilon_option = 1* : to compute the linear correlation function (Xi)
	by an straighforward integration.
	* *upsilon_option = 2* : to include an approximation to the non-liear  correlation function (XiCorr) by an straighforward integration.
	
	
* *use_coyote = T* : to compute the non-linear power spectrum, and use FFTlog
for outputting the correlation function. 

* *use_XiAB = T* : to incorporate the 'proper' non-linear corrections to the correlation function.

**wq_files** make all the work!!:

``wq_run.py `` useful to place files in the queue of the bnl/astro cluster.
This will produce .Ini files --for CosmoMC-- and wq scripts for the cluster.

* contains an option: *jackknife = True*, but it requires *action = 2* in
the .ini file

``wq_run_plot.py``. Once you have the chains in place, run this file to
get plots: posterior distributions, best fit values -with and without non-linear
bias- and best-ft values for sigma8.

**write_files** are useful to write the .Ini files (to run CosmoMC),
to write wq_files (to run in the BNL cluster), to write dist_files (to analyse
chains using getdist), to write bf_files (bestfit values) and finally to 
write plot_files (to plot best-fit values of gg and gm along with data; and
to plot best-fit for simga8/b1/b2)

``jacknife.py``: plots best-fit values and 1sigma errorbars
extracted from the jacknives. 

###Fiducial values 
* for mocks: h = 0.677, Omega_lamda= 0.692885, Omega_matter= 0.307115, Omega_baryons= 0.048206, n=0.96

* for sims:  Omega_m = 0.292, Omega_b h^2 = 0.022, h=0.69, ns=0.965

* mean redshift: z= 0.267

![](https://github.com/ja-vazquez/Upsilon/blob/master/sigma8.jpg)

###Preliminary results

see
[Results](https://github.com/ja-vazquez/Upsilon/tree/master/Results)
[Notebook](http://nbviewer.jupyter.org/github/ja-vazquez/Upsilon/blob/master/Upsilon_plots.ipynb)
