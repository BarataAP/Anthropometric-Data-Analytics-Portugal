# -*- coding:utf-8 -*-

import os
import createDB
import sqlite3 as sql

cwd = os.getcwd()
items = os.listdir(cwd)
if createDB.DB not in items:
    createDB.createDatabase()
    
conn = sql.connect(createDB.DB) 
c = conn.cursor()
userInput = {}
prompt = createDB.IDVAR + ":"
while len(prompt) < 10:
    prompt = prompt + " "
    
userInput[createDB.IDVAR] = str(raw_input(prompt))       
for variable in createDB.VARIABLES:
    prompt = variable + ':'
    while len(prompt) < 10:
        prompt = prompt + " "         
    userInput[variable] = str(raw_input(prompt))
           
command = "INSERT INTO " + createDB.TABLE + " VALUES ('" + userInput[createDB.IDVAR] + "',"
for variable in createDB.VARIABLES:
    command = command + userInput[variable] + ","
    
command = command[:-1] + ");"
print ""
run = str(raw_input("Press ENTER to submit"))
if run == "":
	try:
		c.execute(command)
		conn.commit()
		conn.close()
	except:
		conn.close()
		raw_input("Could not insert values")
        
else:
	conn.close()    
