import streamlit as st
import pandas as pd
import preprocessor, helper
from helper import year_country_list
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

# 🔄 Load preprocessed DataFrame with 'region' column
df = preprocessor.preprocess()

# 🎯 Sidebar menu
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# 🏅 Title
st.sidebar.title('Olympic Analysis')

# 🥇 Medal Tally Section
if user_menu == 'Medal Tally':
    year, country = year_country_list(df)

    selected_year = st.sidebar.selectbox('Year', year)
    selected_country = st.sidebar.selectbox('Country', country)

    medal_tally_data = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall' :
        st.title('Overall Medal Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall' :
        st.title('Medal Tally in ' + str(selected_year))
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s performance every year")
    else :
        st.title(selected_country + "'s performance in " + str(selected_year))
    st.table(medal_tally_data)


if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() - 1  # Remove -1 if not needed
    city = df['City'].nunique()
    region = df['region'].nunique()
    event = df['Event'].nunique()
    players = df['Name'].nunique()
    sport = df['Sport'].nunique()

    st.title('Top Statistics')

    # First row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('Hosts')
        st.title(city)

    with col3:
        st.header('Nations')
        st.title(region)

    # Second row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Event')
        st.title(event)

    with col2:
        st.header('Athletes')
        st.title(players)

    with col3:
        st.header('Sports')
        st.title(sport)

    st.title('Participating nations over time')
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')

    st.plotly_chart(fig)

    st.title('Events over time')
    nations_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(nations_over_time, x='Edition', y='Event')

    st.plotly_chart(fig)

    st.title('No. of events over the years(each sport)')
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(subset=['Year', 'Event', 'Sport'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)

    st.pyplot(fig)

    st.title('Most successful athletes of every sport')

    # Get unique sports
    sports = df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0, 'Overall')  # Add 'Overall' option

    # Dropdown to select sport
    selected_sport = st.selectbox('Select a Sport', sports)

    # Call helper function
    x = helper.successful(df, selected_sport)

    # Display table
    st.table(x)


if user_menu == 'Country-wise Analysis' :
    countries = (df['region'].dropna().unique().tolist())
    countries.sort()
    selected_country = st.sidebar.selectbox('Select a Country',countries)
    st.title(selected_country + " Medal Tally over the years")
    nations_over_time = helper.countrywise_medal_tally(df, selected_country)
    fig = px.line(nations_over_time, x='Year', y='Medal')

    st.plotly_chart(fig)

    st.title(selected_country +" excel in the following sports")
    pt =helper.country_sport_success(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Top 10 athletes of ' + selected_country)
    top10 = helper.most_successful_native(df,selected_country)
    st.table(top10)


if user_menu == 'Athlete-wise Analysis' :
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], group_labels=['Overall distribution', 'Gold Medalist', 'Silver Medalist',
                                                             'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.title('Distribution of Age')

    st.plotly_chart(fig)

    famous = ['Tug-Of-War', 'Swimming', 'Gymnastics', 'Handball', 'Hockey',
              'Rowing', 'Football', 'Sailing', 'Cycling', 'Fencing', 'Taekwondo',
              'Athletics', 'Canoeing', 'Water Polo', 'Wrestling',
               'Golf', 'Softball', 'Boxing', 'Basketball',
              'Diving', 'Baseball', 'Volleyball', 'Shooting', 'Judo',
               'Tennis', 'Rugby Sevens', 'Rhythmic Gymnastics',
              'Weightlifting', 'Badminton', 'Beach Volleyball', 'Rugby',
               'Synchronized Swimming', 'Archery', 'Triathlon',
              'Polo', 'Table Tennis',
              'Art Competitions', 'Ice Hockey']
    x = []
    y = []
    for sport in famous:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        y.append(sport)

    fig = ff.create_distplot(x, y, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Age Distribution of Gold Medalists by Sport')
    st.plotly_chart(fig)

# Get unique sports
    sports = df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0, 'Overall')  # Add 'Overall' option

    st.title('Height vs Weight')

    # Dropdown to select sport
    selected_sport = st.selectbox('Select a Sport', sports)

    temp_df = helper.weight_height_analysis(df,selected_sport)

    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Height'], y=temp_df['Weight'], hue = temp_df['Medal'], style = temp_df['Sex'],s = 60)

    st.pyplot(fig)

    st.title('Men vs Women participation over the years')

    final_df = helper.men_vs_women(df)
    fig = fig = px.line(final_df,x = 'Year', y = ['Male','Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)







