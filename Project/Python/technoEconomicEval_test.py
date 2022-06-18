import pandas as pd
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib import cm 
import matplotlib.ticker as ticker   
#####################
### Dataset class ###
#####################

class Dataset:
    def __init__(self, nominal_power, dataset_power_name, dataset_price_name, dataset_demand_name):
        
        # load power dataset
        self.nominal_power = nominal_power
        self.dataset_power_name = dataset_power_name
        
        # Load price dataset
        self.dataset_price_name = dataset_price_name
        
        # Load demand dataset #
        self.dataset_demand_name = dataset_demand_name
        
        
    def loadDataset(self, filename, column_name):
        self.filename = filename
        self.column_name = column_name  
        self.df = pd.read_csv(self.filename)
        column_data = (self.df[self.column_name])
        
        return column_data
    
    
    def getDemand(self):
        priceArea_data=self.loadDataset(self.dataset_demand_name,"PriceArea")
        TotalLoad_data=self.loadDataset(self.dataset_demand_name,"TotalLoad")
        
        TotalLoad_data_DK2 = []
        for i,area in enumerate(priceArea_data):
            if(area == "DK2"):
                TotalLoad_data_DK2.append(TotalLoad_data[i])
                
        return TotalLoad_data_DK2
                
        
    def scalePowerAndDemand(self, demandList, powerList):
        maxValue_demand = max(demandList)

        demandList_scaled = np.divide(demandList,maxValue_demand)*12*.08
        powerList_scaled = np.divide(powerList,self.nominal_power)*12
        
        return demandList_scaled, powerList_scaled
        
    def getPower(self, year_start, year_forward):
        # Gets power data from a selected year (e.g. 1980) and x years forward (e.g. 1)
        HOURSINYEAR = 8760
        power_data = self.loadDataset(self.dataset_power_name, "Power")
    
        total_power_hours = len(power_data) # Number of hours "Power" spans
        hours_power_list = list(range(0, total_power_hours, 1)) # List of all hours "Power" spans
        year_start_mapped = year_start-1980
        hours_out = hours_power_list[year_start_mapped*HOURSINYEAR:year_start_mapped*HOURSINYEAR+year_forward*HOURSINYEAR]
        self.power = []
        for i in hours_out:
            self.power.append(power_data[i])
        
        return self.power
    
    def getPrice(self):        
        price_data = self.loadDataset(self.dataset_price_name, "SpotPriceEUR")
        return price_data
    
    def getPowerFactor(self):
        return sum(power)/(self.nominal_power*self.HOURSINYEAR)

#####################
#####################
#####################
    


#########################################
### Calculate hydro or electro output ###
#########################################
        
