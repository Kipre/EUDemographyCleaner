import numpy as np
import pandas as pd
from itertools import combinations_with_replacement
from tabulate import tabulate
from IPython.display import display, Markdown, Latex
import pycountry


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
            nb_variables = len(variables)
            variables = ['1'] + variables
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

def make_targets_df(data, time_column='Date', category_column='CountryCode'):
    data = data.sort_values([category_column, time_column]).copy()
    first_date = data.drop_duplicates(category_column)
    last_date = data.drop_duplicates(category_column, keep='last')
    m2, m1 = data.drop(first_date.index).copy(), data.drop(last_date.index).copy()
    return m2.reset_index(drop=True), m1.reset_index(drop=True)

def make_polynomials_df(data, variables, predicted_variables, time_dependent_variables=None, max_degree=2):
    """Returns the augmented array and the number of transformations"""
    variables = ['1'] + list(variables)
    
    def sparse_list(count):
        return [1]*count + [np.nan]*(max_degree - count)
    
    if '1' not in data.columns:
        data['1'] = 1
    result = pd.DataFrame()
    integration_args = {"constant_variables": [], "sparse_filters": []}
    if not time_dependent_variables:
        time_dependent_variables = predicted_variables
    for columns in combinations_with_replacement(variables, max_degree):
        if not set(predicted_variables).isdisjoint(columns):
            result['*'.join(columns)] = data.loc[:, columns].prod(axis=1, numeric_only=True)
            integration_args['constant_variables'].append([col for col in columns if col not in time_dependent_variables + ['1']])
            integration_args['sparse_filters'].append(sum([sparse_list(columns.count(col)) for col in time_dependent_variables], []))
    integration_args['sparse_filters'] = np.array(integration_args['sparse_filters'])
    return result, integration_args

