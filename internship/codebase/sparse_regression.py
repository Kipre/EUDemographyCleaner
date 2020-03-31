import tensorflow as tf
import numpy as np
from itertools import combinations_with_replacement


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