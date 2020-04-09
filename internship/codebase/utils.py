import numpy as np
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
    if (np.diag(weights, k=-1) > 0.5).all() and (np.diag(weights, k=-1) < 1.5).all():
        if derivative and warn:
            print('Are you sure those are derivatives?')
    else:
        if not derivative and warn:
            print('Are you sure those are not derivatives?')
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

