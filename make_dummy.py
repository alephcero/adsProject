def make_dummy(data):
    data['male_14to24'] = ((data.female == 0) & ((data.age >= 14) & (data.age <= 24))).astype(int) 
    data['male_25to34'] = ((data.female == 0) & ((data.age >= 25 ) & ( data.age <= 34))).astype(int)
    data['female_14to24'] = ((data.female == 1) & ((data.age >= 14 ) & ( data.age <= 24))).astype(int)
    data['female_25to34'] = ((data.female == 1) & ((data.age >= 25 ) & ( data.age <= 34))).astype(int)
    data['female_35more'] = ((data.female == 1) & ((data.age >= 35 ))).astype(int)    
    return data

