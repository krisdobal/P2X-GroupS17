'''
Created on: 20220519

Author: Yi Zheng, Department of Electrical Engineering, DTU

'''

from wind_turbine import wind_turbine
import pandas as pd
from Exe_L3_1 import hydrogen_production
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

P2X_rated_power = 12#MW
windturbines = 13
#1. Assume that the project life is 15 years, calculate the cash flow of every year
# (Assume the hydrogen price is 3€/kg and the yearly wind power remains the same).
CAPEX = wt.rated_power()*10**3*wt.capital_cost * windturbines + P2X_rated_power * 1000*10**3 #€
print(CAPEX)
OPEX = .02*CAPEX# €/year,
Revenue = 1474 * 10**3 * 3 #  Ton/year * kg/ton * €/kg = €/year
print(OPEX)
print(Revenue)
CashFlow = [-CAPEX]
for i in range(1,15+1):
    CashFlow.append(Revenue-OPEX)
print(Revenue-OPEX)
print(CashFlow)
print(sum(CashFlow))

#2. Based on the cash flow you got from (1), calculate the NPV (discount rate is 0.05).
DiscountRate = 0.05
NPV = 0
for i in range(15+1):
    NPV += CashFlow[i]/((1+DiscountRate)**i)
print("NPV", NPV)

#3. Calculate the LCOE of wind power.
CAPEX = wt.rated_power()*10**3*wt.capital_cost*windturbines
OPEX = .02*CAPEX# €/year,
CashFlow = [CAPEX]
for n in range(1,15+1):
    CashFlow.append(OPEX)
cost = 0
for n in range(15+1):
    cost += CashFlow[n]/((1+DiscountRate)**n)

ElecDiscoutned =0
for n in range(1,15+1):
    ElecDiscoutned += sum(wt_power) / ((1+DiscountRate)**n)
wt_LCOE = cost / ElecDiscoutned
print("LCOE of wt=",wt_LCOE,"€/MWh")
print("accumulated Electrical Production discoutned", ElecDiscoutned, "MWh")
print(CAPEX)
print(cost)

#4. Calculate the LCOH (discount rate is 0.05).
CAPEX = wt.rated_power()*10**3*wt.capital_cost * windturbines + P2X_rated_power * 1000*10**3 #€
OPEX = .02*CAPEX# €/year,
cost = 0
CashFlow = [CAPEX]
for i in range(1,15+1):
    CashFlow.append(OPEX)
for i in range(15+1):
    cost += CashFlow[i]/((1+DiscountRate)**i)

HydrogenDiscoutned =0
for i in range(1,15+1):
    HydrogenDiscoutned += hydrogen_production(ele_capacity=12) / ((1+DiscountRate)**i)
H2_LCOE = cost / HydrogenDiscoutned
print("LCOE of Hydrogen production=",H2_LCOE/10**3,"€/kg")

