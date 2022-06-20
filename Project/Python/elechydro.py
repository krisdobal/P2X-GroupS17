# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 09:40:01 2022

@author: s152955
"""
class ElecHydro:
    def __init__(self, E_loss, P_elec, power_dataset, demand_dataset, price_dataset):
        self.E_loss = E_loss
        self.P_elec = P_elec
        self.power_dataset = power_dataset
        self.demand_dataset = demand_dataset
        self.price_dataset = price_dataset
        self.dt = 1 # 1 hour interval
        #self.LCOH = LCOH #[EUR/kg] https://www.fchobservatory.eu/observatory/technology-and-market/levelised-cost-of-hydrogen-green-hydrogen-costs

    def technoEcoEval_CalculateDeliveredPower(self, SendingPower,dt):
        # The energy loss at the conversion station  
        eta_st = 1/100;
        
        # The number of the substation
        N_HVDC_st = 2;
        
        # Energy loss per km
        eta_HS = 0.0035 / 100;
        
        # The distance from the hub to the shore [km].
        L_HS = 100
        
        # Sending energy [MJ].
        SendingEnergy = (SendingPower/dt) 
        
        # loss energy [MJ].
        Loss = SendingEnergy * (eta_st * N_HVDC_st + eta_HS * L_HS);
        
        return (SendingEnergy - Loss)* dt
        
    # This function 
    def technoEcoEval_SpotPriceDriven_PeakShaving(self, timeInterval, HydrogenPrice, P_elec_capacity, years, capex, yearly_opex, Hourly_OPEX, Mode = 0):
        #Hourly_OPEX [EUR/Hour per electrolyzer capacity]
        
        income_sum_E = 0

        HHV = 33.3/1000 # MWh/kg
        eta = .66 #[]
        
        if (Mode == 0):
            PriceH2E = HydrogenPrice*eta/HHV #[EUR/MWh]
        elif (Mode == 2):
            PriceH2E = 0;
        else:
            PriceH2E = 10**6;
            
        utilization_electrolyzer_hours = 0
       # full = 0
       # notfull = 0;
        Hourly_OPEX_sum = 0; #[EUR]
        Electrolyzer_cap = 0;
        Electricity_cap = 0;

        # Power threshold of peak shaving [MW].
        PeakPowerThreshold = 12 - P_elec_capacity;
        
        
        # Run through the entiry year.
        for i in range(timeInterval):
           
            
            # If spot price is larger than the energy price of hydrogen:
            # ELECTRICITY DRIVEN
            if(self.price_dataset[i] >= PriceH2E):
               # Electricity_cap = self.power_dataset[i]
               # Electrolyzer_cap = 0;
                
               # If the actual wind farm production is below the power threshold.
                if (self.power_dataset[i] <= PeakPowerThreshold):
                        
                    Electricity_cap = self.power_dataset[i]
                    Electrolyzer_cap = 0
                    
 
                    
                else:
                    Electricity_cap = PeakPowerThreshold
                    Electrolyzer_cap = self.power_dataset[i] - PeakPowerThreshold;
                    
                    if(Electrolyzer_cap > 0):
                        Hourly_OPEX_sum += Hourly_OPEX * Electrolyzer_cap / P_elec_capacity;
                
            # If spot price is below than the energy price of hydrogen.   
            # HYDROGEN DRIVEN
            else:
                
                if (self.power_dataset[i] > 0):
                    utilization_electrolyzer_hours += 1
                
                if (self.power_dataset[i] > P_elec_capacity):
                    #income_sum_E += self.hydrogen_production(P_elec_capacity, P_elec_capacity)*HydrogenPrice*1000
                    Electricity_cap = self.power_dataset[i] - P_elec_capacity
                    Electrolyzer_cap = P_elec_capacity;
                    
                    if(self.power_dataset[i] > 0):
                    #    full += 1;
                        
                        if(P_elec_capacity > 0):
                            Hourly_OPEX_sum += Hourly_OPEX;
                        
                    #income_sum_E += (self.power_dataset[i] - P_elec_capacity) * self.price_dataset[i]
                else:
                   # income_sum_E += self.hydrogen_production(self.power_dataset[i], P_elec_capacity)*HydrogenPrice*1000
                    Electricity_cap = 0
                    Electrolyzer_cap = self.power_dataset[i];
                    
                    if(self.power_dataset[i] > 0):
                    #    notfull += 1;
                        
                        if(P_elec_capacity > 0):
                            Hourly_OPEX_sum += Hourly_OPEX * self.power_dataset[i] / P_elec_capacity;
            
            
            Electricity_cap = self.technoEcoEval_CalculateDeliveredPower(Electricity_cap, self.dt)
            income_sum_E += (Electricity_cap) * self.price_dataset[i]
            income_sum_E += self.hydrogen_production(Electrolyzer_cap, P_elec_capacity)*1000*HydrogenPrice
                       #      
        CAPEX = (P_elec_capacity * capex * 1000);     
        OPEX_Yearly = CAPEX * yearly_opex
        

#        print(P_elec_capacity)
#        print(OPEX_Yearly)
#        print(Hourly_OPEX_sum)
#        print(CAPEX)
#        print(income_sum_E)
#        print("")
        return years*(income_sum_E - OPEX_Yearly - Hourly_OPEX_sum) - CAPEX, utilization_electrolyzer_hours
    
    # This function 
    def technoEcoEval_SpotPriceDriven_capex_opex(self, timeInterval, HydrogenPrice, P_elec_capacity, years, capex, yearly_opex, Hourly_OPEX):
        #Hourly_OPEX [EUR/Hour per electrolyzer capacity]
        
        income_sum_E = 0

        HHV = 33.3/1000 # MWh/kg
        eta = .66 #[]
        PriceH2E = HydrogenPrice*eta/HHV #[EUR/MWh]
        utilization_electrolyzer_hours = 0
        full = 0
        notfull = 0;
        Hourly_OPEX_sum = 0; #[EUR]
        
        
       # if (P_elechej >= 12):
        #    P_elechej = 12;
            
        # Run through the entiry year.
        for i in range(timeInterval):
            
            if(self.price_dataset[i] >= PriceH2E):
                income_sum_E += self.price_dataset[i]*self.power_dataset[i]
            else:
                
                if (self.power_dataset[i] > 0):
                    utilization_electrolyzer_hours += 1
                
                if (self.power_dataset[i] > P_elec_capacity):
                    h2_production_percent = self.hydrogen_production(P_elec_capacity, P_elec_capacity)
                    OPEX = self.calc_OPEX(capex,h2_production_percent)
                    income_sum_E += h2_production_percent*HydrogenPrice*1000
                    Hourly_OPEX = OPEX/365/24
                    
                    if(self.power_dataset[i] > 0):
                        full += 1;
                        
                        if(P_elec_capacity > 0):
                            Hourly_OPEX_sum += Hourly_OPEX;
                        
                    income_sum_E += (self.power_dataset[i] - P_elec_capacity) * self.price_dataset[i]
                else:
                    h2_production_percent = self.hydrogen_production(P_elec_capacity, P_elec_capacity)
                    OPEX = self.calc_OPEX(capex,h2_production_percent)
                    income_sum_E += h2_production_percent*HydrogenPrice*1000
                    Hourly_OPEX = OPEX/365/24
                    
                    if(self.power_dataset[i] > 0):
                        notfull += 1;
                        
                        if(P_elec_capacity > 0):
                            Hourly_OPEX_sum += Hourly_OPEX * self.power_dataset[i] / P_elec_capacity;
               #      
        CAPEX = (P_elec_capacity * capex * 1000);     
        OPEX_Yearly = CAPEX * yearly_opex
#        print(P_elec_capacity)
#        print(OPEX_Yearly)
#        print(Hourly_OPEX_sum)
#        print(CAPEX)
#        print(income_sum_E)
#        print("")
        #print(utilization_electrolyzer_hours)
        return years*(income_sum_E - OPEX_Yearly - Hourly_OPEX_sum) - CAPEX, utilization_electrolyzer_hours,full, notfull

    
    # This function 
    def technoEcoEval_SpotPriceDriven_priceComparison(self, timeInterval, HydrogenPrice,P_elechej):
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
                    income_sum_H += self.hydrogen_production(P_elechej, P_elechej)*HydrogenPrice*1000
                    income_sum_rest += (self.power_dataset[i] - P_elechej) * self.price_dataset[i]
                else:
                    income_sum_H += self.hydrogen_production(self.power_dataset[i], P_elechej)*HydrogenPrice*1000
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
                        income_sum += self.hydrogen_production(self.P_elec, self.P_elec)*HydrogenPrice*1000
                        income_sum += (self.power_dataset[i] - self.P_elec) *  self.price_dataset[i]
                        
                      #pass
                    else:
                        income_sum += self.hydrogen_production(self.power_dataset[i], self.P_elec)*HydrogenPrice*1000

                        
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
                    income_sum_H += self.hydrogen_production(self.P_elec, self.P_elec)*HydrogenPrice*1000
                    income_sum_rest += (self.power_dataset[i] - self.P_elec) *  self.price_dataset[i]
                    
                  #pass
                else:
                    income_sum_H += self.hydrogen_production(self.power_dataset[i],self.P_elec)*HydrogenPrice*1000
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
                    income_sum_H += self.hydrogen_production(self.P_elec, self.P_elec)*HydrogenPrice*1000 + ((self.power_dataset[i] - self.P_elec) *  self.price_dataset[i])
            else:
                    income_sum_H += self.hydrogen_production(self.power_dataset[i], self.P_elec)*HydrogenPrice*1000
                    #pass
        return income_sum_H
    

    
         
    # This function determines the hydrogen production in unit ton.
    def hydrogen_production(self, P_ptx, hydroCap):
        # E_ptx [MWh]        
        h2_production = 0
        
        if(hydroCap > 0):
            p_input = P_ptx/hydroCap;
        else:
            p_input = 0

       
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
        
        ff = p * hydroCap * (2771.36 / 12)
        
        # H2 production [ton]
        h2_production = ff * 0.089/1000
            
        return h2_production
    

#    def calc_OPEX(self, capex, P_elec, installation_frac, os):
#        utilization_electrolyzer_hours = 10000
#       # utilization_electrolyzer_hours 
#        OPEX_tot = capex*(1-installation_frac*(1+os))*0.0344*(P_elec*10**3)**-0.155
#        SF_sr = 1-(1-SF_sr0)*exp(-P_elec/P_stackmax)
#        RC_sr = RU_sr * RC_elec * (1-installation_frac)*(RP_sr/RP_elec)*SF_elec
#        
#        OPEX_tot +=  P_elec*RC_sr*(P_elec*10**3/RP_sr)*SF_sr*OH/OH_max
#        
#        OPEX_tot += capex*0.04*installation_frac*(1+os)
#        OPEX_tot += 
        
    def calc_OPEX(self, CAPEX, h2_production_ton):
        h2_production_ton = h2_production_ton / 0.089 * 1000
        OPEX = 0.02 * CAPEX + h2_production_ton*9*1
        #print(OPEX)
        return OPEX
    
