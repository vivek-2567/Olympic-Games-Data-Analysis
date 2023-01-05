def athelete_age(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    return x1,x2,x3,x4


def age_sports(df,medal):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x = []
    name = []
    sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
    'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
    'Water Polo', 'Hockey', 'Rowing', 'Fencing',
    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
    'Tennis', 'Golf', 'Softball', 'Archery',
    'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
    'Rhythmic Gymnastics', 'Rugby Sevens',
    'Beach Volleyball', 'Triathlon', 'Polo', 'Ice Hockey']

    for sport in sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == medal]['Age'].dropna())
        name.append(sport)


    return x,name

def height_weight_scatter(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna("No Medal",inplace = True)
    if sport != 'Overall':
        return athlete_df[athlete_df['Sport'] == sport]
    return athlete_df
        
def male_vs_female(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    plot_df = men.merge(women,on = 'Year',how = 'left')
    plot_df.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace = True)
    plot_df.fillna(0,inplace = True)
    return plot_df