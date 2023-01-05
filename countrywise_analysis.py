def countrywise_analysis(df,country):
    df = df.dropna(subset=['Medal'])
    df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    df = df[df['region'] == country]
    df = df.groupby('Year').count()['Medal'].reset_index()
    return df

def countrywise_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    temp_df = temp_df[temp_df['region'] == country]
    return temp_df


def best_player(df,country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]
    
    temp_df = temp_df['Name'].value_counts().reset_index().head(10)
    temp_df.rename(columns={'index' : 'Name','Name' : 'Total Medals'},inplace=True)
    temp_df = temp_df.merge(df,on = 'Name')
    temp_df.drop_duplicates(['Name'],inplace = True)
    temp_df = temp_df[['Name',"Event","Total Medals"]].reset_index()
    return temp_df.drop('index',axis = 'columns')