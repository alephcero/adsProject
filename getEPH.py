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
                        'P47T',
                        'P21',
                        'DECCFR',
                        'CH07',
                        'CH09',
                        'CH15']]

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
                  'P47T',
                  'P21',
                  'DECCFR',
                  'maritalStatus',
                  'reading',
                  'placeOfBirth']

    indNoW.index =range(0,indNoW.shape[0])

    dbf2 = simpledbf.Dbf5('data/Hogar_' + trimestre + '.dbf',codec='latin1')
    indRaw2 = dbf2.to_dataframe()

    indNoW2 = indRaw2.loc[indRaw2.REGION == 1,['CODUSU',
                                                'NRO_HOGAR',
                                                'REGION',
                                                'PONDERA',
                                                'IV1',
                                                'IV1_ESP',
                                                'IV2',
                                                'IV3',
                                                'IV3_ESP',
                                                'IV4',
                                                'IV5',
                                                'IV6',
                                                'IV7',
                                                'IV7_ESP',
                                                'IV8',
                                                'IV9',
                                                'IV10',
                                                'IV11',
                                                'IV12_1',
                                                'IV12_2',
                                                'IV12_3',
                                                'II1',
                                                'II2',
                                                'II3',
                                                'II3_1',
                                                'II4_1',
                                                'II4_2',
                                                'II4_3',
                                                'II7',
                                                'II7_ESP',
                                                'II8',
                                                'II8_ESP',
                                                'II9',
                                                'V1',
                                                'IX_TOT',
                                                'IX_MEN10',
                                                'IX_MAYEQ10',
                                                'ITF',
                                                'VII1_1',
                                                'VII1_2',
                                                'VII2_1',
                                                'VII2_2',
                                                'VII2_3',
                                                'VII2_4']]

    indNoW2.columns = [['CODUSU',
                        'NRO_HOGAR',
                        'REGION',
                        'PONDERA',
                        'HomeType',
                        'HomeTypeesp',
                        'RoomsNumber',
                        'FloorMaterial',
                        'FloorMaterialesp',
                        'RoofMaterial',
                        'RoofCoat',
                        'Water',
                        'WaterType',
                        'WaterTypeesp',
                        'Toilet',
                        'ToiletLocation',
                        'ToiletType',
                        'Sewer',
                        'DumpSites',
                        'Flooding',
                        'EmergencyLoc',
                        'UsableTotalRooms',
                        'SleepingRooms',
                        'OfficeRooms',
                        'OnlyWork',
                        'Kitchen',
                        'Sink',
                        'Garage',
                        'Ownership',
                        'Ownershipesp',
                        'CookingCombustible',
                        'CookingCombustibleesp',
                        'BathroomUse',
                        'Working',
                        'HouseMembers',
                        'Memberless10',
                        'Membermore10',
                        'TotalHouseHoldIncome',
                        'DomesticService1',
                        'DomesticService2',
                        'DomesticService3',
                        'DomesticService4',
                        'DomesticService5',
                        'DomesticService6']]

    indNoW2.index = range(0, indNoW2.shape[0])

    indNoW2.to_csv('data/cleanDataHousehold' + trimestre + '.csv', index=False)
    print 'csv file cleanDataHousehold', trimestre, '.csv successfully created in folder data/'

    indNoW.to_csv('data/cleanData' + trimestre + '.csv', index = False)
    print 'csv file cleanData',trimestre,'.csv successfully created in folder data/'
    return