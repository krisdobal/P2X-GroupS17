'''
Created on: 20220519

Author: Yi Zheng, Department of Electrical Engineering, DTU

'''

from wind_turbine import wind_turbine
import pandas as pd
import matplotlib.pyplot as plt

# Read historical wind speed data
meteorological_data = pd.read_csv('./Historical_data.csv', index_col = 'time')
wind_speed_all = meteorological_data['WS10m']
wind_speed = wind_speed_all['20160101:0011':'20161231:2311']
print(len(wind_speed))

# Instantiate a wind turbine object
wt = wind_turbine(height=50, V_ci=3, V_co=22.5, r=75, capital_cost=1311, V_r=14.32, C_p=0.15)
wt_power = [13 * wt.wt_ac_output(v_wind= i) for i in wind_speed] # MW
print(wt.rated_power())

#1. Assume that the project life is 15 years, calculate the cash flow of every year
# (Assume the hydrogen price is 3€/kg and the yearly wind power remains the same).

#2. Based on the cash flow you got from (1), calculate the NPV (discount rate is 0.05).

#3. Calculate the LCOE of wind power.

#4. Calculate the LCOH (discount rate is 0.05).

