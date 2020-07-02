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

# pH 4.0
_acidVoltage = 2000.00
_acidOffset = 178
# pH 7.0
_neutralVoltage = 1520.00
_neutralOffset = 178


TXT_FILE_PATH = "/home/greenponik/bundle_project_raspberry_core/"


class GreenPonik_PH():
    def begin(self):
        global _acidVoltage
        global _neutralVoltage
        try:
            print(">>>Initialization of ph lib<<<")
            with open('%sphdata.txt' % TXT_FILE_PATH, 'r') as f:
                neutralVoltageLine = f.readline()
                neutralVoltageLine = neutralVoltageLine.strip(
                    'neutralVoltage=')
                _neutralVoltage = float(neutralVoltageLine)
                print("get neutral voltage from txt file: %d" %
                      _neutralVoltage)
                acidVoltageLine = f.readline()
                acidVoltageLine = acidVoltageLine.strip('acidVoltage=')
                _acidVoltage = float(acidVoltageLine)
                print("get acid voltage from txt file: %d" % _acidVoltage)
        except:
            self.reset()
            pass

    def readPH(self, voltage):
        global _acidVoltage
        global _neutralVoltage
        print(">>>current voltage is: %.3f mV" % voltage)
        slope = (7.0-4.0)/((_neutralVoltage-1520.0) /
                           3.0 - (_acidVoltage-1520.0)/3.0)
        intercept = 7.0 - slope*(_neutralVoltage-1520.0)/3.0
        _phValue = slope*(voltage-1520.0)/3.0+intercept
        return round(_phValue, 2)

    def calibration(self, voltage):
        # automated 7 buffer solution detection
        if (voltage > (_neutralVoltage - _neutralOffset) and voltage < (_neutralVoltage + _neutralOffset)):
            print(">>>Buffer Solution:7.0")
            f = open('%sphdata.txt' % TXT_FILE_PATH, 'r+')
            flist = f.readlines()
            flist[0] = 'neutralVoltage=' + str(voltage) + '\n'
            f = open('%sphdata.txt' % TXT_FILE_PATH, 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>PH:7.0 Calibration completed<<<"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 7,
                       'voltage': voltage,
                       'status_message': status_msg}
            return cal_res
        # automated 4 buffer solution detection
        elif (voltage > (_acidVoltage - _acidOffset) and voltage < (_acidVoltage + _acidOffset)):
            print(">>>Buffer Solution:4.0")
            f = open('%sphdata.txt' % TXT_FILE_PATH, 'r+')
            flist = f.readlines()
            flist[1] = 'acidVoltage=' + str(voltage) + '\n'
            f = open('%sphdata.txt' % TXT_FILE_PATH, 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>PH:4.0 Calibration completed<<<"
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
        global _acidVoltage
        global _neutralVoltage
        _acidVoltage = 2000.00
        _neutralVoltage = 1520.0
        print(">>>Reset to default parameters<<<")
        try:
            print(">>>Read voltages from txt files<<<")
            f = open('%sphdata.txt' % TXT_FILE_PATH, 'r+')
            flist = f.readlines()
            flist[0] = 'neutralVoltage=' + str(_neutralVoltage) + '\n'
            flist[1] = 'acidVoltage=' + str(_acidVoltage) + '\n'
            f = open('%sphdata.txt' % TXT_FILE_PATH, 'w+')
            f.writelines(flist)
            f.close()
        except:
            print(">>>Cannot read voltages from txt files<<<")
            print(">>>Let's create them and apply the default values<<<")
            f = open('%sphdata.txt' % TXT_FILE_PATH, 'w')
            flist = 'neutralVoltage=' + str(_neutralVoltage) + '\n'
            flist += 'acidVoltage=' + str(_acidVoltage) + '\n'
            f.writelines(flist)
            f.close()
