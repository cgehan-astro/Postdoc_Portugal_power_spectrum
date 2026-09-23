### Project: time_serie_to_fourier_spectrum.py

I completed this project during my postdoc in Porto, Portugal (2019 - 2021).


### Project overview

This project aims at building a Lomb-Scargle power spectrum from a light curve, i.e. flux time-serie, where the flux comes from stars.


### Dataset

The dataset is composed of light curves; one is provided as an example here: 375120406.fits.


### Methodology

The light curves are not always evenly spaced in time, therefore it is safer to use the Lomb-Scargle periodogram that is designed for unevenly spaced time-series data, instead of the standard Fourier Transform that requires evenly spaced data points. The Lomb-Scargle power spectrum is computed with a frequency resolution corresponding to the inverse of the maximum time in the light curve, and a number of output frequencies that is scaled so that the maximum computed frequency corresponds to the Nyquist frequency, in order to not undersample the signal and to reconstruct it without distortion. The output raw power is dimensionless, therefore the final step consists in converting it into a physical unit: the power spectral density.


### Results

The resulting power spectrum is saved in the file 375120406_power_spectrum.txt, where the first column indicates the frequency in muHz and the second column indicates the power spectral density in ppm**2/muHz. Additionally, two plots are saved. The first plot is Light_curve.pdf and shows the light curve, i.e. the flux time-serie, which has been recorded for an observed star over a time span of about 150 days. The second plot is Power_spectrum.pdf and shows the corresponding power spectrum that results from the Lomb-Scargle approach, i.e. the power spectral density as a function of frequency; we can see a power excess around 40 muHz that corresponds to stellar oscillation modes caused by the propagation of internal waves inside stars, which allow us to probe the interior of stars: this field is called asteroseismology, i.e. stellar seismology that works on principle similar as for Earth's seismology.


### Installation: with anaconda

git clone https://github.com/cgehan-astro/Postdoc_Portugal_power_spectrum.git
cd Postdoc_Portugal_power_spectrum
conda env create -f environment.yml
