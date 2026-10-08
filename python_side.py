import skfuzzy as fuzz 
from skfuzzy.control import Consequent,Antecedent,Rule,ControlSystem,ControlSystemSimulation
import numpy as np 
import matplotlib.pyplot as plt 

class DimensionFLow:
     def __init__(self):
          self.karar_dict = {
               'yavas' : 1,
               'orta' : 2,
               'hizli' : 3
          }

          min_sicaklik,max_sicaklik,N_sicaklik = 26,29,10   #deneysel olarak değişltirmeniz gereken veriler 
          min_hiz,max_hiz,hiz_adim = 0,100,1

          sicakliklar = np.linspace(min_sicaklik,max_sicaklik,N_sicaklik)
          hizlar = np.arange(min_hiz,max_hiz+hiz_adim,hiz_adim)

          sicakliklar_ = Antecedent(sicakliklar,'temps')
          self.hizlar_ = Consequent(hizlar,'speeds')

          sicakliklar_['dusuk'] = fuzz.trimf(sicakliklar_.universe,[min_sicaklik,min_sicaklik,(min_sicaklik + max_sicaklik) / 2])
          sicakliklar_['ilik'] = fuzz.trimf(sicakliklar_.universe,[min_sicaklik,(min_sicaklik + max_sicaklik) / 2,max_sicaklik])
          sicakliklar_['sicak'] = fuzz.trimf(sicakliklar_.universe,[(min_sicaklik + max_sicaklik) / 2,max_sicaklik,max_sicaklik])

          self.hizlar_['yavas'] = fuzz.trimf(self.hizlar_.universe,[min_hiz,min_hiz,(min_hiz+max_hiz)/2])
          self.hizlar_['orta'] = fuzz.trimf(self.hizlar_.universe,[min_hiz,(min_hiz+max_hiz)/2,max_hiz])
          self.hizlar_['hizli'] = fuzz.trimf(self.hizlar_.universe,[(min_hiz+max_hiz)/2,max_hiz,max_hiz])

          rule_1 = Rule(sicakliklar_['dusuk'],self.hizlar_['yavas'])
          rule_2 = Rule(sicakliklar_['ilik'],self.hizlar_['orta'])
          rule_3 = Rule(sicakliklar_['sicak'],self.hizlar_['hizli'])

          control_system = ControlSystem([rule_1,rule_2,rule_3])
          self.control_system_sim = ControlSystemSimulation(control_system)

     def sensor_dimension(self,sensor_data):
          self.control_system_sim.input['temps'] = sensor_data

          self.control_system_sim.compute()

          output = self.control_system_sim.output

          net_hiz = output['speeds']

          keys_ = self.hizlar_.terms

          uygun_etiket = max(keys_,key=lambda e : fuzz.interp_membership(self.hizlar_.universe,keys_[e].mf,net_hiz))

          return self.karar_dict[uygun_etiket]