class ElecHydro:
    def __init__(self, E_loss, P_elec, power_dataset, demand_dataset, price_dataset):
        self.E_loss = E_loss
        self.P_elec = P_elec
        self.power_dataset = power_dataset
        self.demand_dataset = demand_dataset
        self.price_dataset = price_dataset
        self.dt = 1 # 1 hour interval
        #self.LCOH = LCOH #[EUR/kg] https://www.fchobservatory.eu/observatory/technology-and-market/levelised-cost-of-hydrogen-green-hydrogen-costs
 
    # This function 
    def technoEcoEval_SpotPriceDriven33(self, timeInterval, HydrogenPrice, P_elechej):
        income_sum_E = 0

        HHV = 33.3/1000 # MWh/kg
        eta = .66 #[]
        PriceH2E = HydrogenPrice*eta/HHV
        utilization_electrolyzer_hours = 0
        full = 0
        notfull = 0;
        
        for i in range(timeInterval):
            
            if(self.price_dataset[i] >= PriceH2E):
                #if(self)
                income_sum_E += self.price_dataset[i]*self.power_dataset[i]
            else:
                
                if (self.power_dataset[i] > 0):
                    utilization_electrolyzer_hours += 1
                
                if (self.power_dataset[i] > P_elechej):
                    income_sum_E += self.hydrogen_production(P_elechej)*HydrogenPrice*1000
                    if(self.power_dataset[i] > 0):
                        full += 1;
                    income_sum_E += (self.power_dataset[i] - P_elechej) * self.price_dataset[i]
                else:
                    income_sum_E += self.hydrogen_production(self.power_dataset[i])*HydrogenPrice*1000
                    if(self.power_dataset[i] > 0):
                        notfull += 1;
               #      
        return income_sum_E - (P_elechej * 1000 * 1000) , utilization_electrolyzer_hours,full, notfull
       
    
    # This function 
    def technoEcoEval_SpotPriceDriven2(self, timeInterval, HydrogenPrice,P_elechej):
        income_sum_E = 0
        income_sum_H = 0
        income_sum_rest = 0
        HHV = 33.3/1000 # MWh/kg
        eta = .66 #[]
        PriceH2E = HydrogenPrice*eta/HHV
        utilization_electrolyzer_hours = 0
        
        for i in range(timeInterval):
            
            if(self.price_dataset[i] >= PriceH2E):
                #if(self)
                income_sum_E += self.price_dataset[i]*self.power_dataset[i]
            else:
                
                if (self.power_dataset[i] > 0):
                    utilization_electrolyzer_hours += 1
                
                if (self.power_dataset[i] > P_elechej):
                    income_sum_H += self.hydrogen_production(P_elechej)*HydrogenPrice*1000
                    income_sum_rest += (self.power_dataset[i] - P_elechej) * self.price_dataset[i]
                else:
                    income_sum_H += self.hydrogen_production(self.power_dataset[i])*HydrogenPrice*1000
        return income_sum_E, income_sum_H, utilization_electrolyzer_hours,  income_sum_rest
    

    
    # This function finds the maximum profil for a given hydrogen selling price.
    def technoEcoEval_FindMaximumProfit(self, HydrogenPrice, timeInterval):
        income_sum = 0
        
        utilization_electrolyzer_hours = 0
        
        income_sum_temp = 0;
        MinimumSpotPrice = 0;  
        
        #
        while MinimumSpotPrice in range(0,500,5):
            
            for i in range(timeInterval):
                
                if(self.price_dataset[i] >= MinimumSpotPrice):
                    #if(self)
                    income_sum += self.price_dataset[i]*self.power_dataset[i]
                else:
                    
                   # if (self.power_dataset[i] > 0):
                    #    utilization_electrolyzer_hours += 1
                    
                    if (self.power_dataset[i] > self.P_elec):
                        income_sum += self.hydrogen_production(self.P_elec)*HydrogenPrice*1000
                        income_sum += (self.power_dataset[i] - self.P_elec) *  self.price_dataset[i]
                        
                      #pass
                    else:
                        income_sum += self.hydrogen_production(self.power_dataset[i])*HydrogenPrice*1000

                        
            if (income_sum < income_sum_temp):
                break
            else:
                income_sum_temp = income_sum;
                income_sum = 0;
                
            MinimumSpotPrice += 5;
            
        return MinimumSpotPrice, income_sum

       
    # This function determines the profit of spot price-driven electrolyzer.
    # If the spot price is below the specified minimum spot price, the total production
    # from the the wind farm is selled on the energy market. 
    # Conversely, the electrolyzer is activated, and any excess energy from the
    # wind farm is selled on the energy market.
    def technoEcoEval_SpotPriceDriven(self, MinimumSpotPrice, timeInterval, HydrogenPrice):
        income_sum_E = 0
        income_sum_H = 0
        income_sum_rest = 0
        
        utilization_electrolyzer_hours = 0
        
        for i in range(timeInterval):
            
            if(self.price_dataset[i] >= MinimumSpotPrice):
                #if(self)
                income_sum_E += self.price_dataset[i]*self.power_dataset[i]
            else:
                
                if (self.power_dataset[i] > 0):
                    utilization_electrolyzer_hours += 1
                
                if (self.power_dataset[i] > self.P_elec):
                    income_sum_H += self.hydrogen_production(self.P_elec)*HydrogenPrice*1000
                    income_sum_rest += (self.power_dataset[i] - self.P_elec) *  self.price_dataset[i]
                    
                  #pass
                else:
                    income_sum_H += self.hydrogen_production(self.power_dataset[i])*HydrogenPrice*1000
                    #pass
        return income_sum_E, income_sum_H, utilization_electrolyzer_hours,  income_sum_rest
    
    # This function determines the profit of hydro-driven electrolyzer. 
    # The remeaning power from the wind farm is selled on the energy market.
    # The electrolyzer is activated, and any excess energy from the
    # wind farm is selled on the energy market.
    def technoEcoEval_Hydro(self, timeInterval, HydrogenPrice):
        income_sum_H = 0
        utilization_electrolyzer_hours = 0;
        
        #utilization_hours = 0
        for i in range(timeInterval):
            
            if (self.power_dataset[i] > 0):
                    utilization_electrolyzer_hours += 1
            
            if (self.power_dataset[i] > self.P_elec and self.power_dataset[i] > 0):
                    income_sum_H += self.hydrogen_production(self.P_elec)*HydrogenPrice*1000 + ((self.power_dataset[i] - self.P_elec) *  self.price_dataset[i])
            else:
                    income_sum_H += self.hydrogen_production(self.power_dataset[i])*HydrogenPrice*1000
                    #pass
        return income_sum_H
    

    
         
    # This function determines the hydrogen production in unit ton.
    def hydrogen_production(self, P_ptx):
        # E_ptx [MWh]        
        h2_production = 0

        p_input = P_ptx/self.P_elec;

       
        if p_input > 0.468 and p_input <= 1:
            # [Nm^3/h]
            y1 = 1385.68 / 2771.36;
            y2 = 2771.36 / 2771.36;
            
            x1 = 0.468;
            x2 = 1;
        elif p_input > 0.222 and p_input <= 0.468:
            # [Nm^3/h]
            y1 = 692.84 / 2771.36;
            y2 = 1385.68 / 2771.36;
            
            # [MW]
            x1 = 0.222;
            x2 = 0.468;
        else: 
            x1 = 0;
            x2 = 0.222;
            y1 = 0;
            y2 = 692.84 / 2771.36;
            
        # Slope.    
        a = (y2 - y1) / (x2 - x1)
        
        b = (-a*x2) + y2
        
 
        # H2 production rate as a function of power [Nm^3/h].
        p = (a * p_input) + b    
        
        ff = p * self.P_elec * (2771.36 / 12)
        
        # H2 production [ton]
        h2_production = ff * 0.089/1000
            
        return h2_production
    
    
    
