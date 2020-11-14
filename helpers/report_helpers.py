import pandas as pd



def change_to_direction(values: pd.Series) -> pd.Series:
    '''
    Takes in a pandas series and maps them to a direction based on the sign
    of the value.
    '''
    mapping = {-1:'down' ,0:'same', 1:'up'}
    return values.fillna(0).apply(lambda change: mapping[pd.np.sign(change)])
        
def high_since(values: pd.Series) -> pd.Series:
    '''
    Creates a Series of booleans based on whether value x is the 
    highest value in the series from [0:x]
    '''
    return values==values.cummax()

def low_since(values: pd.Series) -> pd.Series:
    '''
    Creates a Series of booleans based on whether value x is the 
    lowest value in the series from [0:x]
    
    non-pandas way:
        import math
        cur_min = math.inf
        output = []
        for item in list:
            if item <= cur_min:
                output.append(true)
                cur_min = item
            elif item > cur_min:
                output.append(false)
            else:
                output.append(math.nan)
    
    '''
    return values==values.cummin()

