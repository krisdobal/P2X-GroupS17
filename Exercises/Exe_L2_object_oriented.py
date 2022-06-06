'''
Created on: 20220519

Author: Yi Zheng, Department of Wind and Energy Systems, DTU

'''
import math
import matplotlib.pyplot as plt
import numpy as np

p_0 = 101325
R = 8.314
F = 96485


class alkaline_ele():
    def __init__(self, T=363.15, p=30, A=0.37):
        '''
        Initialize an alkaline electrolyser

        :param T: Temperature (K)
        :param p: Pressure (bar)
        :param A: Cell area (m2)
        '''
        self.T = T
        self.p = p * p_0
        self.A = A

    # -----------These two functions calculate the reversible voltage. You don't have to understand them--------
    def E_rev(self, p_H2O=10 ** (-0.645) * p_0):
        '''
        Reversible potential
        '''
        E_rev = self.E_rev_0() + R * self.T / (2 * F) * math.log((self.p - p_H2O) ** 1.5 / (p_H2O))
        return E_rev

    def E_rev_0(self):
        '''
        Standard reversible potential
        Reference : Low-temperature electrolysis system modelling: A review
        '''
        E_0_T = 1.5184 - 1.5421e-3 * self.T + 9.523e-5 * self.T * math.log(self.T) + 9.84e-8 * self.T ** 2
        return E_0_T

    # -----------------------------------------------------------------------------------------------------------

    def E_cell_empirical(self,
                         r1=8.05e-5,  # ohm m2
                         r2=-2.5e-7,  # ohm m2/celcius
                         s=0.19,  # V
                         t1=1.002,  # A-1 m2
                         t2=8.424,  # A-1 m2 celcius
                         t3=247.3,  # A-1 m2 celcius **2
                         i=1000  # Current density
                         ):
        """
        An empirical model from Ulleberg

        :param r1: Electrolyte ohmic resistive parameter
        :param r2: Electrolyte ohmic resistive parameter
        :param s: over voltage parameter of electrode
        :param t1: empirical over voltage parameter of electrode
        :param t2: empirical over voltage parameter of electrode
        :param t3: empirical over voltage parameter of electrode
        :param i: current density
        :return: cell voltage
        """
        self.i = i  # This could be unnecessary
        assert (t1 + t2 / (self.T - 273.15) + t3 / (self.T - 273.15) ** 2) * self.i + 1 > 0, \
            'The term within Log function should be positive'
        U = self.E_rev() + (r1 + r2 * (self.T - 273.15)) * self.i + s * math.log(
            (t1 + t2 / (self.T - 273.15) + t3 / (self.T - 273.15) ** 2) * self.i + 1, 10)
        return U

    def Faraday_eff(self, i=1000, f1=200, f2=0.94):
        pass

    def hydrogen_production(self, i=1000):
        pass

    def power(self, i=1000):
        pass

    def DC_efficiency(self, i=1000):
        pass

    def Voltage_eff(self, i=1000):
        pass

if __name__ == '__main__':
    # Add new methods in the alkaline_ele class that return different efficiencies or write your own codes.
    # Define an alkaline electrolyser
    my_ael = alkaline_ele(A = 0.25)
    i_range = np.linspace(500, 5000, 20)
    I_range = i_range * my_ael.A

    # 1. Voltage vs current
    Voltage = []
    for current_density in i_range:
        Voltage.append(my_ael.E_cell_empirical(i=current_density))
    plt.plot(I_range, Voltage, label='Voltage')
    plt.ylabel('Voltage(V)')
    plt.xlabel('Current(A)')
    plt.legend()
    plt.show()


