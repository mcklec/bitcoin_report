# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 20:28:56 2020

@author: Matthew L'Ecuyer
"""

from reports.daily_reports import daily_report_at_hour
from datasources.coinranking import fetch_coinranking_history, coinranking_to_df
import time


'''
Full end to end of generating the report.

    Unit testing could be added to verify that daily_report_at_hour can handle 
unstructured data well, or that it warns/errors out properly when appropriate 
fields aren't provided.

    if column order and date format aren't as important, extra lines could be removed
from this module. If they are critical, that functionality can instead be 
moved down in to daily_report_at_hour.

'''


if __name__ == '__main__':
    URL = 'https://api.coinranking.com/v1/public/coin/1/history/30d'
    OUTPUT_FP = './daily_report_{}.json'.format(int(time.time()))
    
    # build report
    raw_data = fetch_coinranking_history(URL)
    raw_df = coinranking_to_df(raw_data)
    daily_data = daily_report_at_hour(raw_df, reporting_hour=0)
   
    # if exact time format is wanted instead of ISO format. Comment out for ISO format
    daily_data['date'] = daily_data['date'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    # if reordering columns is needed
    column_order= ['date','price','direction','change','dayOfWeek',
                   'highSinceStart','lowSinceStart']
    daily_data = daily_data[column_order]
    # Only write to file if there is data.
    if any(daily_data):
        daily_data.to_json(OUTPUT_FP, orient='records',date_format='iso')
    
