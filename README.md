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

``read_data.py`` is used to rezise the correlation function gg and gm, and
the covariance matrix considering only values up to 70 Mpc (also eliminating the first point).

``wq_run.py `` useful to place files in the queue of the clustes.
This will produce .Ini files --for CosmoMC-- and wq scripts for the cluster.

``wq_run_plot.py``. Once you have the chains in place, run this file to
get plots: posterior distributions, best fit values -with and without non-linear
bias- and best-ft values for sigma8.


![](https://github.com/ja-vazquez/Upsilon/sigma8.jpg)