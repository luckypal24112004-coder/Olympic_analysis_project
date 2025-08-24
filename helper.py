import numpy as np




def fetch_medal_tally(df, year, country):
    # Remove duplicate medal entries
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'Sport', 'Event', 'Medal', 'City'])

    # Ensure 'Gold', 'Silver', 'Bronze' are created fresh
    medal_df['Gold'] = medal_df['Medal'].apply(lambda x: 1 if x == 'Gold' else 0)
    medal_df['Silver'] = medal_df['Medal'].apply(lambda x: 1 if x == 'Silver' else 0)
    medal_df['Bronze'] = medal_df['Medal'].apply(lambda x: 1 if x == 'Bronze' else 0)

    # Remove duplicate column names if any
    medal_df = medal_df.loc[:, ~medal_df.columns.duplicated()]

    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
        flag = 1
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x




def year_country_list(df):
    years = df['Year'].dropna().unique().tolist()
    years.sort(reverse=True)
    years.insert(0, 'Overall')

    if 'region' in df.columns:
        countries = np.unique(df['region'].dropna().values).tolist()
        countries.sort()
        countries.insert(0, 'Overall')
    else:
        countries = ['Overall']

    return years, countries


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(subset=[col , 'Year'])['Year'].value_counts().reset_index().sort_values(
        'Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)

    return nations_over_time

def successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == 'Athletics']
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']
    merged_df = medal_counts.merge(temp_df[['Name', 'Sport', 'region']].drop_duplicates(), on='Name')
    merged_df = merged_df.sort_values(by='Medals', ascending=False)
    return merged_df

def countrywise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'Sport', 'Event', 'Medal', 'City']
    ).reset_index(drop=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_sport_success(df,country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'Sport', 'Event', 'Medal', 'City']
    ).reset_index(drop=True)
    new_df = temp_df[temp_df['region'] == country]
    pivot = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')

    return pivot


def most_successful_native(df,country):
    temp_df = df.dropna(subset=['Medal'])
    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']
    merged_df = medal_counts.merge(temp_df[['Name', 'Sport']].drop_duplicates(), on='Name')
    merged_df = merged_df.sort_values(by='Medals', ascending=False).head(10)
    return merged_df

def weight_height_analysis(df, sport):
    # Remove duplicate athletes
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Replace missing medals with 'None'
    athlete_df['Medal'] = athlete_df['Medal'].fillna('None')

    # Filter by sport if specified
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    Men = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    Women = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final_df = Men.merge(Women, on='Year', how='left')
    final_df.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final_df.fillna(0, inplace=True)
    return final_df









