# -*- coding: utf-8 -*-

import requests

import pandas as pd
from helpers.constants import DATE, PRICE, TIME


def fetch_coinranking_history(url: str) -> dict:
    '''
    This function takes a URL as an argument, makes a request to the URL for the JSON
    representation of its data, and returns the data as a list of dictionaries,
    representing the JSON.
    
    params:
        url (str): the URL to request data from    
    
    '''
    # requests handles URL checking, no need to         
    raw_data = requests.get(url).json() or {}
    
    history = raw_data.get('data').get('history')
    if not history:
        raise Warning('Warning, no coin history found at {}, or encountered unexpected schema'.format(url) )    
    
    return history


def coinranking_to_df(raw_data: list) -> pd.DataFrame:
    '''
    This method takes in a list of dictionaries that must include 'timestamp'
    and 'price' within their schema, and returns a dataframe with [price]
    
    params:
        raw_data (list): a list of dictionaries containing at least "date" 
                            and "timestamp" columns
                            
    returns:
        a pandas dataframe renaming "timestamp" to "date" and leaving the rest
        of the data untouched
    '''
     # Convert to dataframe, possibly sparse if extra columns/unparsed
    df = pd.DataFrame(raw_data)
    if TIME not in df.columns or PRICE not in df.columns:
        raise RuntimeError('Data does not have required columns in schema')
        
    df = df.rename({TIME: DATE},axis=1)
    

    
    # Type casting
    df[DATE] = pd.to_datetime(df[DATE], unit='ms')   
    df[PRICE]=df[PRICE].astype(float)
    # Could set index to DATE here for faster time-based operations in future

    return df