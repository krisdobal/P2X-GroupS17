import pandas as pd
import matplotlib.pyplot as plt 


filename = "../Dataset/Kriegers_Flak.csv"
column_name = "Power"

df = pd.read_csv(filename)
column = df['Power']

hours = range(0, len(column), 1)


#print(column[-1:])
power = []
for i in column:
    #print(column)
    power.append(column)
    
plt.plot(hours, power)
#print(column[i])
plt.show()