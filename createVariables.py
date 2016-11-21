import numpy as np
import pandas as pd 


def createVariables(dataset):
	dataset.drop_duplicates(inplace=True)
	dataset['education'] = dataset.primary + dataset.secondary + dataset.university
	dataset['education2'] = dataset['education'] ** 2
	dataset['age2'] = dataset['age'] ** 2
	#ME QUEDO CON LOS QUE TRABAJAN Y TIENEN INGRESOS, SOLO USAMOS ESTOS
	dataset['id'] = (dataset.CODUSU.astype(str) + dataset.NRO_HOGAR.astype(str))
	dataset.P47T.replace(to_replace=[0], value=[1] , inplace=True, axis=None)
	dataset.P21.replace(to_replace=[0], value=[1] , inplace=True, axis=None)
	dataset['lnIncome']= np.log(dataset.P21)
	dataset['lnIncomeT']= np.log(dataset.P47T)
	return dataset

