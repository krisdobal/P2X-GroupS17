# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 09:54:11 2022

@author: s152955
"""
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d
import matplotlib.ticker as plticker
import numpy as np

class Plots:
    
    def __init__(self, ElecHydro_obj, time_interval, MinimumSpotPrice, granularity_3d, granularity_2d):
        self.granularity_3d = granularity_3d
        self.granularity_2d = granularity_2d
        self.ElecHydro_obj = ElecHydro_obj
        self.MinimumSpotPrice = MinimumSpotPrice
        self.time_interval = time_interval
    
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
    
    def LCOE_and_LCOH_vs_elecCap(self, SellingPrices = [], startCap = 0, endCap = 16, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1):
        
        Electro_Capacity = (np.linspace(startCap,endCap,self.granularity_2d))
        factor = 1000
        #Profit = [None]*len(Electro_Capacity)
        
        LCOH_acrossPrice = [None]*len(SellingPrices)
        LCOE_acrossPrice = [None]*len(SellingPrices)
        LCOH = [None]*len(Electro_Capacity) 
        LCOE = [None]*len(Electro_Capacity)
        
        
        for j,SellingPrice in enumerate(SellingPrices):
            for i,Capacity in enumerate(Electro_Capacity):
                _, _, LCOH[i], LCOE[i] = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_PeakShaving(self.time_interval, SellingPrice, Capacity, years, capex, yearly_opex, Hourly_OPEX, Mode = 0)
            
            LCOH_acrossPrice[j] = LCOH[1:]
            LCOE_acrossPrice[j] = LCOE[1:]
            
        Electro_Capacity=np.divide(Electro_Capacity,factor)
        fig = plt.figure(figsize=(5,5), dpi=200)
        for LCOH_val in LCOH_acrossPrice:
            plt.plot(Electro_Capacity[1:], LCOH_val)
            
        fig.tight_layout()
        plt.xlabel("Electrolyzer capacity [GW]")
        plt.ylabel("[EUR/kg]")
        plt.tick_params(labelsize=6)
        #plt.margins(x=0,y=0)
        #plt.title(f"sellingPrice: {SellingPrice}")
        plt.legend([f"Selling price: {SellingPrices[0]}",f"Selling price: {SellingPrices[1]}",f"Selling price: {SellingPrices[2]}",f"Selling price: {SellingPrices[3]}"],fontsize=8)
        plt.grid()
        plt.savefig(f"./plots/LCOE_and_LCOH_vs_elecCap/elec_capVSLCOH_SellingPrice.eps")
        plt.savefig(f"./plots/LCOE_and_LCOH_vs_elecCap_png/elec_capVSLCOH_SellingPrice.png")
        
        
        fig = plt.figure(figsize=(5,5), dpi=200)
        for LCOE_val in LCOE_acrossPrice:
            plt.plot(Electro_Capacity[1:], LCOE_val)
            
        fig.tight_layout()
        plt.xlabel("Electrolyzer capacity [GW]")
        plt.ylabel("[EUR/MWh]")
        plt.ylim((40,100))
        plt.xlim((0,2.9))
        plt.tick_params(labelsize=6)
        #plt.margins(x=0,y=0)
        #plt.title(f"sellingPrice: {SellingPrice}")
        plt.legend([f"Selling price: {SellingPrices[0]}",f"Selling price: {SellingPrices[1]}",f"Selling price: {SellingPrices[2]}",f"Selling price: {SellingPrices[3]}"],fontsize=8)
        plt.grid()
        plt.savefig(f"./plots/LCOE_and_LCOH_vs_elecCap/elec_capVSLCOE_SellingPrice.eps")
        plt.savefig(f"./plots/LCOE_and_LCOH_vs_elecCap_png/elec_capVSLCOE_SellingPrice.png")
        plt.show()
            
 #%% Comparison of peak shaving profit as a function of electrolyzer capacity. 
    
    def profit_PeakShaving_3d_comparison(self, startSellingPrice = 2, stopSellingPrice = 10, startCap = 0, endCap = 16, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1):
        sellingPrice = (np.linspace(startSellingPrice, stopSellingPrice, self.granularity_3d))
        Electro_Capacity = (np.linspace(startCap,endCap,self.granularity_3d))
        Profit = [None]*len(Electro_Capacity)
        utilization_hours = [None]*len(Electro_Capacity)
        #full = [None]*len(Electro_Capacity) 
        #notfull = [None]*len(Electro_Capacity)
        
        for i,Capacity in enumerate(Electro_Capacity):
            Profit[i], utilization_hours[i], _, _ = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_PeakShaving(self.time_interval, sellingPrice[i], Capacity, years, capex, yearly_opex, Hourly_OPEX, Mode = 0)
        ''' 
        plt.plot(Electro_Capacity, np.multiply(Profit,  10**(-6.0)))
        
        for i,Capacity in enumerate(Electro_Capacity):
            Profit[i], utilization_hours[i] = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_PeakShaving(self.time_interval, SellingPrice, Capacity, years, capex, yearly_opex, Hourly_OPEX, Mode = 1)
         
        plt.plot(Electro_Capacity, np.multiply(Profit,  10**(-6.0)))     
        
        for i,Capacity in enumerate(Electro_Capacity):
            Profit[i], utilization_hours[i] = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_PeakShaving(self.time_interval, SellingPrice, Capacity, years, capex, yearly_opex, Hourly_OPEX, Mode = 2)
         
        plt.plot(Electro_Capacity, np.multiply(Profit,  10**(-6.0)))      
        '''       
        
        fig = plt.figure()

        #ax = fig.add_subplot(111, projection='3d')
        
        #ax.plot(Electro_Capacity, np.multiply(Profit,  10**(-6.0)), sellingPrice)
        
        
        
        
        ax = plt.axes(projection='3d')
        mappable = plt.cm.ScalarMappable()
        #mappable.set_array(Z)
        #ax.plot_surface(HYDROGENPRICE, P_ELECHEJ,  np.multiply(Z, 10**(-6.0)), cmap=cm.hsv, linewidth=0, antialiased=False)
        ax.plot_surface(Electro_Capacity, np.multiply(Profit,  10**(-6.0)), [sellingPrice,sellingPrice], cmap=mappable.cmap, linewidth=0, antialiased=False, norm=mappable.norm,)
        #contourf
        clb=plt.colorbar(mappable)
        clb.ax.tick_params(labelsize=8) 
        clb.ax.orientation('vertical')
         #clb.ax.set_title('Your Label',fontsize=8)
        clb.set_label('Profit [Mil. EUR]')
        fig.tight_layout()
        
        plt.margins(x=0 ,y=0)
        #plt.colorbar(mappable)
         #ax.contour3D(HYDROGENPRICE, P_ELECHEJ,  np.multiply(Z, 1/time_interval), 50)
        ax.set_xlabel('Electrolyzer Capacity [MW]')
        ax.set_ylabel('Profit [Mil. EUR]')
        ax.set_zlabel('Hydrogen selling price [EUR/Kg')
        ax.set_title('Hydro selling price %0.2f [EUR/kg] on peak shaving' %sellingPrice[0])
        plt.show()
        
        #plt.show()
        
        #plt.legend(["Spot-price driven", "Hydrogen driven", "Electricity driven"])
        #plt.xlabel("Electrolyzer capacity [MW]")
        #plt.ylabel("[Mil. EUR]")
      

 #%% Comparison of peak shaving profit as a function of electrolyzer capacity. 
    
    def profit_PeakShaving_2d_comparison(self, SellingPrice = 8, startCap = 0, endCap = 16, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1):
        Electro_Capacity = list(np.linspace(startCap,endCap,self.granularity_2d))
        Profit0 = [None]*len(Electro_Capacity)
        Profit1 = [None]*len(Electro_Capacity)
        Profit2 = [None]*len(Electro_Capacity)
        utilization_hours = [None]*len(Electro_Capacity)
        #full = [None]*len(Electro_Capacity) 
        #notfull = [None]*len(Electro_Capacity)
        factor = 1000
        fig = plt.figure(figsize=(5,5), dpi=200)
        ax = plt.axes()
        
        maxVal = 15500/10**(-6.0)
        minVal = 1000/10**(-6.0)   

        for i,Capacity in enumerate(Electro_Capacity):
            Profit0[i], utilization_hours[i], _, _  = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_PeakShaving(self.time_interval, SellingPrice, Capacity, years, capex, yearly_opex, Hourly_OPEX, Mode = 1)
         
#        #if(np.max(Profit0)>maxVal):
#        maxVal = np.max(Profit0)
#        #if(np.min(Profit0)<minVal):
#        minVal = np.min(Profit0)
#            
        for i,Capacity in enumerate(Electro_Capacity):
            Profit1[i], utilization_hours[i], _, _ = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_PeakShaving(self.time_interval, SellingPrice, Capacity, years, capex, yearly_opex, Hourly_OPEX, Mode = 2)
        
#        if(np.max(Profit1)>maxVal):
#            maxVal = np.max(Profit1)
#        if(np.min(Profit1)<minVal):
#            minVal = np.min(Profit1)
        
        for i,Capacity in enumerate(Electro_Capacity):
            Profit2[i], utilization_hours[i], _, _ = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_PeakShaving(self.time_interval, SellingPrice, Capacity, years, capex, yearly_opex, Hourly_OPEX, Mode = 0)
        
#        if(np.max(Profit2)>maxVal):
#            maxVal = np.max(Profit2)
#        if(np.min(Profit2)<minVal):
#            minVal = np.min(Profit2)
            
        
        Profit_total = [Profit0,Profit1,Profit2]
        
        for i in Profit_total:
            plt.plot(np.divide(Electro_Capacity,factor), np.multiply(i,  10**(-6.0)))
        fig.tight_layout()
        plt.tick_params(labelsize=8)
        #plt.margins(x=0,y=0)
        plt.xlabel("Electrolyzer capacity [GW]")
        plt.ylabel("NPV revenue [MEUR]")
        plt.legend(["Hydrogen driven", "Electricity driven", "Spot price driven"],fontsize=8)
        plt.grid()
          

            

        
#        plt.yticks(np.linspace(minVal*(1-0.05) * 10**(-6.0), maxVal*(1+0.05)*10**(-6.0), self.granularity_2d))
#        plt.ylim(minVal*(1-0.05) * 10**(-6.0),  maxVal*(1+0.05)*10**(-6.0))
        '''
        plt.yticks(np.linspace(minVal*(1-0.02) * 10**(-6.0), maxVal*(1+0.02)*10**(-6.0), self.granularity_2d))
        plt.ylim(minVal*(1-0.02) * 10**(-6.0),  maxVal*(1+0.02)*10**(-6.0))        
        
        plt.plot(np.divide(Electro_Capacity,factor), np.multiply(Profit1,  10**(-6.0)))
        
        plt.yticks(np.linspace(minVal*(1-0.02) * 10**(-6.0), maxVal*(1+0.02)*10**(-6.0), self.granularity_2d))
        plt.ylim(minVal*(1-0.02) * 10**(-6.0),  maxVal*(1+0.02)*10**(-6.0))        
        
        
        
        plt.plot(np.divide(Electro_Capacity,factor), np.multiply(Profit2,  10**(-6.0)))
    
        plt.yticks(np.linspace(minVal*(1-0.02) * 10**(-6.0), maxVal*(1+0.02)*10**(-6.0), self.granularity_2d))
        plt.ylim(minVal*(1-0.02) * 10**(-6.0),  maxVal*(1+0.02)*10**(-6.0))        
        '''
        
        


        

        
        
        #locx = plticker.MultipleLocator(base=endCap*0.1)
       # locy = plticker.MultipleLocator(base=np.max(np.multiply(Profit,  10**(-6.0)))*0.1)
       # ax.xaxis.set_major_locator(locx)
        #ax.yaxis.set_major_locator(locy)

# Add the grid
#ax.grid(which='major', axis='both', linestyle='-')
       
        #plt.title('Hydro selling price %0.2f [EUR/kg] on peak shaving' %SellingPrice)
        plt.savefig(f"./plots/profit_PeakShaving_2d_comparison/elec_capVSrevenue_hydrogenPrice{SellingPrice}.eps")
        plt.savefig(f"./plots/profit_PeakShaving_2d_comparison_png/elec_capVSrevenue_hydrogenPrice{SellingPrice}.png")
        plt.show() 
        
        
 #%% Plot of peak shaving profit as a function of electrolyzer capacity.  
    
    def profit_PeakShaving_2d(self, SellingPrice = 8, startCap = 0, endCap = 16, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1):
        Electro_Capacity = list(np.linspace(startCap,endCap,self.granularity_2d))
        Profit = [None]*len(Electro_Capacity)
        utilization_hours = [None]*len(Electro_Capacity)
        #full = [None]*len(Electro_Capacity) 
        #notfull = [None]*len(Electro_Capacity)
        
        for i,Capacity in enumerate(Electro_Capacity):
            Profit[i], utilization_hours[i], _, _ = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_PeakShaving(self.time_interval, SellingPrice, Capacity, years, capex, yearly_opex, Hourly_OPEX)
         
         
        plt.plot(Electro_Capacity, np.multiply(Profit,  10**(-6.0)))
         
        # plt.legend(["Hydro driven"])
        plt.xlabel("Electrolyzer capacity [MW]")
        plt.ylabel("[MEUR]")
        
        locs, labels = plt.yticks()
        #plt.yticks(np.linspace(min(locs), max(locs)+1, self.granularity_2d))
        plt.yticks(np.arange(min(locs), max(locs)+1, 1))
        plt.ylim(min(locs), max(locs))
        
        plt.grid()
        #plt.title('Hydrogen selling price %0.2f [EUR/kg] on peak shaving' %SellingPrice)
        plt.show()       
 #%%  Plot 3D plot of peak shving profit as a function of hydro selling price and Electrolyzer capacity.
    def profit_PeakShaving_3d(self, startPrice = 0, endPrice = 8,  startCap = 0, endCap = 15, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1):
           
        #Z = [[None] * len(P_elechej) for i in range(0,len(P_elechej)) ]
        HydrogenPrice = np.linspace(startPrice, endPrice, self.granularity_3d)
        P_elechej = np.linspace(startCap, endCap, self.granularity_3d)
        HYDROGENPRICE, P_ELECHEJ = np.meshgrid(HydrogenPrice, P_elechej)
              
           
        Z =  np.zeros([len(HydrogenPrice), len(P_elechej)])
        #Z2 =  np.zeros([len(HydrogenPrice), len(P_elechej)])
           
        
        for x, Hyrdro in enumerate(HydrogenPrice):
            for y, Pelec in enumerate(P_elechej):
                income_sum_E, utilization_hours, _, _ = self.ElecHydro_obj.technoEcoEval_SpotPriceDriven_PeakShaving(self.time_interval, Hyrdro, Pelec, years, capex, yearly_opex, Hourly_OPEX) ;
                Z[y, x] = income_sum_E  * 10**(-6.0)
                #Z2[y, x] = utilization_hours  / self.time_interval * 100;
        

        
        fig = plt.figure(figsize=(5 ,5) , dpi=200)
           
        ax = plt.axes(projection='3d')
        mappable = plt.cm.ScalarMappable()
        mappable.set_array(Z)
        #ax.plot_surface(HYDROGENPRICE, P_ELECHEJ,  np.multiply(Z, 10**(-6.0)), cmap=cm.hsv, linewidth=0, antialiased=False)
        ax.plot_surface(HYDROGENPRICE, np.divide(P_ELECHEJ,1000),  Z, cmap=mappable.cmap, linewidth=0, antialiased=False, norm=mappable.norm,)
        #contourf
        clb=plt.colorbar(mappable, orientation='horizontal')
        clb.ax.tick_params(labelsize=8) 
         #clb.ax.set_title('Your Label',fontsize=8)
        clb.set_label('NPV revenue [MEUR]')
        fig.tight_layout()
        
        plt.margins(x=0 ,y=0)
        #plt.colorbar(mappable)
         #ax.contour3D(HYDROGENPRICE, P_ELECHEJ,  np.multiply(Z, 1/time_interval), 50)
        ax.set_xlabel('Hydrogen market price [EUR/kg]')
        ax.set_ylabel('Electrolyzer capacity [GW]')
         #ax.set_zlabel('')
        #ax.set_title('Revenue vs Electrolyzer capacity vs ')
        plt.tick_params(labelsize=8)
        plt.show()
        plt.savefig(f"./plots/profit_PeakShaving_3d/elec_capVSrevenueVShydrogenPrice_3d.eps")
        plt.savefig(f"./plots/profit_PeakShaving_3d_png/elec_capVSrevenueVShydrogenPrice_3d.png")
        '''
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
        ax.set_title('PEAK SHAVING')
        plt.show()       
        '''
 #%% Plot of profit as a function of electrolyzer capacity.  
    
    def profit_elecCap(self, SellingPrice = 8, startCap = 0, endCap = 16, years = 3, capex = 1000, yearly_opex = 0.02, Hourly_OPEX = 1):
        #Electro_Capacity = list(range(startCap,endCap,1))
        Electro_Capacity = list(np.linspace(startCap,endCap,self.granularity_2d))
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
        SellingPrice=list(np.linspace(startPrice,endPrice,self.granularity_2d))
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
        HydrogenPrice = np.linspace(startPrice, endPrice, self.granularity_2d)
        P_elechej=np.linspace(startCap, endCap, self.granularity_2d)
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