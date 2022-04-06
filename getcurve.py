import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

#missao=input("Qual é a Missão? ")
#setor=input("Qual é o setor? ")
#target_id = input("Nos dê o seu TargetID: ")
#search_result = lk.search_lightcurve(target_id, mission=missao, sector=setor)
search_result = lk.search_lightcurve('TIC 251848941', mission='TESS', sector=2)

lc = search_result.download(quality_bitmask='default')
lc = lc.remove_nans().remove_outliers()
lc.scatter()
lc.to_fits(path='output/file.fits', overwrite=True)

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