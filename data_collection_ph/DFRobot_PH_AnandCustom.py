'''!
  @file DFRobot_PH.py
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Jiawei Zhang](jiawei.zhang@dfrobot.com) edited by Anand
  @version  V1.0
  @date  2023-12-19
  @url https://github.com/DFRobot/DFRobot_PH
'''

import time
import sys
n_low = 290
n_mean = 310
n_high = 330
a_low = 335
a_high = 347

_temperature      = 25.0
_acidVoltage      = 340.0
_neutralVoltage   = 310.0
class DFRobot_PH():
	def begin(self):
		'''!
          @brief   Initialization The Analog pH Sensor.
        '''
		global _acidVoltage
		global _neutralVoltage
		try:
			with open('phdata.txt','r') as f:
				neutralVoltageLine = f.readline()
				neutralVoltageLine = neutralVoltageLine.strip('neutralVoltage=')
				_neutralVoltage    = float(neutralVoltageLine)
				acidVoltageLine    = f.readline()
				acidVoltageLine    = acidVoltageLine.strip('acidVoltage=')
				_acidVoltage       = float(acidVoltageLine)
		except :
			print ("phdata.txt ERROR ! Please run DFRobot_PH_Reset")
			sys.exit(1)
	def read_PH(self,voltage,temperature):
		'''!
          @brief   Convert voltage to PH with temperature compensation.
		  @note voltage to pH value, with temperature compensation
          @param voltage       Voltage value
		  @param temperature   Ambient temperature
          @return  The PH value
        '''
		global _acidVoltage
		global _neutralVoltage
		slope     = (7.0-4.0)/((_neutralVoltage-n_mean)/3.0 - (_acidVoltage-n_mean)/3.0)
		intercept = 7.0 - slope*(_neutralVoltage-n_mean)/3.0
		_phValue  = slope*(voltage-n_mean)/3.0+intercept
		round(_phValue,2)
		return _phValue
	def calibration(self,voltage):
		'''!
          @brief   Calibrate the calibration data.
          @param voltage       Voltage value
        '''
		if (voltage>n_low and voltage<n_high):
			print (">>>Buffer Solution:7.0")
			f=open('phdata.txt','r+')
			flist=f.readlines()
			flist[0]='neutralVoltage='+ str(voltage) + '\n'
			f=open('phdata.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>PH:7.0 Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
			time.sleep(5.0)
		elif (voltage>a_low and voltage<a_high):
			print (">>>Buffer Solution:4.0")
			f=open('phdata.txt','r+')
			flist=f.readlines()
			flist[1]='acidVoltage='+ str(voltage) + '\n'
			f=open('phdata.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>PH:4.0 Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
			time.sleep(5.0)
		else:
			print (">>>Buffer Solution Error Try Again<<<")
	def reset(self):
		'''!
          @brief   Reset the calibration data to default value.
        '''
		
		_acidVoltage    = 2032.44
		_neutralVoltage = 1500.0
		try:
			f=open('phdata.txt','r+')
			flist=f.readlines()
			flist[0]='neutralVoltage='+ str(_neutralVoltage) + '\n'
			flist[1]='acidVoltage='+ str(_acidVoltage) + '\n'
			f=open('phdata.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>Reset to default parameters<<<")
		except:
			f=open('phdata.txt','w')
			#flist=f.readlines()
			flist   ='neutralVoltage='+ str(_neutralVoltage) + '\n'
			flist  +='acidVoltage='+ str(_acidVoltage) + '\n'
			#f=open('data.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>Reset to default parameters<<<") 