import tensorflow as tf
import numpy as np
from scipy.integrate import solve_ivp
import codebase
from codebase.utils import find_degree, make_polynomials


def sparse_regression(augmented, targets, 
                      cutoff=1e-4,
                      max_iterations=10,
                      solver=lambda A, B: tf.linalg.lstsq(A, B, fast=False)):
    """Implementation of the sparse regression algorithm as described 
    in https://arxiv.org/pdf/1509.03580.pdf

    Args:
        augmented (np.array): array of shape (m, n) containing the states 
            augmented with the candidate functions.
        targets (np.array): array of shape (m, k) containing the time 
            derivatives or the states at the next timestep.
        cutoff (float): 

    Returns:
        array: The matrix of shape (n, k) of weights that minimize the problem.
    """
    assert targets.shape[0] == augmented.shape[0]
    assert len(targets.shape) == len(augmented.shape) and len(targets.shape) == 2
    
    weights = solver(augmented, targets)
    nb_variables = targets.shape[1]
    for iteration in range(max_iterations):
        weights = tf.where(tf.math.abs(weights) < cutoff, 0, weights)
        other_weights = weights.numpy()
        for i in range(nb_variables):
            condition = tf.math.abs(weights[..., i]) > cutoff
            big_indexes = tf.where(condition)
            subweights = tf.squeeze(tf.gather(augmented, big_indexes, axis=-1), axis=[2])
            other_weights[big_indexes, i] = solver(subweights, targets[..., i, tf.newaxis])
        if not (weights - other_weights).numpy().any():
            break
        weights = tf.cast(other_weights, dtype=tf.float32)
    return weights, iteration


def naive_integrate(weights, initial_state, nb_iterations=100, limit=1e10):
    states = [np.array(initial_state)]
    max_degree = find_degree(weights.shape[0], weights.shape[1] + 1)
    for k in range(nb_iterations-1):
        new_state, _ = make_polynomials(states[k], max_degree=max_degree)
        new_state = tf.matmul(new_state.reshape(1, -1), weights).numpy().reshape(-1)
        states.append(new_state)
    return np.array(states, dtype=np.float32)

def ivp_integrate(weights, initial_state, t, max_degree=None):
    if not max_degree:
        max_degree = find_degree(weights.shape[0], weights.shape[1] + 1)
    def func(t, y):
        augmentation, _ = make_polynomials(y, max_degree=max_degree)
        return tf.matmul(augmentation.reshape(1, -1), weights)
    res = solve_ivp(func, (t[0], t[-1]), initial_state, t_eval=t)
    if res['success']:
        return res['y']
    elif res['message'] == 'Required step size is less than spacing between numbers.':
        return complete(res['y'][0], len(t)).T
    else:
        raise Exception(f"Could not integrate: {res['message']}")

def integrate(weights, initial_state, t, max_degree=None, derivative=False):
    if derivative:
        guess = ivp_integrate(weights, initial_state, t, max_degree=max_degree)
        if len(guess.shape) == 1:
            guess = guess.reshape(1, -1)
        return guess.T
    else:
        return naive_integrate(weights, initial_state, nb_iterations=len(t))

def complete(array, n):
    result = np.full(n, array.flatten()[-1])
    result[:len(array)] = array
    return result