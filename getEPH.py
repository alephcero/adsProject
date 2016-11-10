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



def schoolYears(dataset):
    '''
    This function takes a dataset with
    schoolLevel: last level of school attended
    finishedYear: if the person finished that level
    lastYear: last year of that level aproved
    and returns a new dataset with the amount of school years for each level
    '''
    primary = []
    secondary = []
    university = []
    
    for i in range(dataset.shape[0]):
        
        #kinder, special or no school
        if ((dataset['schoolLevel'][i] > 8) | (dataset['schoolLevel'][i] < 2)):
            primary_i = 0
            secondary_i = 0
            university_i = 0
        
        #from primary to university
        else:
            #finished their level
            if dataset['finishedYear'][i] == 1:
                
                #finish primary
                if ((dataset['schoolLevel'][i] == 2) | (dataset['schoolLevel'][i] == 3)):
                    primary_i = 7
                    secondary_i = 0
                    university_i = 0
                
                #finish seconday
                elif ((dataset['schoolLevel'][i] == 4) | (dataset['schoolLevel'][i] == 5)):
                    primary_i = 7
                    secondary_i = 5
                    university_i = 0
                
                #finish college
                elif dataset['schoolLevel'][i] == 6:
                    primary_i = 7
                    secondary_i = 5
                    university_i = 3
                    
                #finish university
                elif ((dataset['schoolLevel'][i] == 7) | (dataset['schoolLevel'][i] == 8)):
                    primary_i = 7
                    secondary_i = 5
                    university_i = 5
            # didn't finish
            elif dataset['finishedYear'][i] == 2:
                
                #not finish primary
                if dataset['schoolLevel'][i] == 2:
                    if dataset['lastYear'][i] > 90:
                        primary_i = 0
                    elif dataset['lastYear'][i] > 6:
                        primary_i = 6
                    else:
                        primary_i = dataset['lastYear'][i]
                    secondary_i = 0
                    
                    university_i = 0
                
                #not finish EGB
                elif dataset['schoolLevel'][i] == 3:
                    if dataset['lastYear'][i] > 90:
                        primary_i = 0
                        secondary_i = 0
                    elif dataset['lastYear'][i] > 7:
                        primary_i = 7
                        secondary_i = dataset['lastYear'][i] - 7
                    else:
                        primary_i = dataset['lastYear'][i]
                        secondary_i = 0
                        
                    university_i = 0

                    
                #not finish Secondary
                elif dataset['schoolLevel'][i] == 4:
                    if dataset['lastYear'][i] > 90:
                        secondary_i = 0
                    elif dataset['lastYear'][i] > 5:
                        secondary_i = 5
                    else:
                        secondary_i = dataset['lastYear'][i]
                                            
                    primary_i = 7
                    university_i = 0
                
                #not finish polimodal
                elif dataset['schoolLevel'][i] == 5:
                    if dataset['lastYear'][i] > 90:
                        secondary_i = 0
                    elif dataset['lastYear'][i] > 2:
                        secondary_i = 4
                    else:
                        secondary_i = dataset['lastYear'][i]
                    
                    primary_i = 7    
                    university_i = 0
               
                
                #not finish college
                elif dataset['schoolLevel'][i] == 6:
                    if dataset['lastYear'][i] > 90:
                        university_i = 2
                    elif dataset['lastYear'][i] > 3:
                        university_i = 3
                    else:
                        university_i = dataset['lastYear'][i]
                        
                    primary_i = 7
                    secondary_i = 5
                    
                    
                #no finish university
                elif ((dataset['schoolLevel'][i] == 7) | (dataset['schoolLevel'][i] == 8)):
                    if dataset['lastYear'][i] > 90:
                        university_i = 3
                    elif dataset['lastYear'][i] > 5:
                        university_i = 5
                    else:
                        university_i = dataset['lastYear'][i]
                        
                    primary_i = 7
                    secondary_i = 5

                #last year proved
                
                
            #don't know
            else:
                primary_i = 0
                secondary_i = 0
                university_i = 0
            
        
        #add values to list
        primary.append(primary_i)
        secondary.append(secondary_i)
        university.append(university_i)
    
    dataset['primary'] = primary
    dataset['secondary'] = secondary
    dataset['university'] = university
    
    return dataset