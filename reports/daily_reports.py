import pandas as pd 
import datetime
from helpers.report_helpers import change_to_direction, high_since, low_since
from helpers.constants import DATE, PRICE

'''
This module contains various methods to generate daily reports of cryptocurrency.


'''
    
# Constants
#DATE = 'date'
#PRICE = 'price'

def daily_report_at_hour(df: pd.DataFrame, reporting_hour: int) -> pd.DataFrame:
    '''
    This method takes in a dataframe that must include "date" and "price" as columns
    and 'price' within their schema, and returns a report in the following format:
        [
            {
                "date": "{date}",
                “price”: ”{value}",            
                "direction": "{up/down/same}",            
                "change": "{amount}",            
                "dayOfWeek": "{name}”,            
                "highSinceStart": "{true/false}”,            
                “lowSinceStart": "{true/false}”                                     
            }
        ]
    params: 
        raw_data (list): a list of dictionaries that is inteneded to be transformed
        reporting_hour (int): the hour of the day that reports should be generated for.
        
    example:
        daily_report_at_hour(data, 0) will return a dataframe with information 
        about the value of a coin at 00:00:00 each day that there is data given.
    '''
    if reporting_hour < 0 or reporting_hour > 24 or type(reporting_hour) is not int:
        raise RuntimeError('reporting_hour must be integer in range [0,24]')
    
    
    # prune unneeded data
    df = df[[DATE, PRICE]]
    df = df[ df[DATE].dt.time == datetime.time(reporting_hour, 0,0,0) ]
    
    # build derived columns and rename columns
    df['change']=df[PRICE].diff()
    df['direction'] = change_to_direction(df['change'])
    df['dayOfWeek'] = df[DATE].dt.day_name()
    df['highSinceStart'] = high_since(df[PRICE])
    df['lowSinceStart'] = low_since(df[PRICE])
    
    if not df[DATE].is_unique:
        raise Warning('Warning, duplicate values for certain dates')    
        
    return df