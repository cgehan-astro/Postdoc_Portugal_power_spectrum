### Create the appropriate environment with anaconda: conda env create -f environment.yml
### python=3.9.25, ipython=8.15


### This program aims at building a Lomb-Scargle power spectrum from a light curve, i.e. variation of flux over time

import numpy as np
import pylab as plt
import gatspy.periodic as gp
import os
from astropy.io import fits


### Function computing the Lomb-Scargle power spectrum from a light curve

def ps_lomb_scargle(time, flux):
	time = time - time[0]				# shifting the time so that the initial value corresponds to zero
	nyq = 1.0 / (2.0 * np.median(np.diff(time)))	# computing the Nyquist frequency
	df = 1.0 / np.max(time)				# computing the minimum frequency; defines the desired frequency resolution in the Lomb Scargle power spectrum
	Nf = 1 * nyq/df					# defining the desired number of frequencies in the Lomb Scargle power spectrum; the maximum frequency corresponds here to the Nyquist frequency
	f, p = gp.lomb_scargle_fast.lomb_scargle_fast(time, flux, f0=0, df=df, Nf=Nf)		# computing the raw Lomb Scargle power spectrum;
												# f0 and df is the minimum frequency, df the frequency resolution, Nf the number of output data points
	f = f * 1e6					# output frequency in muHz
	
	
	## Converting the power into a power spectral density: the raw power p is a dimensionless, normalized quantity

	lhs = np.sum(flux**2) / float(time.size)	# normalized sum of the squared flux in ppm**2
	rhs = np.sum(p)					# normalized sum of the power (p is already normalized)
	ratio = lhs / rhs
	p = p * ratio / (df * 1e6)			# output power spectral density in ppm**2/muHz; df is in Hz
	return f, p



### Reading the data: flux versus time

fichier = '375120406.fits'
hdul = fits.open(fichier)
data_ini = hdul[1].data
list_data = []
for i in range(data_ini.size):
	list_data.append(np.array(data_ini[i]))
data = np.array(list_data)
time = np.array(data[:,0]) * 24 * 3600		# time in secs (initially in days)
flux = np.array(data[:,1])
flux = (flux - np.median(flux))			# flux in ppm; we center the flux around zero to highlight the flux variations



### Compute the frequencies and power spectral densities

freq, psd = ps_lomb_scargle(time, flux)



### Plotting the light curve and the resulting power spectrum

time_plot = time / (24*3600)		# converting the time in secs
plt.figure()
plt.plot(time_plot, flux)
plt.xlim(np.min(time_plot), np.max(time_plot))
plt.xlabel(r't' + ' (days)', fontsize='x-large')
plt.ylabel('Flux (ppm)', fontsize='x-large')
plt.savefig('Light_curve.pdf')
plt.close()

plt.figure()
plt.plot(freq, psd)
plt.yscale('log')
plt.xlim(np.min(freq), np.max(freq))
plt.xlabel(r'$\nu$' + ' (' + r'$\mu$' + 'Hz)', fontsize='x-large')
plt.ylabel(r'$P$' + ' (ppm' + r'$^2/\mu$' 'Hz)', fontsize='x-large')
plt.savefig('Power_spectrum.pdf')
plt.close()



### Writing the output frequencies and power spectral densities into a file

output_path = './375120406_power_spectrum.txt'
if os.path.exists(output_path) == False:
	fichier = open(output_path, "w")
	size_freq = np.size(freq)
	for j in range(size_freq):
		fichier.write(str('%.8f' % freq[j]) + '		' + str('%.8f' % psd[j]) + '\n')
	fichier.close()

