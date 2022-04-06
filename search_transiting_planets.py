from ctypes import DEFAULT_MODE
import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np

# Search for Kepler observations of Kepler-69
search_result = lk.search_lightcurve('Kepler-69', author='Kepler', cadence='long')
# Download all available Kepler light curves
lc_collection = search_result.download_all()
#ax=lc_collection.plot()
#print(ax)
plt.style.use('ggplot')
#ax.set_title('Kepler-69 Search Results')
#ax.set_xlabel('Flux')
#ax.set_ylabel('Time')
#ax.plot()
#plt.show()
#print("Resultado da Busca:\n",search_result)
# Flatten the light curve
lc = lc_collection.stitch().flatten(window_length=901).remove_outliers()
#lc.plot()
#plt.show()

# Create array of periods to search
period = np.linspace(1, 20, 10000)
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


# Identifying Additional Transiting Planet Signals in the Same Light Curve
# Create a cadence mask using the BLS parameters
planet_x_mask = bls.get_transit_mask(period=planet_x_period,
                                     transit_time=planet_x_t0,
                                     duration=planet_x_dur)
masked_lc = lc[~planet_x_mask]
ax = masked_lc.scatter()
lc[planet_x_mask].scatter(ax=ax, c='r', label='Masked')
period = np.linspace(1, 6, 10000)
bls = masked_lc.to_periodogram('bls', period=period, frequency_factor=500)
bls.plot()



planet_y_period = bls.period_at_max_power
planet_y_t0 = bls.transit_time_at_max_power
planet_y_dur = bls.duration_at_max_power

# Check the value for period
print("periodo do planeta Y",planet_y_period)

ax = masked_lc.fold(planet_y_period, planet_y_t0).scatter()
masked_lc.fold(planet_y_period, planet_y_t0).bin(.1).plot(ax=ax, c='r', lw=2,
                                                          label='Binned Flux')
ax.set_xlim(-5, 5)


planet_y_model = bls.get_transit_model(period=planet_y_period,
                                       transit_time=planet_y_t0,
                                       duration=planet_y_dur)
ax = lc.scatter()
planet_x_model.plot(ax=ax, c='dodgerblue', label='Planet X Transit Model')
planet_y_model.plot(ax=ax, c='r', label='Planet Y Transit Model')






plt.show()



plt.show()