class CountryDataset:

    iso = {'Afghanistan': 'AFG', 'Albania': 'ALB', 'Algeria': 'DZA', 'Andorra': 'AND', 'Angola': 'AGO', 'Antigua and Barbuda': 'ATG', 'Argentina': 'ARG', 'Armenia': 'ARM', 'Australia': 'AUS', 'Austria': 'AUT', 'Azerbaijan': 'AZE', 'Bahamas': 'BHS', 'Bahrain': 'BHR', 'Bangladesh': 'BGD', 'Barbados': 'BRB', 'Belarus': 'BLR', 'Belgium': 'BEL', 'Belize': 'BLZ', 'Benin': 'BEN', 'Bhutan': 'BTN', 'Bolivia': 'BOL', 'Bosnia and Herzegovina': 'BIH', 'Botswana': 'BWA', 'Brazil': 'BRA', 'Brunei': 'BRN', 'Bulgaria': 'BGR', 'Burkina Faso': 'BFA', 'Burma': 'MMR', 'Burundi': 'BDI', 'Cabo Verde': 'CPV', 'Cambodia': 'KHM', 'Cameroon': 'CMR', 'Canada': 'CAN', 'Central African Republic': 'CAF', 'Chad': 'TCD', 'Chile': 'CHL', 'China': 'CHN', 'Colombia': 'COL', 'Comoros': 'COM', 'Costa Rica': 'CRI', "Cote d'Ivoire": 'CIV', 'Croatia': 'HRV', 'Cuba': 'CUB', 'Cyprus': 'CYP', 'Denmark': 'DNK', 'Djibouti': 'DJI', 'Dominica': 'DMA', 'Dominican Republic': 'DOM', 'Ecuador': 'ECU', 'Egypt': 'EGY', 'El Salvador': 'SLV', 'Equatorial Guinea': 'GNQ', 'Eritrea': 'ERI', 'Estonia': 'EST', 'Eswatini': 'SWZ', 'Ethiopia': 'ETH', 'Fiji': 'FJI', 'Finland': 'FIN', 'France': 'FRA', 'Gabon': 'GAB', 'Gambia': 'GMB', 'Georgia': 'GEO', 'Germany': 'DEU', 'Ghana': 'GHA', 'Greece': 'GRC', 'Grenada': 'GRD', 'Guatemala': 'GTM', 'Guinea': 'GNQ', 'Guinea-Bissau': 'GNB', 'Guyana': 'GUY', 'Haiti': 'HTI', 'Holy See': 'VAT', 'Honduras': 'HND', 'Hungary': 'HUN', 'Iceland': 'ISL', 'India': 'IOT', 'Indonesia': 'IDN', 'Iran': 'IRN', 'Iraq': 'IRQ', 'Ireland': 'IRL', 'Israel': 'ISR', 'Italy': 'ITA', 'Jamaica': 'JAM', 'Japan': 'JPN', 'Jordan': 'JOR', 'Kazakhstan': 'KAZ', 'Kenya': 'KEN', 'Kosovo': 'KOS', 'Kuwait': 'KWT', 'Kyrgyzstan': 'KGZ', 'Laos': 'LAO', 'Latvia': 'LVA', 'Lebanon': 'LBN', 'Lesotho': 'LSO', 'Liberia': 'LBR', 'Libya': 'LBY', 'Liechtenstein': 'LIE', 'Lithuania': 'LTU', 'Luxembourg': 'LUX', 'Madagascar': 'MDG', 'Malawi': 'MWI', 'Malaysia': 'MYS', 'Maldives': 'MDV', 'Mali': 'MLI', 'Malta': 'MLT', 'Mauritania': 'MRT', 'Mauritius': 'MUS', 'Mexico': 'MEX', 'Moldova': 'MDA', 'Monaco': 'MCO', 'Mongolia': 'MNG', 'Montenegro': 'MNE', 'Morocco': 'MAR', 'Mozambique': 'MOZ', 'Namibia': 'NAM', 'Nepal': 'NPL', 'Netherlands': 'NLD', 'New Zealand': 'NZL', 'Nicaragua': 'NIC', 'Niger': 'NER', 'Nigeria': 'NGA', 'Norway': 'NOR', 'Oman': 'OMN', 'Pakistan': 'PAK', 'Panama': 'PAN', 'Papua New Guinea': 'PNG', 'Paraguay': 'PRY', 'Peru': 'PER', 'Philippines': 'PHL', 'Poland': 'POL', 'Portugal': 'PRT', 'Qatar': 'QAT', 'Romania': 'ROU', 'Russia': 'RUS', 'Rwanda': 'RWA', 'Saint Kitts and Nevis': 'KNA', 'Saint Lucia': 'LCA', 'Saint Vincent and the Grenadines': 'VCT', 'San Marino': 'SMR', 'Sao Tome and Principe': 'STP', 'Saudi Arabia': 'SAU', 'Senegal': 'SEN', 'Serbia': 'SRB', 'Seychelles': 'SYC', 'Sierra Leone': 'SLE', 'Singapore': 'SGP', 'Slovakia': 'SVK', 'Slovenia': 'SVN', 'Somalia': 'SOM', 'South Africa': 'ZAF', 'South Sudan': 'SSD', 'Spain': 'ESP', 'Sri Lanka': 'LKA', 'Sudan': 'SSD', 'Suriname': 'SUR', 'Sweden': 'SWE', 'Switzerland': 'CHE', 'Syria': 'SYR', 'Tajikistan': 'TJK', 'Tanzania': 'TZA', 'Thailand': 'THA', 'Timor-Leste': 'TLS', 'Togo': 'TGO', 'Trinidad and Tobago': 'TTO', 'Tunisia': 'TUN', 'Turkey': 'TUR', 'US': 'AUS', 'Uganda': 'UGA', 'Ukraine': 'UKR', 'United Arab Emirates': 'ARE', 'United Kingdom': 'GBR', 'Uruguay': 'URY', 'Uzbekistan': 'UZB', 'Venezuela': 'VEN', 'Vietnam': 'VNM', 'Western Sahara': 'ESH', 'Yemen': 'YEM', 'Zambia': 'ZMB', 'Zimbabwe': 'ZWE'}
    
    def __init__(self, 
                 oxford_url = 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv',
                 hopkins_cases_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
                 hopkins_recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
                 indicators_path = 'https://raw.githubusercontent.com/Kipre/files/master/hosted/indicators.csv'):
        self.oxford = pd.read_csv(oxford_url, parse_dates=['Date'])
        self.hopkins_cases = pd.read_csv(hopkins_cases_url)
        self.hopkins_recovered = pd.read_csv(hopkins_recovered_url)
        self.indicators = pd.read_csv(indicators_path).set_index('Country', drop=True)
        self.oxford = self.oxford.sort_values(['CountryCode', 'Date']).copy()
        first_values = self.oxford['CountryCode'].drop_duplicates()
        today_values = self.oxford[self.oxford['Date'].dt.date == pd.Timestamp.today().date()]
        # self.oxford = self.oxford[['CountryName', 'CountryCode', 'Date', 'ConfirmedCases', 'ConfirmedDeaths', 'StringencyIndexForDisplay']].drop(today_values.index)
        self.oxford.loc[first_values.index] = 0
        self.oxford = self.oxford.fillna(method='bfill')

    def ox_full(self, cases_shifts=[], rescaling=1):
        countries = self.oxford['CountryCode'].unique()
        result = self.oxford.copy()
        for shift in cases_shifts:
            for country in countries:
                tmp = result.loc[result['CountryCode'] == country]['ConfirmedCases']/rescaling
                tmp = tmp.shift(periods=shift, fill_value=0)
                result.loc[result['CountryCode'] == country, f'ConfirmedCases {shift}'] = tmp
        return result

    def ox_augmented(self, rescaling=1):
        indicators_df = self.indicators.copy()
        indicators_df = (indicators_df-indicators_df.min())/(indicators_df.max()-indicators_df.min()) # normalization

        data = self.ox_full().join(indicators_df, on='CountryCode')
        data = data.dropna()

        data['StringencyIndexForDisplay'] /= 100
        data['ConfirmedCases'] /= rescaling

        return data

    def ox_train_test(self, rescaling=1, seed=34):
        data = self.ox_augmented(rescaling)

        all_countries = data['CountryName'].unique()

        if seed:
            np.random.seed(seed)

        test_countries = np.random.choice(all_countries, int(0.2*len(all_countries)), replace=False)
        train_countries = [c for c in all_countries if c not in test_countries]


        test_data = data.loc[data.reset_index().set_index('CountryName').loc[test_countries]['index']]
        train_data = data.loc[data.reset_index().set_index('CountryName').loc[train_countries]['index']]
        return train_data, test_data, {'test_countries': test_countries, 'train_countries': train_countries}


    def sir(self, country, rescaling=1):
        recovered = self.hopkins_recovered[self.hopkins_recovered['Country/Region'] == country].sum().iloc[4:]
        recovered = np.array(recovered, dtype=np.int64)/rescaling
        cumulative = self.cumulative(country, rescaling)

        total_population = np.full_like(cumulative, self.indicators.loc[pycountry.countries.get(name=country).alpha_3, 'SP.POP.TOTL'])/rescaling
        infected = cumulative - recovered
        susceptible = total_population - cumulative
        result = np.concatenate([susceptible.reshape(-1, 1), 
                                 infected.reshape(-1, 1), 
                                 recovered.reshape(-1, 1)],
                                 axis=1)
        return result

    def cumulative(self, country, rescaling=1):
        cumulative = self.hopkins_cases[self.hopkins_cases['Country/Region'] == country].sum().iloc[4:]
        if rescaling == -1:
            rescaling = max(cumulative)
        return np.array(cumulative, dtype=np.int64)/rescaling

    def all_hopkins_countries(self, cases_cap=0):
        return list(self.hopkins_cases[self.hopkins_cases.iloc[:, -1] > cases_cap]['Country/Region'].unique())

    def all_ox_countries(self):
        return list(self.oxford['CountryName'].unique())

    def ox_for(self, country, rescaling=1):
        if country not in self.oxford['CountryName'].unique():
            raise Exception('Country is not in names')
        result = self.oxford[self.oxford['CountryName'] == country].copy()
        if rescaling == -1:
            rescaling = result['ConfirmedCases'].max()
        result['ConfirmedCases'] /= rescaling
        return result

    def stringency(self, country):
        return self.ox_for(country)['StringencyIndexForDisplay'].values


