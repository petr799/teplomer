import os 
import re
import sys
import MySQLdb
import glob 
import time 
import subprocess
import datetime

os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm') 
#id_cid = "%s" % id_cidla[0]
#base_dir = '/sys/bus/w1/devices/' 
#device_folder = glob.glob(base_dir + id_cid)[0]
#device_file = device_folder + '/w1_slave' 

def read_temp_raw():
	catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
# Open database connection
db = MySQLdb.connect("localhost","tmep","heslotmep","tmep" )

try:
	#prepare a cursor object using cursor() method
	cursor = db.cursor()
	cursor.execute("SELECT id_cidla FROM provoz")
	id_cidla = cursor.fetchall()
	cursor.execute("SELECT COUNT(id) FROM provoz")
	count_room = cursor.fetchone()

# inicializace promenne teplota
	teplota = {}

# smycka pro vycitani teplot z cidel do promenne teplota
	for x in range (0, count_room[0]):
		base_dir = '/sys/bus/w1/devices/'
		device_folder = glob.glob(base_dir + "%s" % id_cidla[x])[0]
		device_file = device_folder + '/w1_slave'
		teplota[x] = (read_temp())
#		slovo = 'teplota' + x[0]
#		print slovo
#		print teplota[x]
	print teplota

#	cursor.execute("""INSERT INTO tme (kdy, room1, room2) VALUES (%s, %s, %s)""",(datetime.datetime.now(), teplota[0], teplota[1]
	# Execute the SQL command
#	cursor.execute("""INSERT INTO tme (kdy, teplota) VALUES (%s, %s)""",(datetime.datetime.now(), (read_temp())))

	# Commit your changes in the database
	db.commit()

	#close connection to database
	db.close()


except:
	db.rollback()
	db.close()
	print "nefunguje to"
