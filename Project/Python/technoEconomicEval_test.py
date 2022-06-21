import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib import cm
import matplotlib.ticker as ticker
import dataset as ds
import elechydro as eh
import plots as plots

# %%
if __name__ == "__main__":
    nominal_power = 605  # Nominal capacity of wind farm [MW]
    scaleUpVal = 3*10**3
    getData = ds.Dataset(nominal_power, "../Dataset/windturbine/Kriegers_Flak.csv",
                         "../Dataset/spot_price/elspotprices.csv", "../Dataset/demand/electricitybalancenonv.csv")
    power = getData.getPower(2019, 1)
    demand = getData.getDemand()
    price_dataset = getData.getPrice()

    scaled_power = getData.scalePower(power, scaleUpVal)
    #scaled_demand, scaled_power = getData.scalePowerAndDemand_old(demand, power)
    # print(scaled_demand*.8*12)
    # print(scaled_power*12)

    #plt.plot(range(8670), power)
    # plt.show()

    P_elec = 6
    E_loss = 0
    time_interval = 8760
    HydrogenPrice = 8  # https://www.fchobservatory.eu/observatory/technology-and-market/levelised-cost-of-hydrogen-green-hydrogen-costs

    MinimumSpotPrice = list(range(0, 500, 30))
    LCOH_g = list(range(0, 10, 1))

    # Create object for hydro or elec driven class
    ElecHydro_obj = eh.ElecHydro(E_loss=E_loss, P_elec=P_elec, power_dataset=scaled_power,
                                  price_dataset=price_dataset, scaleVal = scaleUpVal)

    ### Plots ###
    plots_obj = plots.Plots(ElecHydro_obj=ElecHydro_obj, time_interval=time_interval, MinimumSpotPrice=MinimumSpotPrice, granularity_3d=30, granularity_2d=20)

    # Plot of profit as a function of hydro selling price.
    #plots_obj.profit_hydroPrice(Electro_Capacity = 0, startPrice = 4, endPrice = 13, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1)
    # Plot of profit as a function of electrolyzer capacity.
    #plots_obj.profit_elecCap(SellingPrice=6, startCap=0, endCap=12, years=5, capex=1000, yearly_opex=0.02, Hourly_OPEX=1)

    # Plot 3D plot of profit as a function of hydro selling price and Electrolyzer capacity.
   # plots_obj.profit_hydroPrice_elecCap(startPrice = 0, endPrice = 8,  startCap = 0, endCap = 15, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1)

  #  print(ElecHydro_obj.hydrogen_production(6))

    # 2D plot of peak shaving profit as a function of electrolyzer capacity.
    #plots_obj.profit_PeakShaving_2d(SellingPrice = 2, startCap = 0, endCap = 3*10**3, years = 20, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1)

    # 3d Plot of peak shaving profit as a function of electrolyzer capacity.
    #plots_obj.profit_PeakShaving_3d(startPrice = 0, endPrice = 8, startCap = 0, endCap = 3*10**3, years = 20, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1)

    # Comparison of peak shaving profit as a function of electrolyzer capacity.
    for i in range(2,10,2):
        plots_obj.profit_PeakShaving_2d_comparison(SellingPrice = 8, startCap = 0, endCap = 3*10**3, years = 20, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1)
    #plots_obj.profit_PeakShaving_3d_comparison(startSellingPrice = 2, stopSellingPrice = 10, startCap = 0, endCap = 16, years = 5, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1)
    #############