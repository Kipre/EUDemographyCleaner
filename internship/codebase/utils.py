import numpy as np
import pandas as pd
from itertools import combinations_with_replacement
from tabulate import tabulate
from IPython.display import display, Markdown, Latex


def reduce(expression, terms):
    exponents = [0]*len(terms)
    for i, k in enumerate(terms):
        for e in expression:
            if k == e:
                exponents[i] += 1
    result = '$'
    for i, exp in enumerate(exponents[1:]):
        if exp == 1:
            result += f' {terms[i + 1]}'
        elif exp > 1:
            result += f' {terms[i + 1]}^{exp}'
    if result == '$':
        result = '$1$'
    else:
        result += '$'
    return result

def make_polynomials(data, max_degree=3):
    """Returns the augmented array and the number of transformations"""
    def handle_row(example):
        row = []
        # making an array with [1, x, y, ...]
        example = np.concatenate(([1], example.reshape((nb_variables))))
        for indexes in combinations_with_replacement(range(nb_variables + 1), max_degree):
            product = np.take(example, indexes).prod()
            row.append(product)
        return row

    if len(data.shape) == 2:
        nb_variables = data.shape[1]
        result = []
        for example in data:
            result.append(handle_row(example))
        return np.array(result, dtype=np.float32), len(result[-1])
    elif len(data.shape) == 1:
        nb_variables = data.shape[0]
        result = handle_row(data)
        return np.array(result, dtype=np.float32), len(result)
    else:
        raise Exception('Shape not understood')

def make_targets(data, derivative=False, timestep=1, threshold=-1, listed=False):
    """Returns 2 matrices: derivatires or m2 and m1"""
    derivatives, m2, m1 = [], [], []

    def separate(scenario):
        if len(scenario) != 0:
            gradients = np.gradient(scenario, axis=0)
            for i, grad in enumerate(gradients[1:-1]):
                if (abs(scenario[i+1]) > threshold).any():
                    derivatives.append(grad)
                    m2.append(scenario[i+2])
                    m1.append(scenario[i+1])

    if len(data.shape) == 3 or listed:
        for scenario in data:
            separate(scenario)
    elif len(data.shape) == 2:
        separate(data)
    elif len(data.shape) == 2:
        separate(data.reshape(-1, 1))
    if derivative:
        return np.array(derivatives, dtype=np.float32)/timestep, np.array(m1, dtype=np.float32)
    else:
        return np.array(m2, dtype=np.float32), np.array(m1, dtype=np.float32)



def show_weights(weights, derivative=False, variables=None, max_degree=6, raw=False, warn=True, pde=False):
    if not pde:
        nb_variables = weights.shape[1]
        if not variables:
            variables = ['1', 'x', 'y', 'z']
    else:
        nb_variables = weights.shape[0]
        if not variables:
            variables = ['1', 'u', 'u_x', 'u_{xx}', 'u_{xxx}'][:min(pde + 2, 5)]
    params = [[reduce(name, variables)] + list(val)
              for name, val in zip(combinations_with_replacement(variables[:1 + nb_variables], max_degree), weights.numpy())]
    headers = ['function'] + ['$\dot{' + str(var) + '}$' if derivative else '$' + str(var) + '_{k+1}$'
                              for var in variables[1:1 + nb_variables]]
    if raw:
        print(tabulate(params, headers=headers, tablefmt="pipe"))
    else:
        display(Markdown(tabulate(params, headers=headers, tablefmt="pipe")))

def find_degree(N, n):
    """very inefficient way for finding the max degree"""
    for max_degree in range(1, 10):
        if N == len(list(combinations_with_replacement('a'*n, max_degree))):
            return max_degree
    raise Exception("Couldn't find a max degree between 1 and 10")

