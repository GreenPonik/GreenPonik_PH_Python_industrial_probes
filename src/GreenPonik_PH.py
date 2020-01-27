"""
####################################################################
####################################################################
####################################################################
################ GreenPonik Read PH through Python3 ################
################ Use only with industrial probes 3/4 ###############
####################################################################
####################################################################
####################################################################
Based on GreenPonik_PH_Python library
https://github.com/GreenPonik/GreenPonik_PH_Python

Need DFRobot_ADS1115 library
https://github.com/DFRobot/DFRobot_ADS1115/tree/master/RaspberryPi/Python
"""


import time
import sys

_acidVoltage = 2000.00
_acidOffset = 178
_neutralVoltage = 1520.00
_neutralOffset = 178


class GreenPonik_PH():
    def begin(self):
        global _acidVoltage
        global _neutralVoltage
        try:
            with open('phdata.txt', 'r') as f:
                neutralVoltageLine = f.readline()
                neutralVoltageLine = neutralVoltageLine.strip(
                    'neutralVoltage=')
                _neutralVoltage = float(neutralVoltageLine)
                acidVoltageLine = f.readline()
                acidVoltageLine = acidVoltageLine.strip('acidVoltage=')
                _acidVoltage = float(acidVoltageLine)
        except:
            self.reset()
            pass

    def readPH(self, voltage):
        global _acidVoltage
        global _neutralVoltage
        slope = (7.0-4.0)/((_neutralVoltage-1500.0) /
                           3.0 - (_acidVoltage-1500.0)/3.0)
        intercept = 7.0 - slope*(_neutralVoltage-1500.0)/3.0
        _phValue = slope*(voltage-1500.0)/3.0+intercept
        round(_phValue, 2)
        return _phValue

    def calibration(self, voltage):
        # automated 7 buffer solution detection
        if (voltage > (_neutralVoltage - _neutralOffset) and voltage < (_neutralVoltage + _neutralOffset)):
            print(">>>Buffer Solution:7.0")
            f = open('phdata.txt', 'r+')
            flist = f.readlines()
            flist[0] = 'neutralVoltage=' + str(voltage) + '\n'
            f = open('phdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>PH:7.0 Calibration completed<<<""
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 7,
                       'voltage': voltage,
                       'status_message': status_msg}
            return cal_res
        # automated 4 buffer solution detection
        elif (voltage > (_acidVoltage - _acidOffset) and voltage < (_acidVoltage + _acidOffset)):
            print(">>>Buffer Solution:4.0")
            f = open('phdata.txt', 'r+')
            flist = f.readlines()
            flist[1] = 'acidVoltage=' + str(voltage) + '\n'
            f = open('phdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>PH:4.0 Calibration completed<<<""
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 4,
                       'voltage': voltage,
                       'status_message': status_msg}
            return cal_res
        else:
            status_msg = ">>>Buffer Solution Error Try Again<<<"
            print(status_msg)
            cal_res = {'status': 9999, 'status_message': status_msg}
            return cal_res

    def reset(self):
        _acidVoltage = 2000.00
        _neutralVoltage = 1520.0
        try:
            f = open('phdata.txt', 'r+')
            flist = f.readlines()
            flist[0] = 'neutralVoltage=' + str(_neutralVoltage) + '\n'
            flist[1] = 'acidVoltage=' + str(_acidVoltage) + '\n'
            f = open('phdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            print(">>>Reset to default parameters<<<")
        except:
            f = open('phdata.txt', 'w')
            flist = 'neutralVoltage=' + str(_neutralVoltage) + '\n'
            flist += 'acidVoltage=' + str(_acidVoltage) + '\n'
            f.writelines(flist)
            f.close()
            print(">>>Reset to default parameters<<<")
