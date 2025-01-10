import pandas as pd
from datetime import datetime, timedelta


df = pd.read_csv("data/token_data.csv")


def convert_age_to_datetime(age_str, query_time):
    hours = 0
    minutes = 0
    
    if 'd' in age_str:
        hours = 25
    elif 'h' in age_str:
        hours = int(age_str.split('h')[0])
        rest = age_str.split('h')[1].strip()
        if 'm' in rest:
            minutes = int(rest.split('m')[0])
    elif 'm' in age_str:
        minutes = int(age_str.split('m')[0])
    
    time_delta = timedelta(hours=hours, minutes=minutes)
    return query_time - time_delta

def convert_currency(cap):
    if "K" in cap:
        cap = cap.replace("K", "")
        cap = float(cap)/1000
        
    elif "B" in cap:
        cap = cap.replace("B", "")
        cap = float(cap)*1000
    
    else:
        cap = cap.replace("M", "")
        cap = float(cap)
        
    return cap

def apply_first_filter(df, query_time):
    """
    - trong 24h 
    - marketcap > 1m

    Args:
        df (_type_): _description_
    """
    # Filter by timestamp
    df['timestamp'] = df['Age'].apply(lambda x: convert_age_to_datetime(x, query_time))
    # Filter entries less than 24h old
    cutoff_time = query_time - timedelta(hours=24)
    filtered_df = df[df['timestamp'] > cutoff_time]
    filtered_df = filtered_df.drop('timestamp', axis=1)
    #filter by marketcap
    filtered_df["FDV"] = filtered_df['FDV'].apply(lambda x: convert_currency(x))
    filtered_df = filtered_df[filtered_df['FDV'] > 1]
    print("Filtered ", filtered_df)
    
    
query_time = datetime.now()
apply_first_filter(df, query_time)

