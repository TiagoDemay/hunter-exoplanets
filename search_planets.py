from ctypes import DEFAULT_MODE
import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image   
search_result = lk.search_lightcurve('TIC 251848941', mission='TESS', sector=2)
lc_collection = search_result.download_all(quality_bitmask='default')
lc = lc_collection[0]


# Create array of periods to search
period = np.linspace(1,20, 10000)
# Create a BLSPeriodogram
bls = lc.to_periodogram(method='bls', period=period, frequency_factor=500)
bls.plot()

# Searching for the biggest transit
planet_x_period = bls.period_at_max_power
planet_x_t0 = bls.transit_time_at_max_power
planet_x_dur = bls.duration_at_max_power

# Check the value for period
print("periodo do planeta X",planet_x_period)

# Create a BLS model using the BLS parameters
planet_x_model = bls.get_transit_model(period=planet_x_period,
                                       transit_time=planet_x_t0,
                                       duration=planet_x_dur)

ax = lc.fold(planet_x_period, planet_x_t0).scatter()
planet_x_model.fold(planet_x_period, planet_x_t0).plot(ax=ax, c='r', lw=2)
ax.set_xlim(-5, 5)



plt.show()