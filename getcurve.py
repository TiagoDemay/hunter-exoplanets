import os
import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

missao = os.environ.get('MISSION')
setor = os.environ.get('SECTOR')
target_id = os.environ.get('TARGERT_ID')
#missao=input("Qual é a Missão? ")
#setor=input("Qual é o setor? ")
#target_id = input("Nos dê o seu TargetID: ")
search_result = lk.search_lightcurve(target_id, mission=missao, sector=setor)
#search_result = lk.search_lightcurve('TIC 251848941', mission='TESS', sector=2)

lc = search_result.download(quality_bitmask='default')
lc = lc.remove_nans().remove_outliers()
lc.scatter()
filename = "output/%s.fits" % target_id
lc.to_fits(path=filename, overwrite=True)

# Number of cadences in the full light curve
#cadencia_max=lc.time.shape
#cadencia_max=cadencia_max[0]
#lista=[]
#for n in range(1,cadencia_max,5):
#    lista.append(n)
    #print(lista)

#for l in range(0,6):
    # Create array of periods to search
#    period = np.linspace(lista[l], lista[l+1], 10000)
    # Create a BLSPeriodogram
#    bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500)
#    bls.plot()
#    plt.savefig('output/{}_{}.png'.format(l,l+1))

#lc=lk.read('output/file.fits')

# Create array of periods to search
period = np.linspace(1,20, 10000)
# Create a BLSPeriodogram
bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500)

# Searching for the biggest transit
planet_x_period = bls.period_at_max_power
planet_x_t0 = bls.transit_time_at_max_power
planet_x_dur = bls.duration_at_max_power

# Check the value for period
print("Check the value for period",planet_x_period)

# Create a BLS model using the BLS parameters
planet_x_model = bls.get_transit_model(period=planet_x_period,
                                       transit_time=planet_x_t0,
                                       duration=planet_x_dur)

ax = lc.fold(planet_x_period, planet_x_t0).scatter()
planet_x_model.fold(planet_x_period, planet_x_t0).plot(ax=ax, c='r', lw=2)
ax.set_xlim(-5, 5)
plt.savefig('output/period_found_{:.2f}.png'.format(planet_x_period))
