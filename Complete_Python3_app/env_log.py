#!/usr/bin/env python

'''

FILE NAME
env_log.py

1. WHAT IT DOES
Takes a reading from a DHT sensor and records the values in an SQLite3 database using a Raspberry Pi.

2. REQUIRES
* Any Raspberry Pi
* A DHT sensor
* A 10kOhm resistor
* Jumper wires
* Appropriate Google API credentials for Google Drive and Google Sheet.

3. ORIGINAL WORK
Raspberry Full stack 2015, Peter Dalmaris

4. HARDWARE
D17: Data pin for sensor

5. SOFTWARE
Command line terminal
Simple text editor
Libraries:
import sqlite3
import sys
import Adafruit_DHT
import gspread
from oauth2client.service_account import ServiceAccountCredentials

6. WARNING!
None

7. CREATED

8. TYPICAL OUTPUT
No text output. Two new records are inserted in the database and in a Google Sheet when the script is executed

 // 9. COMMENTS
--

 // 10. END

'''


import sqlite3
import sys
import Adafruit_DHT
from time import gmtime, strftime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import RPi.GPIO as GPIO
import requests
import os
from twilio.rest import Client


def email_alert(device_id, temp, hum):
    report = {}
    report["value1"] = device_id
    report["value2"] = temp
    report["value3"] = hum
    key_val = os.environ["IFTTT_RPIFS_REPORT_KEY"]
    req_link = f"https://maker.ifttt.com/trigger/RPiFS_report/with/key/{key_val}"
    requests.post(req_link, data=report)

def text_alert(device_id, temp, hum):
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    my_twilio_phone_number = os.environ["TWILIO_PHONE_NUMBER"]
    receive_phone_number = os.environ["MY_PHONE_NUMBER"]
    deg_sign = u"\N{DEGREE SIGN}"
    report = f'Device {device_id} reported a temperature of {temp}{deg_sign}C and {hum}% humidity.'
    client = Client(account_sid, auth_token)
    client.messages.create(to = receive_phone_number,
                           from_ = my_twilio_phone_number,
                           body = report)

def log_values(sensor_id, temp, hum):
    GPIO.output(pin, GPIO.HIGH)  ## Turn on GPIO pin (HIGH)

    # It is important to provide an absolute path to the database
    # file, otherwise Cron won't be able to find it!
    conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
    curs=conn.cursor()

    #This will store the new record at UTC
    curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP,
                 'localtime'), (?), (?))""", (sensor_id,temp))

    #This will store the new record at UTC
    curs.execute("""INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP,
                 'localtime'), (?), (?))""", (sensor_id,hum))
    conn.commit()
    conn.close()

    # Create a new record in the Google Sheet
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/var/www/lab_app/RPiFSv2-f4ae75e2c55f.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('RPiFSv2 sensor data').sheet1
    row = [strftime("%Y-%m-%d %H:%M:%S", gmtime()),
           sensor_id, round(temp,2), round(hum,2)]
    sheet.append_row(row)

    print("Email alert if needed...")

    if temp > 81 or hum > 65:
        print('Sending email alert message')
        email_alert(sensor_id, temp, hum)

    if temp > 82 or hum > 70:
        print('Sending text alert message')
        text_alert(sensor_id, temp, hum)

    GPIO.output(pin, GPIO.LOW)   ## Turn off GPIO pin (LOW)

GPIO.setwarnings(False)
pin = 7                    ## We're working with pin 7
GPIO.setmode(GPIO.BOARD)   ## Use BOARD pin numbering
GPIO.setup(pin, GPIO.OUT)  ## Set pin 7 to OUTPUT

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 17)

# If you don't have a sensor but still wish to run this program, comment out
# all the sensor related lines, and uncomment the following lines (these will
# produce random numbers for the temperature and humidity variables):
# import random
# humidity = random.randint(1,100)
# temperature = random.randint(10,30)
if humidity is not None and temperature is not None:
    # Convert the temperature to Fahrenheit.
    temperature = temperature * 9/5.0 + 32

    if (humidity <= 100):
        log_values("1", temperature, humidity)
    else:
        print(f'Invalid humidity reading of {humidity}')
else:
    log_values("1", -999, -999)
