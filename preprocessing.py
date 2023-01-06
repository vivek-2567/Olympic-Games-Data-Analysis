import pandas as pd

def s_initial_load():
    events = pd.read_csv("athlete_events.csv")
    regions = pd.read_csv("noc_regions.csv")
    events = events[events['Season'] == "Summer"]
    events = events.merge(regions,on='NOC',how='left')
    events.drop_duplicates(inplace=True)
    events = pd.concat([events,pd.get_dummies(events['Medal'])], axis='columns')
    return events

def w_initial_load():
    events = pd.read_csv("athlete_events.csv")
    regions = pd.read_csv("noc_regions.csv")
    events = events[events['Season'] == "Winter"]
    events = events.merge(regions,on='NOC',how='left')
    events.drop_duplicates(inplace=True)
    events = pd.concat([events,pd.get_dummies(events['Medal'])], axis='columns')
    return events