class CountryDataset:

    iso = {'Aruba': 'ABW', 'Czechia': 'CZE', 'Canada': 'CAN', 'Australia': 'AUS', 'US': 'USA', 'Korea, South': 'KOR', 'Belgium': 'BEL', 'Switzerland': 'CHE', 'Austria':'AUT', 'Afgé': 'CPV', 'Costa Rica': 'CRI', 'China':'CHN', 'Cuba': 'CUB', 'Cyprus': 'CYP', 'Czech Republic': 'CZE', 'Germany': 'DEU', 'Djibouti': 'DJI', 'Dominica': 'DMA', 'Denmark': 'DNK', 'Dominican Republic': 'DOM', 'Algeria': 'DZA', 'Ecuador': 'ECU', 'Egypt': 'EGY', 'Spain': 'ESP', 'Estonia': 'EST', 'Ethiopia': 'ETH', 'Finland': 'FIN', 'France': 'FRA', 'Gabon': 'GAB', 'United Kingdom': 'GBR', 'Ghana': 'GHA', 'Gambia': 'GMB', 'Greece': 'GRC', 'Greenland': 'GRL', 'Guatemala': 'GTM', 'Guam': 'GUM', 'Guyana': 'GUY', 'Hong Kong': 'HKG', 'Honduras': 'HND', 'Croatia': 'HRV', 'Hungary': 'HUN', 'Indonesia': 'IDN', 'India': 'IND', 'Ireland': 'IRL', 'Iran': 'IRN', 'Iraq': 'IRQ', 'Iceland': 'ISL', 'Israel': 'ISR', 'Italy': 'ITA', 'Jamaica': 'JAM', 'Jordan': 'JOR', 'Japan': 'JPN', 'Kazakhstan': 'KAZ', 'Kenya': 'KEN', 'Kyrgyz Republic': 'KGZ', 'South Korea': 'KOR', 'Kuwait': 'KWT', 'Laos': 'LAO', 'Lebanon': 'LBN', 'Libya': 'LBY', 'Sri Lanka': 'LKA', 'Lesotho': 'LSO', 'Luxembourg': 'LUX', 'Macao': 'MAC', 'Morocco': 'MAR', 'Moldova': 'MDA', 'Madagascar': 'MDG', 'Mexico': 'MEX', 'Mali': 'MLI', 'Myanmar': 'MMR', 'Mongolia': 'MNG', 'Mozambique': 'MOZ', 'Mauritania': 'MRT', 'Mauritius': 'MUS', 'Malawi': 'MWI', 'Malaysia': 'MYS', 'Namibia': 'NAM', 'Niger': 'NER', 'Nigeria': 'NGA', 'Nicaragua': 'NIC', 'Netherlands': 'NLD', 'Norway': 'NOR', 'New Zealand': 'NZL', 'Oman': 'OMN', 'Pakistan': 'PAK', 'Panama': 'PAN', 'Peru': 'PER', 'Philippines': 'PHL', 'Papua New Guinea': 'PNG', 'Poland': 'POL', 'Puerto Rico': 'PRI', 'Portugal': 'PRT', 'Paraguay': 'PRY', 'Palestine': 'PSE', 'Qatar': 'QAT', 'Romania': 'ROU', 'Russia': 'RUS', 'Rwanda': 'RWA', 'Saudi Arabia': 'SAU', 'Sudan': 'SDN', 'Singapore': 'SGP', 'Sierra Leone': 'SLE', 'El Salvador': 'SLV', 'San Marino': 'SMR', 'Serbia': 'SRB', 'South Sudan': 'SSD', 'Slovak Republic': 'SVK', 'Slovenia': 'SVN', 'Sweden': 'SWE', 'Eswatini': 'SWZ', 'Seychelles': 'SYC', 'Syria': 'SYR', 'Chad': 'TCD', 'Thailand': 'THA', 'Trinidad and Tobago': 'TTO', 'Tunisia': 'TUN', 'Turkey': 'TUR', 'Taiwan': 'TWN', 'Tanzania': 'TZA', 'Uganda': 'UGA', 'Ukraine': 'UKR', 'Uruguay': 'URY', 'United States': 'USA', 'Uzbekistan': 'UZB', 'Venezuela': 'VEN', 'Vietnam': 'VNM', 'South Africa': 'ZAF', 'Zambia': 'ZMB', 'Zimbabwe': 'ZWE'}

    def __init__(self, 
                 oxford_url = 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv',
                 hopkins_cases_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
                 hopkins_recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
                 indicators_path = 'indicators.csv'):
        self.oxford = pd.read_csv(oxford_url, parse_dates=['Date'])
        self.hopkins_cases = pd.read_csv(hopkins_cases_url)
        self.hopkins_recovered = pd.read_csv(hopkins_recovered_url)
        self.indicators = pd.read_csv(indicators_path).set_index('Country', drop=True)

    def get_sir(self, country, rescaling=1):
        recovered = self.hopkins_recovered[self.hopkins_recovered['Country/Region'] == country].sum().iloc[4:]
        recovered = np.array(recovered, dtype=np.int64)/rescaling
        cumulative = self.get_cumulative(country, rescaling)

        total_population = np.full_like(cumulative, self.indicators.loc[self.iso[country], 'SP.POP.TOTL'])/rescaling
        infected = cumulative - recovered
        susceptible = total_population - cumulative
        result = np.concatenate([susceptible.reshape(-1, 1), 
                                 infected.reshape(-1, 1), 
                                 recovered.reshape(-1, 1)],
                                 axis=1)
        return result

    def get_cumulative(self, country, rescaling=1):
        cumulative = self.hopkins_cases[self.hopkins_cases['Country/Region'] == country].sum().iloc[4:]
        return np.array(cumulative, dtype=np.int64)/rescaling

    def all_hopkins_countries(self, cases_cap=np.inf):
        return list(self.hopkins_cases['Country/Region'].unique())
        


