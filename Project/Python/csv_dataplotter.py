import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
   
#####################
### Dataset class ###
#####################

class Dataset:
    def __init__(self, nominal_power, dataset_power_name, dataset_price_name, dataset_demand_name):
        
        #################
        # Power dataset #
        #################
        
        # load power dataset
        
        self.nominal_power = nominal_power
        
        self.dataset_power_name = dataset_power_name
        '''
        self.column_power_name = "Power"        
        self.df_power = pd.read_csv(self.dataset_power_name)
        
        # Get column with header "Power"
        self.column_power_data = self.df_power[self.column_power_name] # "Power" data
        self.total_power_hours = len(self.column_power_data) # Number of hours "Power" spans
        self.hours_power_list = list(range(0, self.total_power_hours, 1)) # List of all hours "Power" spans
        '''
        self.HOURSINYEAR = 8670
        
        #################
        # Price dataset #
        #################
        
        # Load price dataset
        
        self.dataset_price_name = dataset_price_name
        '''
        self.column_price_name = "SpotPriceEUR"
        self.df_price = pd.read_csv(self.dataset_price_name)
        
        # Get column with header "SpotPriceEUR"
        self.column_price_data = self.df_price[self.column_price_name] # "SpotPriceEUR" data
        self.total_price_hours = len(self.column_price_data) # Number of hours "SpotPriceEUR" spans
        self.hours_price_list = list(range(0, self.total_price_hours, 1)) # List of all hours  "SpotPriceEUR" spans
        '''
        
        # Load demand dataset #
        self.dataset_demand_name = dataset_demand_name
        
        
        #self.loadDataset(self, self.dataset_power_name, "Power")
        #self.loadDataset(self, self.dataset_price_name, "SpotPriceEUR")
        
    def loadDataset(self, filename, column_name):
        self.filename = filename
        self.column_name = column_name  
        
        self.df = pd.read_csv(self.filename)
        column_data = self.df[self.column_name]
        
        return column_data
    
    
    def getDemand(self):
        priceArea_data=self.loadDataset(self.dataset_demand_name,"PriceArea")
        TotalLoad_data=self.loadDataset(self.dataset_demand_name,"TotalLoad")
        
        for i,area in enumerate(priceArea_data):
            if(area == "DK1"):
                del priceArea_data[i]
                del TotalLoad_data[i]
                
        return TotalLoad_data
                
        
    def scalePowerAndDemand(self, demandList, powerList):
        maxValue_demand = max(demandList)
        maxValue_power = max(powerList)
        
        demandList_scaled = np.divide(demandList,maxValue_demand)
        powerList_scaled = np.divide(powerList,maxValue_power)
        
        return demandList_scaled, powerList_scaled
        
    def getPower(self, year_start, year_forward):
        # Gets power data from a selected year (e.g. 1980) and x years forward (e.g. 1)
        power_data = self.loadDataset(self.dataset_power_name, "Power")
    
        total_power_hours = len(power_data) # Number of hours "Power" spans
        hours_power_list = list(range(0, total_power_hours, 1)) # List of all hours "Power" spans
        year_start_mapped = year_start-1980
        hours_out = hours_power_list[year_start_mapped*self.HOURSINYEAR:year_start_mapped*self.HOURSINYEAR+year_forward*self.HOURSINYEAR]
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
    def __init__(self, E_loss, P_elec, P_hub):
        self.E_loss = E_loss
        self.P_elec = P_elec
        self.P_hub = P_hub
        self.dt = 1 # 1 hour interval
        
        
    def H_driven(self,timeInterval): 
        # dt is [hours]
        # P_elec is [MW]
        self.E_ptx_H_dt = []
        for i in range(timeInterval):
            self.E_ptx_H_dt.append(min(self.P_elec*self.dt,self.P_hub[i]*self.dt-self.E_loss))
            
        return self.E_ptx_H_dt
    
    def E_driven(self, timeInterval):
        # dt is [hours]
        # P_elec is [MW]
        #self.E_hub = self.P_hub*dt
        self.E_ptx_E_dt = []
        for i in range(timeInterval):
            if(self.P_hub[i]*self.dt-self.P_elec*self.dt > 0):            
                self.E_ptx_E_dt.append(self.P_hub[i]*self.dt-self.E_loss-min(self.P_hub[i]*self.dt-self.P_elec*self.dt, self.P_hub[i]*self.dt-self.E_loss))
            else:
                self.E_ptx_E_dt.append(0)
                
        return self.E_ptx_E_dt


    def hydrogen_production(self, E_ptx, eff_variation=True):
        # E_ptx [MWh]        
        h2_production = []
        P_ptx = np.divide(E_ptx, self.dt) # To ensure that E_ptx has correct unit [MW] and renamed to P_ptx 
        for i in P_ptx:
            ele_capacity=i/self.P_elec
            
            if not eff_variation:
                #p_after_converter = 0.96 * p
                    
            #    if p_after_converter>=ele_capacity:
                h2_production.append(ele_capacity*1000/4.33 * 0.089/1000) # ton
                #else:
                    #h2_production += p_after_converter*1000/4.33 * 0.089/1000
                        
            else:            
                # [MW].
                #p_after_converter = 0.96 * p;
                #if p_after_converter >= ele_capacity:
                p_input = i/self.P_elec;
                #else:
                #    p_input = p_after_converter;
                
                if p_input > 0.468 and p_input <= 1:
                    # [Nm^3/h]
                    y1 = 1385.68;
                    y2 = 2771.36;
                    
                    x1 = 0.468;
                    x2 = 1;
                elif p_input > 0.222 and p_input <= 0.468:
                    # [Nm^3/h]
                    y1 = 692.84;
                    y2 = 1385.68;
                    
                    # [MW]
                    x1 = 0.222;
                    x2 = 0.468;
                else: 
                    x1 = 0;
                    x2 = 0.222;
                    y1 = 0;
                    y2 = 692.84;
                    
                # Slope.    
                a = (y2 - y1) / (x2 - x1)
                b = (-a*x2) + y2
                
                # H2 production rate as a function of power [Nm^3/h].
                f = (a * p_input) + b    
                
                # H2 production [ton]
                h2_production.append(f * 0.089/1000)
                    
        return h2_production

