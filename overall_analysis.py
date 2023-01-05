def over_time(df,col,y=0):
    df = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')
    if y:
        df.rename(columns = {'index':'Edition','Year':y},inplace = True)
    else:
        df.rename(columns = {'index':'Edition','Year':col},inplace = True)
    return df


def best_player(df,sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    temp_df = temp_df['Name'].value_counts().reset_index().head(10)
    temp_df.rename(columns={'index' : 'Name','Name' : 'Total Medals'},inplace=True)
    temp_df = temp_df.merge(df,on = 'Name')
    temp_df.drop_duplicates(['Name'],inplace = True)
    temp_df = temp_df[['Name',"Event", "region","Total Medals"]].reset_index()
    return temp_df.drop('index',axis = 'columns')