def integrate_df(real_trajectory, 
                 variables, 
                 predicted_variables, 
                 sparse_filters,
                 time_dependent_variables,
                 constant_variables,
                 weights,
                 extrapolation=50, 
                 max_degree=2):
    real_trajectory = real_trajectory.append(real_trajectory.iloc[[-1]*extrapolation]).reset_index(drop=True)
    
    constant_terms = [real_trajectory.iloc[[0]].loc[:, inds].values.prod() for inds in constant_variables]
    
    constant_terms = np.multiply(np.array(constant_terms).reshape(-1, 1), weights)
    predicted_values = [real_trajectory.iloc[0][predicted_variables].values]
    not_predicted_time_dependent = real_trajectory[[a for a in time_dependent_variables if a not in predicted_variables]].values
    
    def time_dependent_terms(k):
        current_filter = sparse_filters.copy()
        values = list(predicted_values[k]) + list(not_predicted_time_dependent[k])
        for i, val in enumerate(values):
            current_filter[:, i*max_degree:(i + 1)*max_degree] *= val
        return np.nanprod(current_filter, axis=1)
    for k in range(len(real_trajectory.index) - 1):
        current_filter = time_dependent_terms(k)
        predicted_values.append(current_filter @ constant_terms)
    return np.array(predicted_values)
