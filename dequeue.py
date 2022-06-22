import json
import os
import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits


site="http://192.168.50.10:8080/memq/server/queues/Lista/dequeue"
resposta = requests.post(site)

missao = 'TESS'
setor = '2'

dados = json.loads(resposta.text)
target_id = dados['body']
print(missao,setor,target_id)
search_result = lk.search_lightcurve(target_id, mission=missao, sector=setor)
lc = search_result.download(quality_bitmask='default')
resposta = requests.post(site)

try:
        lc = lc.remove_nans().remove_outliers()
        lc.scatter()
        filename = "output/%s.fits" % target_id
        lc.to_fits(path=filename, overwrite=True) 
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
        print("=================================NEXT TARGET ===============================>")
except:
        print("PROBLEM WITH TARGET",target_id)

