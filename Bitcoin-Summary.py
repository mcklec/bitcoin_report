# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 20:28:56 2020

@author: Matthew L'Ecuyer
"""

from reports.daily_reports import daily_report_at_hour
from datasources.coinranking import fetch_coinranking_history
import time



if __name__ == '__main__':
    URL = 'https://api.coinranking.com/v1/public/coin/1/history/30d'
    OUTPUT_FP = './daily_report_{}.json'.format(int(time.time()))
    
    raw_data = fetch_coinranking_history(URL)
    daily_data = daily_report_at_hour(raw_data, reporting_hour=0)
   
    # if exact time format is wanted instead of ISO format
    #daily_data['timestamp'] = daily_data['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    
    # 

    if any(daily_data):
        daily_data.to_json(OUTPUT_FP, orient='records',date_format='iso')
    
