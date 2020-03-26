import tensorflow as tf
from tensorflow_model_optimization.sparsity import keras as sparsity
import tensorflow_model_optimization as tfmot
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


class SparseLayer(tf.keras.layers.Layer, sparsity.PrunableLayer):

    def __init__(self, nb_funcs, state_dim, starting_vector=None):
        super(SparseLayer, self).__init__()
        if starting_vector is not None:
            self.w = tf.Variable(initial_value=starting_vector,
                                 dtype='float32',
                                 trainable=True)
        else:
            w_init = tf.random_normal_initializer()
            self.w = tf.Variable(initial_value=w_init(shape=(nb_funcs, 1),
                                                      dtype='float32'),
                                 trainable=True)

    def call(self, inputs, **kwargs):
        return tf.matmul(inputs, self.w)

    def get_prunable_weights(self):
        return [self.w]


class PDEPruningSchedule(sparsity.PruningSchedule):

    def __init__(self,
                 begin_step,
                 end_step,
                 nb_funcs,
                 nb_funcs_to_keep=3,
                 initial_sparsity=0.5,
                 frequency=100):
        super(PDEPruningSchedule, self).__init__()
        self.nb_funcs = nb_funcs
        self.nb_funcs_to_keep = nb_funcs_to_keep
        self.begin_step = begin_step,
        self.end_step = end_step
        self.initial_sparsity = initial_sparsity
        final_sparsity = 1 - nb_funcs_to_keep / nb_funcs
        delta_steps = end_step - begin_step
        nb_updates = delta_steps / frequency
        sparsity_increase = (final_sparsity - initial_sparsity) / nb_updates
        self.schedule = []
        for k in range(delta_steps):
            i = k // frequency
            self.schedule.append((tf.constant(True, dtype=tf.bool),
                                  tf.constant(i * sparsity_increase + initial_sparsity, dtype=tf.float32)))

    def __call__(self, step):
        if step < self.begin_step or step > self.end_step:
            return tf.constant(False, dtype=tf.bool), tf.constant(self.initial_sparsity, dtype=tf.float32)
        else:
            return self.schedule[step + self.begin_step]

    def from_config(self):
        raise NotImplementedError

    def get_config(self):
        raise NotImplementedError


class PrunedSparseRegression(tf.keras.Model):

    def __init__(self, nb_funcs, state_dim,
                 starting_vector=None):
        super(PrunedSparseRegression, self).__init__()
        self.xi = sparsity.prune_low_magnitude(SparseLayer(nb_funcs=nb_funcs,
                                                           state_dim=state_dim,
                                                           starting_vector=starting_vector))

    def call(self, x, **kwargs):
        return self.xi(x)
