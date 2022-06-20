# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 09:54:11 2022

@author: s152955
"""
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d
import numpy as np

class Plots:
    
    def __init__(self, ElecHydro_obj, time_interval, MinimumSpotPrice):
        self.ElecHydro_obj = ElecHydro_obj
        self.MinimumSpotPrice = MinimumSpotPrice
        self.time_interval = time_interval
        pass
    
    def stepPlot(self):
        #%%
            
        income_sum_E = [None]*len(self.MinimumSpotPrice)
        income_sum_H = [None]*len(self.MinimumSpotPrice)
        income_sum_rest = [None]*len(self.MinimumSpotPrice)
        income_sum_Hydro = [None]*len(self.MinimumSpotPrice)
        income_sum_SpotPriceDriven = [None]*len(self.MinimumSpotPrice)
        utilization_hours = [None]*len(self.MinimumSpotPrice)
        
        for i,price in enumerate(self.MinimumSpotPrice):
            income_sum_E[i], income_sum_H[i], utilization_hours[i], income_sum_rest[i] = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven(price, self.time_interval, self.HydrogenPrice)
            income_sum_SpotPriceDriven[i] = income_sum_E[i] + income_sum_H[i] + income_sum_rest[i];
            
            income_sum_Hydro[i] = self.ElecHydro_obj.technoEcoEval_Hydro(self.time_interval, self.HydrogenPrice) 
            
            #print(f"Spot price: {price:.2f} [EUR/MWh] - Income in given period: {income_sum_SpotPriceDriven[i] / (10**6):.2f} [Mil. EUR] / Utilization factor {utilization_hours[i]/time_interval*100:.2f} [%]" )
            
        #plt.step(MinimumSpotPrice, np.multiply(income_sum_E,10**(-6.0)))
        #plt.step(MinimumSpotPrice, np.multiply(income_sum_H,10**(-6.0)))
        #plt.step(MinimumSpotPrice, np.multiply(income_sum_rest,10**(-6.0)))
        plt.plot(self.MinimumSpotPrice, np.multiply(income_sum_Hydro,10**(-6.0)))
        plt.plot(self.MinimumSpotPrice, np.multiply(income_sum_SpotPriceDriven, 10**(-6.0)))
        #plt.step(MinimumSpotPrice, np.multiply( np.add(np.add(income_sum_E,income_sum_H), income_sum_rest),10**(-6.0)))
        #plt.legend(["Electricity","Hydrogen", "Rest", "Hydro", "Total"])
        plt.legend(["Hydro driven", "Spot price driven"])
        plt.xlabel("Minimum spot price [EUR/MWh]")
        plt.ylabel("[Mil. EUR]")
        plt.grid()
        plt.show()
    
    #%%    
#    OptimalSpotPrice = [None]*len(LCOH_g)
#    EE = [None]*len(LCOH_g)
#    
#    for i,LCOH in enumerate(LCOH_g):
#        OptimalSpotPrice[i], EE[i] = ElecHydro_obj.technoEcoEval_FindMaximumProfit(LCOH,time_interval)
#    
#    
#    plt.plot(LCOH_g, np.multiply(EE,  10**(-6.0)))
#
#   # plt.legend(["Hydro driven"])
#    plt.xlabel("Hydrogen selling price [EUR/kg]")
#    plt.ylabel("[Mil. EUR]")
#    plt.grid()
#    plt.show()
    #price_dataset[price_dataset>600]

#%%
#    P_elec = list(range(0,10,1))
#    #x = np.array([[1, 2, 3], [4, 5, 6]], np.int32)
#    
#    income_sum_E = np.ndarray(shape=(len(LCOH_g),len(P_elec)))
#    income_sum_H  = np.ndarray(shape=(len(LCOH_g),len(P_elec)))    
#    income_sum_rest = np.ndarray(shape=(len(LCOH_g),len(P_elec)))
#    income_sum_Hydro = np.ndarray(shape=(len(LCOH_g),len(P_elec)))
#    income_sum_SpotPriceDriven = np.ndarray(shape=(len(LCOH_g),len(P_elec)))
#    utilization_hours = np.ndarray(shape=(len(LCOH_g),len(P_elec)))
#    
#    
#    for i,HydrogenPrice in enumerate(LCOH_g):
#        for j,P_elechej in enumerate(P_elec):
#            income_sum_E[i,j], income_sum_H[i,j], utilization_hours[i,j], income_sum_rest[i,j] = ElecHydro_obj.technoEcoEval_SpotPriceDriven_priceComparison(time_interval, HydrogenPrice, P_elechej)
#            income_sum_SpotPriceDriven[i,j] = income_sum_E[i,j] + income_sum_H[i,j] + income_sum_rest[i,j];
#    
#    
#        #income_sum_Hydro[i] = ElecHydro_obj.technoEcoEval_Hydro(time_interval, HydrogenPrice) 
#        
        #print(f"Spot price: {price:.2f} [EUR/MWh] - Income in given period: {income_sum_SpotPriceDriven[i] / (10**6):.2f} [Mil. EUR] / Utilization factor {utilization_hours[i]/time_interval*100:.2f} [%]" )
#%%        
    #plt.step(MinimumSpotPrice, np.multiply(income_sum_E,10**(-6.0)))
    #plt.step(MinimumSpotPrice, np.multiply(income_sum_H,10**(-6.0)))
    #plt.step(MinimumSpotPrice, np.multiply(income_sum_rest,10**(-6.0)))
    #plt.plot(MinimumSpotPrice, np.multiply(income_sum_Hydro,10**(-6.0)))
    #plt.plot(MinimumSpotPrice, np.multiply(income_sum_SpotPriceDriven, 10**(-6.0)))
    #plt.plot(LCOH_g, np.multiply( np.add(np.add(income_sum_E,income_sum_H), income_sum_rest),10**(-6.0)))
    #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # Make data.
    # def f(HydrogenPrice, P_elechej):
    #    income_sum_E, income_sum_H, utilization_hours, income_sum_rest = ElecHydro_obj.technoEcoEval_SpotPriceDriven_priceComparison(time_interval, HydrogenPrice, P_elechej)
    #    return income_sum_E + income_sum_H + income_sum_rest
   
    # HydrogenPrice = np.linspace(0, 4, 11)
    # P_elechej = np.linspace(0, 4, 11)
    
    # #Z = [[None] * len(P_elechej) for i in range(0,len(P_elechej)) ]
    # HYDROGENPRICE, P_ELECHEJ = np.meshgrid(HydrogenPrice, P_elechej)
    
    # Z =  np.zeros([len(HydrogenPrice), len(P_elechej)])
    
    # for x, Hyrdro in enumerate(HydrogenPrice):
    #     for y, Pelec in enumerate(P_elechej):
    #         Z[x, y] =   f(Hyrdro, Pelec)  
    # #Z = f(HYDROGENPRICE, P_ELECHEJ)
    
    # fig = plt.figure()
    
    # ax = plt.axes(projection='3d')
    # ax.contour3D(HYDROGENPRICE, P_ELECHEJ,  np.multiply(Z, 10**(-6.0)), 50)
    # ax.set_xlabel('Hydrogen price [EUR/kg]')
    # ax.set_ylabel('Electrolyzer capacity [MW]')
    # ax.set_zlabel('Profit [Mil. EUR]')
    # ax.set_title('3D contour')
    # plt.show()
    
    
    
    
    
 #%% Plot of profit as a function of electrolyzer capacity.  
    
    def profit_elecCap(self, SellingPrice = 8, startCap = 0, endCap = 16, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1):
        Electro_Capacity = list(range(startCap,endCap,200))
        Profit = [None]*len(Electro_Capacity)
        utilization_hours = [None]*len(Electro_Capacity)
        full = [None]*len(Electro_Capacity) 
        notfull = [None]*len(Electro_Capacity)
        
        for i,Capacity in enumerate(Electro_Capacity):
            Profit[i], utilization_hours[i], full[i], notfull[i] = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_capex_opex(self.time_interval, SellingPrice, Capacity, years, capex, yearly_opex, Hourly_OPEX)
         
         
        plt.plot(Electro_Capacity, np.multiply(Profit,  10**(-6.0)))
         
        # plt.legend(["Hydro driven"])
        plt.xlabel("Electrolyzer capacity [MW]")
        plt.ylabel("[Mil. EUR]")
        plt.grid()
        plt.title('Hydro selling price %0.2f [EUR/kg]' %SellingPrice)
        plt.show()   
  
  #%% Plot of profit as a function of hydro selling price.  
         
    def profit_hydroPrice(self, Electro_Capacity = 0, startPrice = 4, endPrice = 13, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1):
        SellingPrice=list(range(startPrice,endPrice,1))
        #Electro_Capacity is [MW]
        Profit = [None]*len(SellingPrice)
        utilization_hours = [None]*len(SellingPrice)
        full = [None]*len(SellingPrice) 
        notfull = [None]*len(SellingPrice) 
        
        
        for i,Price in enumerate(SellingPrice):
            Profit[i], utilization_hours[i], full[i], notfull[i] = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_capex_opex(self.time_interval, Price, Electro_Capacity, years, capex, yearly_opex, Hourly_OPEX)
         
         
        plt.plot(SellingPrice, np.multiply(Profit,  10**(-6.0)))
         
         # plt.legend(["Hydro driven"])
        plt.xlabel("Hydro selling price [EUR/kg]")
        plt.ylabel("[Mil. EUR]")
        plt.grid()
        plt.title('Electrolyzer capacity %0.2f [MW]' %Electro_Capacity)
        plt.show()      
    
 #%%  Plot 3D plot of profit as a function of hydro selling price and Electrolyzer capacity.
    def profit_hydroPrice_elecCap(self, startPrice = 0, endPrice = 8,  startCap = 0, endCap = 15, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1):
           
        #Z = [[None] * len(P_elechej) for i in range(0,len(P_elechej)) ]
        HydrogenPrice = np.linspace(startPrice, endPrice, 10)
        P_elechej=np.linspace(startCap, endCap, 10)
        HYDROGENPRICE, P_ELECHEJ = np.meshgrid(HydrogenPrice, P_elechej)
        
        
        
           
        Z =  np.zeros([len(HydrogenPrice), len(P_elechej)])
        Z2 =  np.zeros([len(HydrogenPrice), len(P_elechej)])
           
        
        for x, Hyrdro in enumerate(HydrogenPrice):
            for y, Pelec in enumerate(P_elechej):
                income_sum_E, utilization_hours, _ ,_ = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_capex_opex(self.time_interval, Hyrdro, Pelec, years, capex, yearly_opex, Hourly_OPEX) ;
                Z[y, x] = income_sum_E  * 10**(-6.0)
                Z2[y, x] = utilization_hours  / self.time_interval * 100;
        
         #Z = f(HYDROGENPRICE, P_ELECHEJ)
        
        fig = plt.figure(figsize=(5 ,5) , dpi=100)
           
        ax = plt.axes(projection='3d')
        mappable = plt.cm.ScalarMappable()
        mappable.set_array(Z)
        #ax.plot_surface(HYDROGENPRICE, P_ELECHEJ,  np.multiply(Z, 10**(-6.0)), cmap=cm.hsv, linewidth=0, antialiased=False)
        ax.plot_surface(HYDROGENPRICE, P_ELECHEJ,  Z, cmap=mappable.cmap, linewidth=0, antialiased=False, norm=mappable.norm,)
        #contourf
        clb=plt.colorbar(mappable)
        clb.ax.tick_params(labelsize=8) 
         #clb.ax.set_title('Your Label',fontsize=8)
        clb.set_label('Profit [Mil. EUR]')
        fig.tight_layout()
        
        plt.margins(x=0 ,y=0)
        #plt.colorbar(mappable)
         #ax.contour3D(HYDROGENPRICE, P_ELECHEJ,  np.multiply(Z, 1/time_interval), 50)
        ax.set_xlabel('Selling hydro price [EUR/kg]')
        ax.set_ylabel('Electrolyzer capacity [MW]')
         #ax.set_zlabel('')
         #ax.set_title('Profit [Mil. EUR]')
        plt.show()
        
        fig = plt.figure(2 ,figsize=(5 ,5) , dpi=100)
           
        ax = plt.axes(projection='3d')
        mappable = plt.cm.ScalarMappable()
        mappable.set_array(Z2)
        #ax.plot_surface(HYDROGENPRICE, P_ELECHEJ,  np.multiply(Z, 10**(-6.0)), cmap=cm.hsv, linewidth=0, antialiased=False)
        ax.plot_surface(HYDROGENPRICE, P_ELECHEJ,  Z2, cmap=mappable.cmap, linewidth=0, antialiased=False, norm=mappable.norm,)
         #contourf
        clb=plt.colorbar(mappable)
        clb.ax.tick_params(labelsize=8) 
         #clb.ax.set_title('Your Label',fontsize=8)
        clb.set_label('Electrolyzer utilization percentage')
        fig.tight_layout()
        
        plt.margins(x=0 ,y=0)
         #plt.colorbar(mappable)
         #ax.contour3D(HYDROGENPRICE, P_ELECHEJ,  np.multiply(Z, 1/time_interval), 50)
        ax.set_xlabel('Selling hydro price [EUR/kg]')
        ax.set_ylabel('Electrolyzer capacity [MW]')
         #ax.set_zlabel('')
         #ax.set_title('Profit [Mil. EUR]')
        plt.show()   