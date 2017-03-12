# -*- coding:utf-8 -*-

import os
import shutil
import createDB
import numpy as np
import sqlite3 as sql
from matplotlib import pyplot as plt

DB = createDB.DB
TABLE = createDB.TABLE
IDVAR = createDB.IDVAR
VARIABLES = createDB.VARIABLES

def dataDictionary():
    conn = sql.connect(DB)
    c = conn.cursor()
    command = "SELECT * FROM " + TABLE
    dataDict = {}
    for line in c.execute(command):
        key = line[0]
        dataDict[key] = {}
        i = 1
        for variable in VARIABLES:
            dataDict[key][variable] = line[i]
            i = i + 1          
    conn.close()
    return dataDict

def variableDictionary():    
    conn = sql.connect(DB)
    c = conn.cursor()
    command = "SELECT * FROM " + TABLE
    varDict = {}
    varDict[IDVAR] = []
    for variable in VARIABLES:
        varDict[variable] = []        
    for line in c.execute(command):
        for i in range(0, len(line)):
            if i == 0:
                varDict[IDVAR] = varDict[IDVAR] + [line[i]]           
            else:
                variable = VARIABLES[i-1]
                varDict[variable] = varDict[variable] + [line[i]]           
    conn.close()
    return varDict

def gestationDictionary(gestation = VARIABLES[0]):
    gestDict = {}
    dataDict = dataDictionary()  
    varDict = variableDictionary()
    unique = list(set(varDict[gestation]))
    for value in unique:
        gestDict[value] = {}
        gestDict[value][IDVAR] = []
        for variable in VARIABLES:
            if variable != gestation:
                gestDict[value][variable] = []      
        for ind in varDict[IDVAR]:
            if dataDict[ind][gestation] == value:
                gestDict[value][IDVAR] = gestDict[value][IDVAR] + [ind]
                for variable in VARIABLES:
                    if variable != gestation:
                        gestDict[value][variable] = gestDict[value][variable] + [dataDict[ind][variable]]                  
    return gestDict
    