#########################################
#########################################
#########################################


if __name__ == "__main__":
    nominal_power = 630
    getData = Dataset(nominal_power, "../Dataset/windturbine/London_Array.csv", "../Dataset/spot_price/elspotprices.csv", "../Dataset/demand/electricitybalancenonv.csv")
    power = getData.getPower(2015, 1)
    demand = getData.getDemand()
    
    scaled_demand, scaled_power = getData.scalePowerAndDemand(demand, power)
    
    #print(scaled_demand*.8*12)
    #print(scaled_power*12)
    
    #plt.plot(range(8670), power)
    #plt.show()
    
    P_elec = 12
    E_loss = 0
    P_hub = power
    time_interval = 10
    LOCH = 4.95 #https://www.fchobservatory.eu/observatory/technology-and-market/levelised-cost-of-hydrogen-green-hydrogen-costs
    
    
    # Create object for hydro or elec driven class
    ElecHydro_obj = ElecHydro(E_loss = E_loss, P_elec = P_elec, P_hub = power)
    B_H = [None]*time_interval # Binary list of preferable drive state
    H_driven_dataset = ElecHydro_obj.H_driven(time_interval)
    E_driven_dataset = ElecHydro_obj.E_driven(time_interval)

    
    # Populate 
    for i in range(time_interval):
        if (H_driven_dataset[i] > E_driven_dataset[i]):
            #print("Hydro driven")
            B_H[i]=1
        elif (H_driven_dataset[i] < E_driven_dataset[i]):
            #print("Electric driven")
            B_H[i]=0
        else:
            #print("Equally profitable")
            B_H[i]=-1
       
    # Get dataset for both H and E driven for a given timesample
    E_driven_H_production = ElecHydro_obj.hydrogen_production([12,12])
    H_driven_H_production = ElecHydro_obj.hydrogen_production([12,12])
    
    
    '''
    for i in range(2):
        print(f"Hour: {i} / E driven H production: {E_driven_H_production[i]} / H driven H production: {H_driven_H_production[i]}")
    
    
    plt.step(range(time_interval),B_H)
    plt.show()
    cp=getData.getPowerFactor()
    print(cp)
    '''