#########################################
#########################################
#########################################

#%%
if __name__ == "__main__":
    nominal_power = 630 # Nominal capacity of wind farm [MW]
    getData = Dataset(nominal_power, "../Dataset/windturbine/London_Array.csv", "../Dataset/spot_price/elspotprices.csv", "../Dataset/demand/electricitybalancenonv.csv")
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
    ElecHydro_obj = ElecHydro(E_loss = E_loss, P_elec = P_elec, power_dataset = scaled_power, \
                              demand_dataset = scaled_demand, price_dataset = price_dataset)
  #  print(ElecHydro_obj.hydrogen_production(6))
    
  #%%
        
#    income_sum_E = [None]*len(MinimumSpotPrice)
#    income_sum_H = [None]*len(MinimumSpotPrice)
#    income_sum_rest = [None]*len(MinimumSpotPrice)
#    income_sum_Hydro = [None]*len(MinimumSpotPrice)
#    income_sum_SpotPriceDriven = [None]*len(MinimumSpotPrice)
#    utilization_hours = [None]*len(MinimumSpotPrice)
#    
#    for i,price in enumerate(MinimumSpotPrice):
#        income_sum_E[i], income_sum_H[i], utilization_hours[i], income_sum_rest[i] = ElecHydro_obj.technoEcoEval_SpotPriceDriven(price,time_interval, HydrogenPrice)
#        income_sum_SpotPriceDriven[i] = income_sum_E[i] + income_sum_H[i] + income_sum_rest[i];
#        
#        income_sum_Hydro[i] = ElecHydro_obj.technoEcoEval_Hydro(time_interval, HydrogenPrice) 
#        
#        #print(f"Spot price: {price:.2f} [EUR/MWh] - Income in given period: {income_sum_SpotPriceDriven[i] / (10**6):.2f} [Mil. EUR] / Utilization factor {utilization_hours[i]/time_interval*100:.2f} [%]" )
#        
#    #plt.step(MinimumSpotPrice, np.multiply(income_sum_E,10**(-6.0)))
#    #plt.step(MinimumSpotPrice, np.multiply(income_sum_H,10**(-6.0)))
#    #plt.step(MinimumSpotPrice, np.multiply(income_sum_rest,10**(-6.0)))
#    plt.plot(MinimumSpotPrice, np.multiply(income_sum_Hydro,10**(-6.0)))
#    plt.plot(MinimumSpotPrice, np.multiply(income_sum_SpotPriceDriven, 10**(-6.0)))
#    #plt.step(MinimumSpotPrice, np.multiply( np.add(np.add(income_sum_E,income_sum_H), income_sum_rest),10**(-6.0)))
#    #plt.legend(["Electricity","Hydrogen", "Rest", "Hydro", "Total"])
#    plt.legend(["Hydro driven", "Spot price driven"])
#    plt.xlabel("Minimum spot price [EUR/MWh]")
#    plt.ylabel("[Mil. EUR]")
#    plt.grid()
#    plt.show()
#    
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
#            income_sum_E[i,j], income_sum_H[i,j], utilization_hours[i,j], income_sum_rest[i,j] = ElecHydro_obj.technoEcoEval_SpotPriceDriven2(time_interval, HydrogenPrice, P_elechej)
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
    #    income_sum_E, income_sum_H, utilization_hours, income_sum_rest = ElecHydro_obj.technoEcoEval_SpotPriceDriven2(time_interval, HydrogenPrice, P_elechej)
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
    
    
    
    
    
 #%% Plot of profit as a function of wind farm capacity.  
    

    # Electro_Capacity = list(range(0,16,1))
    # Profit = [None]*len(Electro_Capacity)
    # utilization_hours = [None]*len(Electro_Capacity)
    # full = [None]*len(Electro_Capacity) 
    # notfull = [None]*len(Electro_Capacity) 
    # SellingPrice = 30 # [EUR/kg]
    
    # for i,Capacity in enumerate(Electro_Capacity):
    #     Profit[i], utilization_hours[i], full[i], notfull[i] = ElecHydro_obj.technoEcoEval_SpotPriceDriven33(time_interval, SellingPrice, Capacity)
     
     
    # plt.plot(Electro_Capacity, np.multiply(Profit,  10**(-6.0)))
     
    # # plt.legend(["Hydro driven"])
    # plt.xlabel("Electrolyzer capacity [MW]")
    # plt.ylabel("[Mil. EUR]")
    # plt.grid()
    # plt.title('Hydro selling price %0.2f [EUR/kg]' %SellingPrice)
    # plt.show()   
  
  #%% Plot of profit as a function of hydro selling price.  
     

    # SellingPrice = list(range(0,13,1)) #[EUR/kg]
    # Profit = [None]*len(SellingPrice)
    # utilization_hours = [None]*len(SellingPrice)
    # full = [None]*len(SellingPrice) 
    # notfull = [None]*len(SellingPrice) 
    # Electro_Capacity = 15 # [MW]
    
    # for i,Price in enumerate(SellingPrice):
    #     Profit[i], utilization_hours[i], full[i], notfull[i] = ElecHydro_obj.technoEcoEval_SpotPriceDriven33(time_interval, Price, Electro_Capacity)
     
     
    # plt.plot(SellingPrice, np.multiply(Profit,  10**(-6.0)))
     
    # # plt.legend(["Hydro driven"])
    # plt.xlabel("Hydro selling price [EUR/kg]")
    # plt.ylabel("[Mil. EUR]")
    # plt.grid()
    # plt.title('Electrolyzer capacity %0.2f [MW]' %Electro_Capacity)
    # plt.show()      
    
 # #%%  Plot 3D plot of profit as a function of hydro selling price and Electrolyzer capacity.

    def f(HydrogenPrice, P_elechej):
        income_sum_E, utilization_hours, full, notfull = ElecHydro_obj.technoEcoEval_SpotPriceDriven33(time_interval, HydrogenPrice, P_elechej)
    
        return income_sum_E, utilization_hours
  
    HydrogenPrice = np.linspace(0, 10, 10)
    P_elechej = np.linspace(0, 15, 10)
   
    #Z = [[None] * len(P_elechej) for i in range(0,len(P_elechej)) ]
    HYDROGENPRICE, P_ELECHEJ = np.meshgrid(HydrogenPrice, P_elechej)
   
    Z =  np.zeros([len(HydrogenPrice), len(P_elechej)])
    Z2 =  np.zeros([len(HydrogenPrice), len(P_elechej)])
   

    for x, Hyrdro in enumerate(HydrogenPrice):
        for y, Pelec in enumerate(P_elechej):
            income_sum_E, utilization_hours = f(Hyrdro, Pelec) ;
            Z[y, x] = income_sum_E  * 10**(-6.0)
            Z2[y, x] = utilization_hours  / time_interval * 100;
            
    #Z = f(HYDROGENPRICE, P_ELECHEJ)

    fig = plt.figure(1 ,figsize=(5 ,5) , dpi=100)
   
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
       