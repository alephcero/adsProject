import pandas as pd
import numpy as np
import os
import sys
import simpledbf


def getEPHdbf(censusstring):
    print ("Downloading", censusstring)
    ### First I will heck that it is not already there
    if not os.path.isfile("data/Individual_" + censusstring + ".dbf"):
        if os.path.isfile('Individual_' + censusstring + ".dbf"):
            # if in the current dir just move it
            if os.system("mv " + 'Individual_' + censusstring + ".dbf " + "data/"):
                print ("Error moving file!, Please check!")
        # otherwise start looking for the zip file
        else:
            if not os.path.isfile("data/" + censusstring + "_dbf.zip"):
                if not os.path.isfile(censusstring + "_dbf.zip"):
                    os.system(
                        "curl -O http://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/" + censusstring + "_dbf.zip")
                ###  To move it I use the os.system() functions to run bash commands with arguments
                os.system("mv " + censusstring + "_dbf.zip " + "data/")
            ### unzip the csv
            os.system("unzip " + "data/" + censusstring + "_dbf.zip -d data/")

    if not os.path.isfile("data/" + 'Individual_' + censusstring + ".dbf"):
        print ("WARNING!!! something is wrong: the file is not there!")

    else:
        print ("file in place, creating CSV file")

    trimestre = censusstring

    dbf = simpledbf.Dbf5('data/Individual_' + trimestre + '.dbf',codec='latin1')
    indRaw = dbf.to_dataframe()

    indNoW = indRaw.loc[indRaw.REGION == 1,['CODUSU',
                        'NRO_HOGAR',
                        'COMPONENTE',
                        'AGLOMERADO',
                        'PONDERA',
                        'CH03',
                        'CH04',
                        'CH06',
                        #'CH10', ## borraR
                        'CH12', ## schoolLevel
                        'CH13',
                        'CH14',
                        'ESTADO',
                        #'NIVEL_ED',## borrar
                        'CAT_OCUP',
                        'CAT_INAC',
                        'ITF',
                        'IPCF',
                        'P47T']]

    indNoW.columns = ['CODUSU',
                        'NRO_HOGAR',
                        'COMPONENTE',
                        'AGLOMERADO',
                        'PONDERA',
                        'familyRelation',
                        'female',
                        'age',
                        #'schooled',## borrar
                        'schoolLevel',## schoolLevel
                        'finishedYear',
                        'lastYear',
                        'activity',
                        #'educLevel',## borrar
                        'empCond',
                        'unempCond',
                        'ITF',
                        'IPCF',
                  'P47T']
    indNoW.index =range(0,indNoW.shape[0])

    indNoW.to_csv('data/cleanData' + trimestre + '.csv', index = False)
    print 'csv file cleanData',trimestre,'.csv successfully created in folder data/'
    return