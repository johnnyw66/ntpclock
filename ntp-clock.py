#! /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -u


# Requires pip3 install pytz colored cursor astral atexit netifaces
import os
import time
from datetime import datetime
from datetime import date
import pytz
from colored import fg, bg, attr
import sys
import configparser
import cursor
import astral
import astral.sun as sun
import atexit
import netifaces as ni
import subprocess
import ntp_clock_numbers as num
import platform
import re
import socket

def restoreCursor():
    cursor.show()

# Hide cursor at launch and restore cursor on exit
cursor.hide()
atexit.register(restoreCursor)

def heightFiller(lines):
        for i in range(int(lines)-1):
                print ("\r%s%s%s%s%s" % (fg(fgColor), bg(bgColor), attr('bold'), " ".center(width), attr('reset')))






def getIP():
    try:
        if platform.system() == 'Darwin':  # macOS
            output = subprocess.check_output(['route', 'get', 'default']).decode()
            #print("DEBUG: route get default output:\n", output)

            match = re.search(r'gateway:\s+(\S+)', output)
            if not match:
                return "unknown"

            gateway = match.group(1)
            try:
                # Try to resolve hostname to IP
                gateway_ip = socket.gethostbyname(gateway)
            except socket.gaierror:
                # If resolution fails, return the original gateway string
                gateway_ip = gateway

            return gateway_ip

        elif platform.system() == 'Linux':
            output = subprocess.check_output(['ip', 'route', 'show', 'default']).decode().split()
            return output[2] if len(output) >= 3 else "unknown"

        else:
            return "unsupported"

    except Exception as e:
        print(f"Error in getIP(): {e}")
        return "error"

Config = configparser.ConfigParser()
Config.read("./settings.conf")

tz = pytz.timezone(Config.get('settings', 'timezone'))

try:
        rows, columns = os.popen('stty size', 'r').read().split()
        autoAllow = True
except:
        rows = 30
        columns = 100
        autoAllow = False

width = int(columns)
widthAuto = True

height = int(rows)
heightAuto = True

formatChange = True

location = astral.LocationInfo(Config.get('location', 'city'), Config.get('location', 'region'), Config.get('settings', 'timezone'), Config.get('location', 'latitude'), Config.get('location', 'longitude'))

fgColorDay=Config.get('settings', 'fgColorDay')
bgColorDay=Config.get('settings', 'bgColorDay')
fgColorNight=Config.get('settings', 'fgColorNight')
bgColorNight=Config.get('settings', 'bgColorNight')

ipAddress = getIP()

last = str(datetime.now().minute) + str(datetime.now().second)

while True:
        
        sunrise = sun.sunrise(location.observer, date=date.today(), tzinfo=tz)
        sunset = sun.sunset(location.observer, date=date.today(), tzinfo=tz)

        if datetime.now(tz) > sunrise and datetime.now(tz) < sunset:
                fgColor = fgColorDay
                bgColor = bgColorNight
                mode = "Day"
        else:
                fgColor = fgColorNight
                bgColor = bgColorNight
                mode = "Night"

        output1 = " "
        output2 = " "
        output3 = " "
        output4 = " "
        output5 = " "

        if formatChange:
                nothing = os.system('clear')
                formatChange = False
        else:
                for i in range(height-1):
                        sys.stdout.write("\033[F")

        label = "IP Address : "
        print ("%s%s%s%s" % (fg('grey_27'), label, ipAddress.center(width-(len(label)*2)).rjust(len(label)), attr('reset')))

        heightFiller((height + 6)/2)

        quickClock = True
        while True:
                if (1.0 - (time.time() % 1.0)) > 0 and not quickClock:
                        try:
                                time.sleep(1.0 - (time.time() % 1.0))
                        except KeyboardInterrupt:
                                nothing = os.system('clear')
                                print ("Program Ended By User...Done.")
                                sys.exit()
                        except:
                                nothing = True

                for i in range(7):
                        sys.stdout.write("\033[F")

                output1 = ""
                output2 = ""
                output3 = ""
                output4 = ""
                output5 = ""
                count = 0

                for number in datetime.now(tz).strftime('%H:%M.%S'):
                        if count > 0:
                                output1 += "  "
                                output2 += "  "
                                output3 += "  "
                                output4 += "  "
                                output5 += "  "

                        if number.isdigit():
                                output1 += num.number1[int(number)]
                                output2 += num.number2[int(number)]
                                output3 += num.number3[int(number)]
                                output4 += num.number4[int(number)]
                                output5 += num.number5[int(number)]
                        elif number == ":":
                                output1 += num.colon1
                                output2 += num.colon2
                                output3 += num.colon3
                                output4 += num.colon4
                                output5 += num.colon5
                        elif number == ".":
                                output1 += num.period1
                                output2 += num.period2
                                output3 += num.period3
                                output4 += num.period4
                                output5 += num.period5
                        count += 1

                print ("\r%s%s%s%s%s" % (fg(fgColor), bg(bgColor), attr('bold'), datetime.now(tz).strftime('%A %B %d, %Y %Z').center(width), attr('reset')))
                print ("\r%s%s%s%s%s" % (fg(fgColor), bg(bgColor), attr('bold'), " ".center(width), attr('reset')))
                print ("\r%s%s%s%s%s" % (fg(fgColor), bg(bgColor), attr('bold'), output1.center(width), attr('reset')))
                print ("\r%s%s%s%s%s" % (fg(fgColor), bg(bgColor), attr('bold'), output2.center(width), attr('reset')))
                print ("\r%s%s%s%s%s" % (fg(fgColor), bg(bgColor), attr('bold'), output3.center(width), attr('reset')))
                print ("\r%s%s%s%s%s" % (fg(fgColor), bg(bgColor), attr('bold'), output4.center(width), attr('reset')))
                print ("\r%s%s%s%s%s" % (fg(fgColor), bg(bgColor), attr('bold'), output5.center(width), attr('reset')))
                print ("\r%s%s%s%s%s" % (fg(fgColor), bg(bgColor), attr('bold'), " ".center(width), attr('reset')), end ="")
                quickClock = False

                if datetime.now().minute % 1 == 0 and datetime.now().second == 0 and last != str(datetime.now().minute) + str(datetime.now().second):
                        last = str(datetime.now().minute) + str(datetime.now().second)
                        break
                else:
                        if widthAuto or heightAuto:
                                if autoAllow:
                                        update = False
                                        rows, columns = os.popen('stty size', 'r').read().split()
                                if widthAuto and width != int(columns):
                                        width = int(columns)
                                        update = True
                                        formatChange = True
                                if heightAuto and height != int(rows):
                                        height = int(rows)
                                        update = True
                                        formatChange = True
                        if datetime.now(tz) > sunrise and datetime.now(tz) < sunset and mode == "Night":
                                # After Sunrise - Switch to Day Mode
                                update = True
                        elif datetime.now(tz) > sunrise and datetime.now(tz) > sunset and mode == "Day":
                                # After Sunset - Switch to Night Mode
                                update = True
                        newIpAddress = getIP()
                        if newIpAddress != ipAddress:
                                ipAddress = newIpAddress
                                update = True
                        if update:
                                break

