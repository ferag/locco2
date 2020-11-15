#!/usr/bin/python3
import mh_z19

import os, time, sys
import RPi.GPIO as GPIO
import datetime
import mysql.connector
import configparser
import sqlite3

redPin = 11   #Set to appropriate GPIO
greenPin = 13 #Should be set in the
bluePin = 15  #GPIO.BOARD format

config = configparser.ConfigParser()
config.read('/home/ubuntu/config.ini')

db_host = config['db']['host']
db_name = config['db']['name']
db_user = config['db']['user']
db_pass = config['db']['pass']
db_local = config['db']['local_db']

def blink(pin):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def redOn():
    blink(redPin)

def redOff():
    turnOff(redPin)

def greenOn():
    blink(greenPin)

def greenOff():
    turnOff(greenPin)

def blueOn():
    blink(bluePin)

def blueOff():
    turnOff(bluePin)

def yellowOn():
    blink(redPin)
    blink(greenPin)

def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)

def cyanOn():
    blink(greenPin)
    blink(bluePin)

def cyanOff():
    turnOff(greenPin)
    turnOff(bluePin)

def magentaOn():
    blink(redPin)
    blink(bluePin)

def magentaOff():
    turnOff(redPin)
    turnOff(bluePin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)

def connect_online_db():
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    return mydb

def connect_local_db():
    mydb = sqlite3.connect(db_local)
    return mydb

def check_local_data():
    mydb = connect_local_db()
    cursor = mydb.cursor()
    cursor.execute('SELECT date, co2, temp from co2_device')
    result = cursor.fetchall()
    mydb.close()
    return result

def drop_local(timestamp):
    try:
        mydb = connect_local_db()
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM co2_device where date = '%s'" % timestamp)
        print("DELETE FROM co2_device where date = %s" % timestamp)
        mydb.commit()
        mydb.close()
    except Exception as e:
        print("Problem at deleting item: %s" % e)

def update_local():
    if os.system("ping -c 1 %s" % db_host) == 0:
        check_local = check_local_data()
        if len(check_local) != 0:
            for row in check_local:
                insert_values(row[0],row[1],row[2])
                drop_local(row[0])

def insert_values(timestamp, co2, temp):
    try:
        mydb = connect_local_db()
        iam = "LOCAL | "
        mydb = connect_online_db()
        iam = "REMOTE | "
    except Exception as e:
        print("Exception: %s" % e)
    finally:
        cursor = mydb.cursor()
        query = "INSERT INTO co2_device(date, co2, temp) VALUES ('%s', %i, %i);" % (timestamp, co2, temp)
        print(iam + query)
        cursor.execute(query)
        mydb.commit()
    mydb.close()

def main():
    while(True):
        try:
            output = mh_z19.read_all()
            co2 = int(output['co2'])
            temp = output['temperature']
            print("CO2: %s | Temp: %s" % (co2, temp))
            if(co2 < 400):
                whiteOff()
                time.sleep(0.3)
                blueOn()
            elif(co2 >= 400 and co2 < 700):
                whiteOff()
                time.sleep(0.3)
                cyanOn()
            elif(co2 >= 700 and co2 < 850):
                whiteOff()
                time.sleep(0.3)
                greenOn()
            elif(co2 >= 850 and co2 < 1500):
                whiteOff()
                time.sleep(0.3)
                yellowOn()
            elif(co2 >= 1500 and co2 < 1750):
                whiteOff()
                time.sleep(0.3)
                magentaOn()
            elif(co2 >= 1750 and co2 < 5500):
                whiteOff()
                time.sleep(0.3)
                redOn()
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            insert_values(timestamp, co2, temp)
        except Exception as e:
            print("Exception: %s" % e)
        try:
            update_local()
        except Exception as e:
            print("Exception: %s" % e)
        time.sleep(60)

if __name__ == "__main__":
    main()

