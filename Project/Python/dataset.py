# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 09:35:35 2022

@author: s152955
"""
import numpy as np
import pandas as pd

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
        
        powerList_scaled = np.divide(powerList, self.nominal_power)*12
    
        
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