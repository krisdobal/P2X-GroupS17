import pandas as pd
import matplotlib.pyplot as plt 


filename = "../Dataset/windturbine/Kriegers_Flak.csv"
column_name = "Power"

df = pd.read_csv(filename)
column = df['Power']

#hours = range(len(column)-8760, len(column), 1)
hours = range(0, 8760, 1)


#print(hours)
#print(column[-1:])
power = []
for i in hours:
    #print(i)
    power.append(column[i])
    
plt.plot(hours, power)
plt.show()


cp=sum(power)/(600*8760)
print(cp)