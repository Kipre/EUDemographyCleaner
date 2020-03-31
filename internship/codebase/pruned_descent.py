import tensorflow as tf
from tensorflow_model_optimization.sparsity import keras as sparsity

class PrunableLayer(tf.keras.layers.Layer, sparsity.PrunableLayer):

    def __init__(self, nb_funcs=None, 
                 nb_variables=None, 
                 starting_vector=None):
        super(PrunableLayer, self).__init__()
        if starting_vector is not None:
            self.w = tf.Variable(initial_value=starting_vector,
                                dtype='float32',
                                trainable=True)
        else:
            w_init = tf.random_normal_initializer()
            self.w = tf.Variable(initial_value=w_init(shape=(nb_funcs, nb_variables),
                                dtype='float32'),
                                trainable=True)

    def call(self, inputs):
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
        self.frequency = frequency
        self.nb_funcs_to_keep = nb_funcs_to_keep
        self.begin_step = begin_step.astype(tf.int64)
        self.end_step = end_step.astype(tf.int64)
        self.initial_sparsity = initial_sparsity
        final_sparsity = 1 - nb_funcs_to_keep/(nb_funcs + nb_variables)
        delta_steps = end_step - begin_step
        nb_updates = delta_steps/frequency
        self.sparsity_increase = (final_sparsity - initial_sparsity)/nb_updates
        self.sparsities = []
        self.schedule = []
        for k in range(end_step):
            if k > begin_step:
                i = (k-begin_step)//frequency + 1
                self.schedule.append(tf.constant(True, dtype=tf.bool))
                self.sparsities.append(tf.constant(i*self.sparsity_increase + self.initial_sparsity, dtype=tf.float32))
            else:
                self.schedule.append(tf.constant(False, dtype=tf.bool))
                self.sparsities.append(tf.constant(0, dtype=tf.float32))
        self.schedule = tf.stack(self.schedule)
        self.sparsities = tf.stack(self.sparsities)


    def __call__(self, step):
        return tf.gather(self.schedule, step), tf.gather(self.sparsities, step)

    def from_config(self):
        raise NotImplementedError

    def get_config(self):
        raise NotImplementedError


class PrunedRegression(tf.keras.Model):

    def __init__(self, nb_funcs, nb_variables,
                 model=None,
                 **kwargs):
        super(PrunedRegression, self).__init__()
        if not model is None:
            self.xi = sparsity.prune_low_magnitude(PrunableLayer(starting_vector=model.xi.layer.w), 
                              **kwargs)
        else:
            self.xi = sparsity.prune_low_magnitude(PrunableLayer(nb_funcs=nb_funcs,
                                nb_variables=nb_variables,
                                starting_vector=starting_vector), 
                                **kwargs)

    def call(self, x):
        return self.xi(x)