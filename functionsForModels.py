import pandas as pd
import numpy as np
import os
import sys
import simpledbf
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
import math




def prepareDataForModel(dataset):
    #select variables and people with jobs and income for that job
    jobsAndIncome = ((dataset.activity==1) & (dataset.P21>1))
    dataModel = dataset.copy().loc[jobsAndIncome,
                              ['PONDERA','P47T','P21',
                               'primary','secondary','university',
                               'male_14to24','male_25to34',
                               'female_14to24', 'female_25to34', 'female_35more',
                               'female','age']]
    
    dataModel['education'] = dataModel.primary + dataModel.secondary + dataModel.university
    dataModel['education2'] = dataModel['education'] ** 2
    dataModel['age2'] = dataModel['age'] ** 2
    dataModel.P47T.replace(to_replace=[0], value=[1] , inplace=True, axis=None)
    dataModel.P21.replace(to_replace=[0], value=[1] , inplace=True, axis=None)
    dataModel['lnIncome']= np.log(dataModel.P21)
    dataModel['lnIncomeT']= np.log(dataModel.P47T)
    dataModel.dropna(inplace=True)
    return dataModel
    

def runModel(dataset, income = 'lnIncome',
              variables = [
        'primary','secondary','university',
        'male_14to24','male_25to34',
        'female_14to24', 'female_25to34', 'female_35more']):
    
    '''
    This function takes a data set, runs a model according to specifications,
    and returns the model, printing the summary
    '''
    selectedVariables = ['PONDERA',income] + variables
    dataToRun = dataset.loc[:,selectedVariables]
    y = dataToRun.copy().iloc[:,1].values
    X = sm.add_constant(dataToRun.copy().iloc[:,2:].values)
    w = dataToRun.copy().iloc[:,0].values
    lm = sm.WLS(y, X, weights=1. / w).fit()
    print lm.summary()
    for i in range(1,len(variables)+1):
        print 'x%d: %s' % (i,variables[i-1])
    #testing within sample
    R_IS=[]
    R_OS=[]
    nCross=1000
    
    for i in range(nCross):
        X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(X, y, w, test_size=0.33)
        lm = sm.WLS(y_train, X_train, weights=1. / w_train, hasconst=False).fit()        
        R_IS.append(1-((np.asarray(lm.predict(exog = X_train))-y_train)**2).sum()/((y_train-np.mean(y_train))**2).sum())                                                                     
        R_OS.append(1-((np.asarray(lm.predict(exog = X_test))-y_test)**2).sum()/((y_test-np.mean(y_test))**2).sum())
    print("IS R-squared for {} times is {}".format(nCross,np.mean(R_IS)))
    print("OS R-squared for {} times is {}".format(nCross,np.mean(R_OS)))

    return lm

