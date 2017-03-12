# -*- coding:utf-8 -*-

import os
import sqlite3 as sql

DB = "CHLO.db" 
TABLE = "Autopsias"
IDVAR = "idd"
VARIABLES = ["GA (weeks)", "Body (g)", "CHL (cm)", "CRL (cm)", "HC (cm)",
             "CC (cm)", "AC (cm)", "FL (cm)", "HL (cm)", "MFL (cm)",
             "ICD (cm)", "OCD (cm)", "LPFW (cm)", "RPFW (cm)", "LEL (cm)",
             "REL (cm)", "PL (cm)", "ID (cm)", "Lungs (g)", "Thymus (g)",
             "liver (g)", "Spleen (g)", "Adrenals (g)", "Kidneys (g)"]

def createDatabase():
    cwd = os.getcwd()
    if DB in os.listdir(cwd):
        try:
            os.remove(DB)
            conn = sql.connect(DB)
            c = conn.cursor()
            command = "CREATE TABLE " + TABLE + " (" + IDVAR + " VARCHAR(255) PRIMARY KEY,"
            for variable in VARIABLES:
                command = command + "'" + variable + "'" + "FLOAT," 
            command = command[:-1] + ");"
            c.execute(command)
            conn.commit()
            conn.close()
        except:
            return createDatabase()
    else:
        conn = sql.connect(DB)
        c = conn.cursor()
        command = "CREATE TABLE " + TABLE + " (" + IDVAR + " VARCHAR(255) PRIMARY KEY,"
        for variable in VARIABLES:
            command = command + "'" + variable + "'" + "FLOAT," 
        command = command[:-1] + ");"
        c.execute(command)
        conn.commit()
        conn.close()
    