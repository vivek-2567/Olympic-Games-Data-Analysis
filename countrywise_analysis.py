def countrywise_analysis(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return temp_df

def countrywise_heatmap(df,country):
    temp_df = df.copy()
    temp_df['Medal'].fillna("No Medal",inplace = True)
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    temp_df = temp_df[temp_df['region'] == country]
    return temp_df


def best_player(df,country):
    # print(df)
    tempo_df = df.dropna(subset=['Medal'])

    tempo_df = tempo_df[tempo_df['region'] == country]
    if tempo_df.empty:
        return tempo_df[['Name','Event']]
    tempo_df = tempo_df['Name'].value_counts().reset_index().head(10)
    tempo_df.rename(columns={'index' : 'Name','Name' : 'Total Medals'},inplace=True)
    tempo_df = tempo_df.merge(df,on = 'Name')
    tempo_df.drop_duplicates(['Name'],inplace = True)
    tempo_df = tempo_df[['Name',"Event","Total Medals"]].reset_index()
    return tempo_df.drop('index',axis = 'columns')