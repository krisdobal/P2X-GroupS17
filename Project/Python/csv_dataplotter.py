import pandas as pd
import matplotlib.pyplot as plt 
   
    
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
    
    
class test:
    def H_driven(self):
        pass
    
    def E_driven(self):
        pass
 
if __name__ == "__main__":
    nominal_power = 630
    getData = Dataset(nominal_power,"../Dataset/windturbine/London_Array.csv")
    power = getData.getPower(2015, 1)
    plt.plot(range(8670), power)
    plt.show()


    cp=getData.getPowerFactor()
    print(cp)