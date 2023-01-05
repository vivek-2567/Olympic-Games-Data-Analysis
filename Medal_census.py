import pandas as pd
    

def medal_census(df,year,country):
    nos_medal = df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'])
    nos_medal['Total'] = nos_medal['Gold'] + nos_medal['Silver'] + nos_medal['Bronze']

    nos_medal['Gold'] = nos_medal['Gold'].astype('int')
    nos_medal['Silver'] = nos_medal['Silver'].astype('int')
    nos_medal['Bronze'] = nos_medal['Bronze'].astype('int')
    nos_medal['Total'] = nos_medal['Total'].astype('int')
    


    if year == 'Overall' and country == 'Overall':
        title = "Country wise Overall Performance"
        nos_medal = nos_medal.groupby('region').sum()[['Gold','Silver','Bronze','Total']].sort_values('Gold',ascending = False).reset_index()

    elif year != 'Overall' and country == 'Overall':
        title = "Country wise overall Performance"
        nos_medal = nos_medal[nos_medal['Year'] == year]
        nos_medal = nos_medal.groupby('region').sum()[['Gold','Silver','Bronze','Total']].sort_values('Gold',ascending = False).reset_index()

    elif year == 'Overall' and country != 'Overall':
        title = "Yearwise performance of " + country 
        nos_medal = nos_medal[nos_medal['region'] == country]
        nos_medal = nos_medal.groupby('Year').sum()[['Gold','Silver','Bronze','Total']].sort_values('Gold',ascending = False).reset_index()

    else:
        title = "Performance of " + country + " in " + str(year)
        nos_medal = nos_medal[nos_medal['region'] == country]
        nos_medal = nos_medal[nos_medal['Year'] == year]
        nos_medal = nos_medal.groupby('region').sum()[['Gold','Silver','Bronze','Total']].sort_values('Gold',ascending = False).reset_index()


    return title,nos_medal