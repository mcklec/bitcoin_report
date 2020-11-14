import pandas as pd 
import datetime
from helpers.report_helpers import change_to_direction, high_since, low_since

'''
This module contains various methods to generate daily reports of cryptocurrency.


'''
    
# Constants
DATE = 'date'
PRICE = 'price'

def daily_report_at_hour(raw_data: list, reporting_hour: int) -> pd.DataFrame:
    '''
    This method takes in a list of dictionaries that must include 'timestamp'
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

    # Convert to dataframe, possibly sparse if extra columns/unparsed
    df = pd.DataFrame(raw_data)
    df = df.rename({'timestamp': DATE},axis=1)
    if DATE not in df.columns or PRICE not in df.columns:
        raise RuntimeError('Data does not have required columns in schema')
    
    # convert to datetime and prune unneeded data
    df[DATE] = pd.to_datetime(df[DATE], unit='ms')
    
    # API occasionally returned the "most current" date that was not on the hour,
    # otherwise could do dt.hour == reporting_hour
    df = df[ df[DATE].dt.time == datetime.time(reporting_hour, 0,0,0) ]
    
    # Type casting
    df[PRICE]=df[PRICE].astype(float)
    
    # Could set index to DATE here for faster DATE-based operations in future
    
    # build derived columns and rename columns
    df['change']=df[PRICE].diff()
    df['direction'] = change_to_direction(df['change'])
    df['dayOfWeek'] = df[DATE].dt.day_name()
    df['highSinceStart'] = high_since(df[PRICE])
    df['lowSinceStart'] = low_since(df[PRICE])
    
    if not df[DATE].is_unique:
        raise Warning('Warning, duplicate values for certain dates')    
    return df