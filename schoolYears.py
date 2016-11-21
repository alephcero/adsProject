import pandas as pd
import numpy as np
import os
import sys
import simpledbf
import math

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
                    elif pd.isnull(dataset['lastYear'][i]):
                    	primary_i = 3
                    else:
                        primary_i = dataset['lastYear'][i]
                    secondary_i = 0
                    
                    university_i = 0
                
                #not finish EGB
                elif dataset['schoolLevel'][i] == 3:
                    if dataset['lastYear'][i] > 90:
                        primary_i = 0
                        secondary_i = 0
                    elif pd.isnull(dataset['lastYear'][i]):
                    	primary_i = 3
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
                    elif pd.isnull(dataset['lastYear'][i]):
                    	secondary_i = 2
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
                    elif pd.isnull(dataset['lastYear'][i]):
                    	secondary_i = 1
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
                    elif pd.isnull(dataset['lastYear'][i]):
                    	university_i = 1
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
                    elif pd.isnull(dataset['lastYear'][i]):
                    	university_i = 2
                    elif dataset['lastYear'][i] > 5:
                        university_i = 5
                    elif math.isnan(dataset['lastYear'][i]):
                        university_i = 2

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
