# -*- coding: utf-8 -*-

import requests

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
