import numpy as np
from itertools import combinations_with_replacement


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

def make_targets(data, threshold=-1):
    """Returns 3 matrices: derivatires, m2 and m1"""
    derivatives, m2, m1 = [], [], []

    def separate(scenario):
        gradients = np.gradient(scenario, axis=0)
        for i, derivative in enumerate(gradients[1:-1]):
            if (abs(scenario[i+1]) > threshold).any():
                derivatives.append(derivative)
                m2.append(scenario[i+2])
                m1.append(scenario[i+1])

    if len(data.shape) == 3:
        for scenario in data:
            separate(scenario)
    elif len(data.shape) == 2:
        separate(data)
    return np.array(derivatives, dtype=np.float32), np.array(m2, dtype=np.float32), np.array(m1, dtype=np.float32)