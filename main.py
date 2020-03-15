"""
NETID: phil1999
Philip Lee
Section AA

This file contains all the necessary methods to recreate all the plots
for the Coronavirus analysis project. Simply run this file according to the
reproduction section of the report and it will recreate all the plots.
"""
# Colors
ded = '#ff0000' # deaths - red
rec = '#33CC00' # recovered - green
act = '#FFD300' # active case - cyber yellow
# Analysis
import pandas as pd
# Plotting
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots

confirmed = 'CSE163final/datasets/time_series_19-covid-Confirmed.csv'
recovered = 'CSE163final/datasets/time_series_19-covid-Recovered.csv'
deaths = 'CSE163final/datasets/time_series_19-covid-Deaths.csv'


def load_data(file):
    """
    Takes in a filename and converts it into a dataframe
    using pandas. If file isn't found notifies the user.
    """
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print("Invalid path given:", file, end='')
    else:
        return df


def clean_data():
    """
    Cleans the confirmed, deaths, and recovered datasets taken from
    https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
    and writes the resulting dataset as a csv file named 'covid-19-cleaned.csv'.
    """
    # Cleaning/manipulating the datasets
    c_df = load_data(confirmed)
    r_df = load_data(recovered)
    d_df = load_data(deaths)
    dates = c_df.columns[4:]
    # We now want to melt the dates from each df to a wide format to a
    # long format so that we can look at each date together.
    c_df_long = c_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Confirmed')
    r_df_long = r_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                            value_vars=dates, var_name='Date', value_name='Recovered')
    d_df_long = d_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                            value_vars=dates, var_name='Date', value_name='Deaths')
    # Now all we need to do is combine everything together.
    clean_data = pd.concat([c_df_long, d_df_long['Deaths'], r_df_long['Recovered']],
     axis=1, sort=False)
    # also need to clear county level data to avoid double counts
    clean_data = clean_data[clean_data['Province/State'].str.contains(',')!=True]
    # Replace Mainland China with just China
    clean_data['Country/Region'] = clean_data['Country/Region'].replace('Mainland China',
    'China')
    clean_data['Country/Region'] = clean_data['Country/Region'].replace('US',
    'USA')
    # Fill missing values
    clean_data[['Province/State']] = clean_data[['Province/State']].fillna('')
    clean_data[['Confirmed', 'Deaths', 'Recovered']] = \
    clean_data[['Confirmed', 'Deaths', 'Recovered']].fillna(0)
    # Create active column
    clean_data['Active'] = clean_data['Confirmed'] - clean_data['Deaths'] \
     - clean_data['Recovered']
    clean_data['Active'].fillna(0)
    # Create as a new csv
    clean_data.to_csv('CSE163final/covid-19-cleaned.csv', index=False)


def plot_spread(df):
    """
    Takes in the dataframe and creates a plot showing the spread of Coronavirus.
    """
    temp = df.groupby('Date')['Recovered', 'Deaths', 'Active'].sum().reset_index()
    temp = temp.melt(id_vars="Date", value_vars=['Recovered', 'Deaths', 'Active'],
                 var_name='Case', value_name='Count')
    plot = px.area(temp, x='Date', y='Count', color='Case',
                    title='Number cases over time',
                    color_discrete_sequence = [rec, ded, act])
    plot.show()


def plot_status(df):
    """
    Takes in the dataframe and creates a choropleth showing areas infected with
    Coronavirus.
    """
    # Grab the latest data from the most recent date and group
    latest_data = df[df['Date'] == max(df['Date'])].reset_index()
    latest_data_agg = \
        latest_data.groupby('Country/Region')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
    data = latest_data_agg
    # Plot the data on a choropleth
    plot = px.choropleth(data, locations="Country/Region", 
                    locationmode='country names', color="Confirmed", 
                    hover_name="Country/Region", range_color=[1,2500], 
                    color_continuous_scale="Blues", 
                    title='Countries with Confirmed Cases', 
                    )
    plot.update(layout_coloraxis_showscale=False)
    plot.show()


def plot_china(df):
    """
    Uses the dataframe and plots the current status of China by 
    Province on horizontal bar graphs.
    """
    # Manipulates data to get what we want
    latest_data = df[df['Date'] == max(df['Date'])].reset_index()
    china_latest = latest_data[latest_data['Country/Region']=='China']
    china_latest_grouped = \
        china_latest.groupby('Province/State')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
    data = \
        china_latest_grouped.sort_values('Confirmed', ascending=False).head(20).sort_values('Confirmed', ascending=True)
    # Plot the # confirmed cases by Province
    plot1 = px.bar(data, 
             x="Confirmed", y="Province/State", title='Top 20 Confirmed Cases in China', text='Confirmed', orientation='h', 
             width=700, height=700, range_x = [0, max(data['Confirmed'])+10000])
    plot1.update_traces(marker_color='#add8e6', textposition='outside')
    plot1.show()
    # Plot the # active cases
    plot2 = px.bar(data, 
             x="Active", y="Province/State", title='Top 20 Active Cases in China', text='Active', orientation='h', 
             width=700, height=700, range_x = [0, max(data['Active'])+5000])
    plot2.update_traces(marker_color=act, textposition='outside')
    plot2.show()
    # Plot death cases
    plot3 = px.bar(data, 
             x="Deaths", y="Province/State", title='Top 20 Deaths from Covid-19 in China',
              text='Deaths', orientation='h', 
            width=700, height=700, range_x = [0, max(data['Deaths'])+500])
    plot3.update_traces(marker_color=ded, textposition='outside')
    plot3.show()
    # Plot Recovered cases
    plot4 = px.bar(data, x="Recovered", y="Province/State",
             title='Top 20 Recovered from Covid-19 in China',
              text='Recovered', orientation='h', width=700,
            height=700, range_x=[0, max(data['Recovered'])+10000])
    plot4.update_traces(marker_color=rec, textposition='outside')
    plot4.show()


def main():
    clean_data()
    df_parsed = \
        pd.read_csv('CSE163final/covid-19-cleaned.csv', parse_dates=['Date'])
    plot_spread(df_parsed)
    plot_status(df_parsed)
    plot_china(df_parsed)


if __name__ == '__main__':
    main()
