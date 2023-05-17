import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_worldbank_file(filename):
    """
    Read the Worldbank format file using pandas.

    Args:
        filename (str): Path to the data file.

    Returns:
        tuple: Two dataframes - df_years and df_countries.
    """
    df_years = pd.read_csv(filename, skiprows=4)

    df_years = df_years.fillna(0)
    df_years = df_years.drop(['Country Code', 'Indicator Code'], axis=1)

    df_countries = df_years.transpose()
    return df_years, df_countries

df_years, df_countries = read_worldbank_file('API_19_DS2_en_csv_v2_5346672.csv')

df_countries.describe()
df_years.describe()

indicators = df_years['Indicator Name'].unique()
len(indicators)

countries = df_years['Country Name'].unique()
len(countries)

def get_factors(data, indicator_name):
    """
    Get factors for selected countries and a specific indicator.

    Args:
        data (pd.DataFrame): Input dataframe.
        indicator_name (str): Name of the indicator.

    Returns:
        pd.DataFrame: Filtered dataframe with factors.
    """
    countries = [
        'Finland', 'Poland', 'United Kingdom', 'Pakistan', 'India',
        'New Zealand', 'Turkiye', 'South Africa', 'China', 'United States'
    ]
    df_data = data[data['Indicator Name'] == indicator_name]

    result = df_data[df_data['Country Name'].isin(countries)]
    result = result.drop(['Indicator Name'], axis=1)
    result = result.loc[:, ['Country Name', '1980', '1990', '2000', '2010', '2020']]
    
    return result

ub_population = get_factors(df_years, 'Urban population')
elec_power = get_factors(df_years, 'Electric power consumption (kWh per capita)')
energy = get_factors(df_years, 'Energy use (kg of oil equivalent per capita)')
co2 = get_factors(df_years, 'CO2 emissions (kg per PPP $ of GDP)')

def plot_bar_graph(data, title, filename):
    """
    Plot a bar graph from the given data.

    Args:
        data (pd.DataFrame): Input dataframe.
        title (str): Title of the graph.
        filename (str): Output filename.
    """
    data.plot.bar(x="Country Name", title=title, figsize=(20, 10))
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

def plot_line_graph(data, title, filename):
    """
    Plot a line graph from the given data.

    Args:
        data (pd.DataFrame): Input dataframe.
        title (str): Title of the graph.
        filename (str): Output filename.
    """
    data.plot(x="Country Name", title=title, figsize=(20, 10))
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

def plot_scatter_graph(data, x_column, y_column, title, filename):
    """
    Plot a scatter graph from the given data.

    Args:
        data (pd.DataFrame): Input dataframe.
        x_column (str): Name of the column to be plotted on the x-axis.
        y_column (str): Name of the column to be plotted on the y-axis.
        title (str): Title of the graph.
        filename (str): Output filename.
    """
    data.plot.scatter(x=x_column, y=y_column, title=title, figsize=(20, 10))
    plt.savefig(filename, bbox_inches='tight')
    plt.show()


plot_line_graph(elec_power,'Electric power consumption (kWh per capita)','Line Plot elec_power.jpg')

plot_line_graph(ub_population,'Urban population in last 50 year','Line Plot Urban_population.jpg')
 
plot_bar_graph(ub_population,'Urban population in last 50 year','Bar Graph Urban_population.jpg')
plot_bar_graph(elec_power,'Electric power consumption (kWh per capita)','Bar Graph elec_power.jpg')


plot_bar_graph(energy,'Energy use (kg of oil equivalent per capita)','Bar Graph energy.jpg')
plot_scatter_graph(ub_population, 'Country Name', '2010', 'Urban population in last 50 years', 'Bar Graph Urban_population.jpg')

plot_scatter_graph(energy, 'Country Name', '2010', 'Energy use (kg of oil equivalent per capita)', 'Scatter plot Energy consumption.jpg')

def heat_map(data):
    """
    Create a heatmap based on the given data.

    Args:
        data (pd.DataFrame): Input dataframe.
    """
    # List of selected countries
    country_hm = [
        'Finland', 'Poland', 'United Kingdom', 'Pakistan', 'India',
        'New Zealand', 'Turkiye', 'South Africa', 'China', 'United States'
    ]
    result_hm = data[data['Country Name'].isin(country_hm)]
    result_hm = result_hm.loc[:, ['Country Name', 'Indicator Name', '2010']]

    # List of selected indicators
    selected_values = [
        'Urban population',
        'Electric power consumption (kWh per capita)',
        'Energy use (kg of oil equivalent per capita)',
        'CO2 emissions (kg per PPP $ of GDP)'
    ]
    result_hm = result_hm[result_hm['Indicator Name'].isin(selected_values)]

    # Creating pivot table for heatmap
    temp_df = result_hm.pivot(index='Country Name', columns='Indicator Name', values='2010')

    # Create a heatmap
    sns.heatmap(temp_df, annot=True, fmt=".1f")
    plt.savefig('heatmap.jpg')
    plt.show()

heat_map(df_years)