def polynomialDictionary(gestation = VARIABLES[0], degrees = 2, mean = False, plot = False):
    cwd = os.getcwd()
    dirList = os.listdir(cwd)
    polyDict = {}
    gestDict = gestationDictionary()
    values = gestDict.keys()
    values.sort()
    polyDict = {}
    if plot == True:
        try:
            if mean == 0:
                if "Values" in dirList:
                    shutil.rmtree("Values")
                else:
                    os.mkdir("Values")
                os.chdir("Values")
            else:
                if "Means" in dirList:
                    shutil.rmtree("Means")
                else:
                    os.mkdir("Means")
                os.chdir("Means")
        except:
            return polynomialDictionary(gestation, degrees, mean, plot)
    for variable in VARIABLES:
        if variable != gestation:
            polyDict[variable] = {}
            x = []
            y = []
            for value in values:
                if mean == False:
                    x = x + gestDict[value][variable]
                    for i in range(0, len(gestDict[value][variable])):                    
                        y.append(value)
                else:
                    x.append(np.mean(gestDict[value][variable]))
                    y.append(value)
            for degree in range(1, degrees + 1):
                polyDict[variable][degree] = {}
                p = list(np.polyfit(x, y, degree))
                n = len(x)
                df = n - len(p)
                if df < 0:
                    df = 0
                polyDict[variable][degree]['x'] = x
                polyDict[variable][degree]['y'] = y
                polyDict[variable][degree]['n'] = n
                polyDict[variable][degree]['p'] = p
                polyDict[variable][degree]['df'] = df
                f = []
                index = 0
                ssr = 0.0
                sst = 0.0
                for xi in x:
                    pred = 0
                    for i in range(0, len(p)):
                        pred = pred + p[i] * xi**(len(p)-i-1)
                    f.append(pred)
                    ssr = ssr + (y[index] - pred)**2
                    sst = sst + (y[index] - np.mean(y))**2
                    index = index + 1
                see = (ssr/n)**0.5
                polyDict[variable][degree]['f'] = f
                polyDict[variable][degree]['ssr'] = ssr
                polyDict[variable][degree]['sst'] = sst
                polyDict[variable][degree]['see'] = see
                r2 = 1 - ssr/sst
                polyDict[variable][degree]['R2'] = r2
                if plot == True:
                    plt.hold(True)
                    if mean == 0:
                        fileName = variable + " - Degree " + str(degree) + " - Values"
                        legend = ["Regression", "Observed Value"]
                    else:
                        fileName = variable + " - Degree " + str(degree) + " - Means"
                        legend = ["Regression", "Observed Mean"]
                    xMin = min(polyDict[variable][degree]["x"])
                    xMax = max(polyDict[variable][degree]["x"])
                    yMin = min(polyDict[variable][degree]["y"])
                    yMax = max(polyDict[variable][degree]["y"])
                    xMargin = (xMax - xMin)/100.0 
                    xPlot = []
                    xPlot.append(xMin)
                    xValue = xMin
                    for i in range(0,98):
                        xValue = xValue + xMargin
                        xPlot.append(xValue)
                    xPlot.append(xMax)
                    yPlot = []
                    for xi in xPlot:
                        pred = 0
                        for i in range(0, len(p)):
                            pred = pred + p[i] * xi**(len(p)-i-1)
                        yPlot.append(pred)
                    yMargin = (yMax - yMin)/100.0
                    plt.xlim([xMin - xMargin*5, xMax + xMargin*5])
                    plt.ylim([yMin - yMargin*10, yMax + yMargin*10])
                    plt.scatter(polyDict[variable][degree]["x"], polyDict[variable][degree]["y"],
                                marker = "o", color = "blue", edgecolor = "black", alpha = 0.5)
                    plt.plot(xPlot, yPlot, color = "red")
                    if degree == 1:
                        title = "$\mathregular{" + str(degree) + "^{st}}$ Degree Polynomial Regression"
                    elif degree == 2:
                        title = "$\mathregular{" + str(degree) + "^{nd}}$ Degree Polynomial Regression"
                    elif degree == 3:
                        title = "$\mathregular{" + str(degree) + "^{rd}}$ Degree Polynomial Regression"
                    else:
                        title = "$\mathregular{" + str(degree) + "^{th}}$ Degree Polynomial Regression"
                    plt.title(title)
                    plt.xlabel(variable)
                    plt.ylabel(gestation)
                    r2Anno = "%.3f" % polyDict[variable][degree]["R2"]
                    seeAnno = "%.3f" % polyDict[variable][degree]["see"]
                    annot1 = "$\mathregular{R^{2}}$ = " + r2Anno
                    annot2 = "$\mathregular{SEE}$ = " + seeAnno
                    plt.annotate(annot1, [xMin, yMax])
                    plt.annotate(annot2, [xMin, yMax - yMargin*10])
                    plt.legend(legend, loc=4)
                    plt.savefig(fileName, dpi = 500)
                    plt.hold(False)
                    plt.clf()
    os.chdir(cwd)
    return polyDict
                
def dataCSV():
    conn = sql.connect(DB)
    c = conn.cursor()
    command = "SELECT * FROM " + TABLE
    fileName = DB[:-2] + "csv"
    cwd = os.getcwd()
    items = os.listdir(cwd)
    if fileName in items:
        os.remove(fileName)
    op = open(fileName, "w")
    lineL = IDVAR + ","
    for variable in VARIABLES:
        lineL = lineL + variable + ","
    lineL = lineL[:-1] + "\n"
    op.write(lineL)
    for line in c.execute(command):
        lineL = ""
        for value in line:
            lineL = lineL + str(value) + ","
        lineL = lineL[:-1] + "\n"
        op.write(lineL)
    op.close()

    
    
    
    
    
    