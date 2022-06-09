"""
Created on Tue May 17 15:02:33 2022
@author: zhe chen

# In Python you need to 'import' packages and external functions before you can 
# use them. We can import NumPy (which enables us to work with matrices, among 
# other things) by writing 'import numpy as np'. 
# We load the package into the ``namespace'' np to reference it easily,
# now we can write 'np.sum(X)' instead of 'numpy.sum(X)'.

Besides Python, this file defines the exercise, including run a simulation of power flow.

So far there are:
    - Simple network power flow and impact of network parameters.
    - Power flow time series simulation.
    - P2X data in network model.

"""
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
# Generate data for network model.
import os
import pandapower.networks as pn
import pandapower.plotting as plot
import pandapower as pp
colors = ["b", "g", "r", "c", "y", "m", "k", "w"] #Define colors for later use
PF = 0.92 #Power factor: related to P and Q
#%% Ex 1
#Define 2 Bus network, it is a pandas structure.
net = pp.create_empty_network() 

pp.create_std_type(net, {"r_ohm_per_km": 0.126, "x_ohm_per_km":0.116,
                "c_nf_per_km": 0, "max_i_ka": 0.14,
                "endtemp_degree": 70.0}, name="240AL",element = "line")

#Define 2 Bus with rate voltage in kV 
b0 = pp.create_bus(net, vn_kv=10.5, name="Bus 0")
b1 = pp.create_bus(net, vn_kv=10.5, name="Bus 1")

#Assign bus 0 as reference, per unit of voltage always 1
pp.create_ext_grid(net, bus=b0, vm_pu=1, name="Grid Connection")

#Assign a line connect bus 0 and bus 1     
pp.create_line(net, from_bus=b0, to_bus=b1, length_km=2, name="Line 0-1",std_type="240AL")
#Define Load Power and assign to bus 1.
Load_b1 = pp.create_load(net, bus=b1, p_mw=0, q_mvar=0, name="Load_b1")

#Change the load consumption
p_tmp = 9 #Consumption is positive
q_tmp = 8
net.load.p_mw = p_tmp
net.load.q_mvar = q_tmp

#Run power flow
pp.runpp(net) #it is very trival

#Check results and try to interprete them.
print("Bus volatge:",net.res_bus)
print("Line current:",net.res_line)

#Impact of network model, change the network data and conclude the impact of 
#voltage and line current
net.load.p_mw = 10
net.load.q_mvar = 8
pp.runpp(net) #test 1

net.line.length_km = 4
net.line.r_ohm_per_km = 0.15
net.line.x_ohm_per_km = 0.2
pp.runpp(net) 
#Plot the new result

#%% Ex 2
#If we have a time-series load data, how to calculate time-series voltages.

#Generate time series data. Let's have a 24 hourly data point.
p_time = np.random.rand(24)*6
q_time = np.random.rand(24)*1

v_fullpp = np.zeros([len(net.bus),24]) #Recod time series bus result
l_fullpp = np.zeros([len(net.line),24])#Recod time series line result

# 24 points, each point run power flow once
for i in range(24):
    net.load.p_mw = p_time[i]
    net.load.q_mw = q_time[i]

    pp.runpp(net) #Run a point.
    
    #Recording
    v_fullpp[:,i] = net.res_bus.vm_pu.to_numpy()
    l_fullpp[:,i] = net.res_line.loading_percent.to_numpy()

#Check v_fullpp and l_fullpp and plot them

#%% Ex 3
#We consider a synthetic network and use P2X data as loads.
#20kv, medium voltage, 6 buses system with P2X and consumption
#Simulation covers 24 hourly points.
net = pn.simple_mv_open_ring_net()

#Try to get more familiar with net model
bus = net.bus
line = net.line
trafo = net.trafo
load = net.load
#Plot the network
plot.simple_plot(net, show_plot=True)

#Read Power to X data
p_time = np.random.rand(24,5)*6
q_time = np.random.rand(24,5)*1

df_h = pd.read_excel('P2Xloads.xlsx') #Hydrogen P power
P_h  = df_h.P_load.to_numpy()
Q_h = P_h * np.sqrt(1 - PF * PF) / PF #Hydrogen Q power

#You can add P2X load to any existing load, here load 1.
add_ind = 1
p_time[:,add_ind] = p_time[:,add_ind] + P_h
q_time[:,add_ind] = q_time[:,add_ind] + Q_h

# # run load flow
v_fullpp = np.zeros([len(net.bus),24]) #Recod time series bus result
l_fullpp = np.zeros([len(net.line),24])#Recod time series line result
trafo_load = np.zeros(24)              #Recod time series in transformer result

for i in range(24):
    for j in range(len(net.load)):#if multiple buses, assign load to each bus.
        net.load.p_mw[j] = p_time[i,j]
        net.load.q_mvar[j] = q_time[i,j]

    pp.runpp(net)
    v_fullpp[:,i] = net.res_bus.vm_pu.to_numpy()
    l_fullpp[:,i] = net.res_line.loading_percent.to_numpy()
    trafo_load[i] = net.res_trafo.loading_percent.to_numpy()
    print("Running at hour:",i)


#Check v_fullpp and l_fullpp and plot them


print('Done')