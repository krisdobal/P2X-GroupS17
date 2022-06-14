import pandas as pd
import matplotlib.pyplot as plt 
   
#####################
### Dataset class ###
#####################

class Dataset:
    def __init__(self, nominal_power, dataset_name):
        self.nominal_power = nominal_power
        self.dataset_name = dataset_name
        self.column_name = "Power"

        self.df = pd.read_csv(self.dataset_name)
        self.column_data = self.df[self.column_name]
        self.totalHours = len(self.column_data)
        self.hoursList = list(range(0, self.totalHours, 1))
        
        self.HOURSINYEAR = 8670
        
    def getPower(self, year_start, year_forward):
        #pass
        #hours = range(, 8760, 1)
        year_start_mapped = year_start-1980
        hours_out = self.hoursList[year_start_mapped*self.HOURSINYEAR:year_start_mapped*self.HOURSINYEAR+year_forward*self.HOURSINYEAR]
        self.power = []
        for i in hours_out:
            self.power.append(self.column_data[i])
        
        return self.power
    
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
        self.dt = 1
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

#########################################
#########################################
#########################################


 
if __name__ == "__main__":
    nominal_power = 630
    getData = Dataset(nominal_power,"../Dataset/windturbine/London_Array.csv")
    power = getData.getPower(2015, 1)
    plt.plot(range(8670), power)
    plt.show()
    
    
    test_ElecHydro = ElecHydro(E_loss= 0, P_elec = 200, P_hub = power)
    time_interval = 200
    B_H = [None]*time_interval
    H_driven_dataset = test_ElecHydro.H_driven(time_interval)
    E_driven_dataset = test_ElecHydro.E_driven(time_interval)
    print(H_driven_dataset)
    print(E_driven_dataset)
    
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
            
            
    plt.step(range(time_interval),B_H)
    plt.show()
    cp=getData.getPowerFactor()
    print(cp)