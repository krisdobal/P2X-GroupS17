import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
   
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
    def __init__(self, E_loss, P_elec, power_dataset, demand_dataset, price_dataset, LCOH):
        self.E_loss = E_loss
        self.P_elec = P_elec
        self.power_dataset = power_dataset
        self.demand_dataset = demand_dataset
        self.price_dataset = price_dataset
        self.dt = 1 # 1 hour interval
        self.LCOH = LCOH #[EUR/kg] https://www.fchobservatory.eu/observatory/technology-and-market/levelised-cost-of-hydrogen-green-hydrogen-costs
        
    # This function determines the profit of spot price-driven electrolyzer.
    # If the spot price is below the specified minimum spot price, the total production
    # from the the wind farm is selled on the energy market. 
    # Conversely, the electrolyzer is activated, and any excess energy from the
    # wind farm is selled on the energy market.
    def technoEcoEval(self, MinimumSpotPrice, timeInterval):
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
                    income_sum_H += self.hydrogen_production(self.P_elec)*self.LCOH*1000
                    income_sum_rest += (self.power_dataset[i] - self.P_elec) *  self.price_dataset[i]
                    
                  #pass
                else:
                    income_sum_H += self.hydrogen_production(self.power_dataset[i])*self.LCOH*1000
                    #pass
        return income_sum_E, income_sum_H, utilization_electrolyzer_hours,  income_sum_rest
    
    # This function determines the profit of hydro-driven electrolyzer. 
    # The remeaning power from the wind farm is selled on the energy market.
    # The electrolyzer is activated, and any excess energy from the
    # wind farm is selled on the energy market.
    def technoEcoEval_Hydro(self, timeInterval):
        income_sum_H = 0
        utilization_electrolyzer_hours = 0;
        
        #utilization_hours = 0
        for i in range(timeInterval):
            
            if (self.power_dataset[i] > 0):
                    utilization_electrolyzer_hours += 1
            
            if (self.power_dataset[i] > self.P_elec and self.power_dataset[i] > 0):
                    income_sum_H += self.hydrogen_production(self.P_elec)*self.LCOH*1000 + ((self.power_dataset[i] - self.P_elec) *  self.price_dataset[i])
            else:
                    income_sum_H += self.hydrogen_production(self.power_dataset[i])*self.LCOH*1000
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
    LCOH = 5 #https://www.fchobservatory.eu/observatory/technology-and-market/levelised-cost-of-hydrogen-green-hydrogen-costs
    #MinimumSpotPrice = [10, 20, 25, 30, 35, 40, 45, 50, 60, 70,80, 90, 500]#, 80, 90, 100,300,400, 500
    MinimumSpotPrice = list(range(0,500,10))
    # Create object for hydro or elec driven class
    ElecHydro_obj = ElecHydro(E_loss = E_loss, P_elec = P_elec, power_dataset = scaled_power, \
                              demand_dataset = scaled_demand, price_dataset = price_dataset, LCOH = LCOH)
    #print(ElecHydro_obj.hydrogen_production(6))
    income_sum_E = [None]*len(MinimumSpotPrice)
    income_sum_H = [None]*len(MinimumSpotPrice)
    income_sum_rest = [None]*len(MinimumSpotPrice)
    income_sum_Hydro = [None]*len(MinimumSpotPrice)
    income_sum_SpotPriceDriven = [None]*len(MinimumSpotPrice)
    utilization_hours = [None]*len(MinimumSpotPrice)
    
    for i,price in enumerate(MinimumSpotPrice):
        income_sum_E[i], income_sum_H[i], utilization_hours[i], income_sum_rest[i] = ElecHydro_obj.technoEcoEval(price,time_interval)
        income_sum_SpotPriceDriven[i] = income_sum_E[i] + income_sum_H[i] + income_sum_rest[i];
        
        income_sum_Hydro[i] = ElecHydro_obj.technoEcoEval_Hydro(time_interval) 
        
        #print(f"Spot price: {price:.2f} [EUR/MWh] - Income in given period: {income_sum_SpotPriceDriven[i] / (10**6):.2f} [Mil. EUR] / Utilization factor {utilization_hours[i]/time_interval*100:.2f} [%]" )
        
    #plt.step(MinimumSpotPrice, np.multiply(income_sum_E,10**(-6.0)))
    #plt.step(MinimumSpotPrice, np.multiply(income_sum_H,10**(-6.0)))
    #plt.step(MinimumSpotPrice, np.multiply(income_sum_rest,10**(-6.0)))
    plt.plot(MinimumSpotPrice, np.multiply(income_sum_Hydro,10**(-6.0)))
    plt.plot(MinimumSpotPrice, np.multiply(income_sum_SpotPriceDriven, 10**(-6.0)))
    #plt.step(MinimumSpotPrice, np.multiply( np.add(np.add(income_sum_E,income_sum_H), income_sum_rest),10**(-6.0)))
    #plt.legend(["Electricity","Hydrogen", "Rest", "Hydro", "Total"])
    plt.legend(["Hydro driven", "Spot price driven"])
    plt.xlabel("Minimum spot price [EUR/MWh]")
    plt.ylabel("[Mil. EUR]")
    plt.grid()
    plt.show()
#price_dataset[price_dataset>600]
