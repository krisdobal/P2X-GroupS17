import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib import cm 
import matplotlib.ticker as ticker 
import dataset as ds  
import elechydro as eh
import plots as plots

#%%
if __name__ == "__main__":
    nominal_power = 630 # Nominal capacity of wind farm [MW]
    getData = ds.Dataset(nominal_power, "../Dataset/windturbine/London_Array.csv", "../Dataset/spot_price/elspotprices.csv", "../Dataset/demand/electricitybalancenonv.csv")
    power = getData.getPower(2015, 1)
    demand = getData.getDemand()
    price_dataset = getData.getPrice()
    
    scaled_demand, scaled_power = getData.scalePowerAndDemand(demand, power)
    
    #print(scaled_demand*.8*12)
    #print(scaled_power*12)
    
    #plt.plot(range(8670), power)
    #plt.show()
    
    P_elec = 6
    E_loss = 0
    time_interval = 8760
    HydrogenPrice = 8 #https://www.fchobservatory.eu/observatory/technology-and-market/levelised-cost-of-hydrogen-green-hydrogen-costs
 
    
    
    
    
    #MinimumSpotPrice = [10, 20, 25, 30, 35, 40, 45, 50, 60, 70,80, 90, 500]#, 80, 90, 100,300,400, 500
    MinimumSpotPrice = list(range(0,500,30))
    LCOH_g = list(range(0,10,1))
    
    # Create object for hydro or elec driven class
    ElecHydro_obj = eh.ElecHydro(E_loss = E_loss, P_elec = P_elec, power_dataset = scaled_power, \
                              demand_dataset = scaled_demand, price_dataset = price_dataset)
    
    # Plots
    plots_obj = plots.Plots(ElecHydro_obj, time_interval, MinimumSpotPrice)
    
    # Plot of profit as a function of hydro selling price.  
    #plots_obj.profit_hydroPrice(Electro_Capacity = 0, startPrice = 4, endPrice = 13, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1)
    
    # Plot of profit as a function of electrolyzer capacity.  
    plots_obj.profit_elecCap(SellingPrice = 90, startCap = 0, endCap = 20, years = 1, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1)
    
    # Plot 3D plot of profit as a function of hydro selling price and Electrolyzer capacity.
   # plots_obj.profit_hydroPrice_elecCap(startPrice = 0, endPrice = 8,  startCap = 0, endCap = 15, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1)
    
  #  print(ElecHydro_obj.hydrogen_production(6))
    
