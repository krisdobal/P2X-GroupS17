'''
Created on: 20220517

Author: Yi Zheng, Department of Electrical Engineering, DTU

'''
from wind_turbine import wind_turbine
import matplotlib.pyplot as plt
import pandas as pd

# Read historical wind speed data
meteorological_data = pd.read_csv('./Historical_data.csv', index_col = 'time')
wind_speed_all = meteorological_data['WS10m']
wind_speed = wind_speed_all['20160101:0011':'20161231:2311']
print(len(wind_speed))

# Instantiate a wind turbine object
wt = wind_turbine(height=50, V_ci=3, V_co=22.5, r=75, capital_cost=1311, V_r=14.32, C_p=0.15)
print(wt.rated_power())
wt_power = [13 * wt.wt_ac_output(v_wind= i) for i in wind_speed] # MW

plt.plot(range(len(wt_power)), wt_power, label = 'Wind power')
plt.ylabel('Wind power (MW)')
plt.xlabel('Time (hour)')
plt.legend()
plt.show()

def hydrogen_production(ele_capacity=12, eff_variation=False):
    if not eff_variation:
        h2_production = 0
        for p in wt_power:
            p_after_converter = 0.96 * p
            if p_after_converter>=ele_capacity:
                h2_production += ele_capacity*1000/4.33 * 0.089/1000 # ton
            else:
                h2_production += p_after_converter*1000/4.33 * 0.089/1000
    else:
        pass
    return h2_production

# 1. Calculate the yearly hydrogen production.
print(hydrogen_production(ele_capacity= 12))

# 2. Recalculate the hydrogen production using an electrolyser model with varing efficiency.

# 3. Change the capacity of the electrolyser and compare the hydrogen production.
