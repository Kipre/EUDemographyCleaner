import unittest
from sysiden import *
import pandas as pd
import numpy as np
from scipy.integrate import solve_ivp
import io

url = "https://raw.githubusercontent.com/Kipre/files/master/hosted/test_data/"

data = pd.read_csv(f"{url}linear_oscillator_data.csv")
X = pd.read_csv(f"{url}linear_oscillator_X.csv")
augmented = pd.read_csv(f"{url}linear_oscillator_augmented.csv")
targets = pd.read_csv(f"{url}linear_oscillator_targets.csv")
weights = pd.read_csv(f"{url}linear_oscillator_weights.csv", index_col=0)

lorenz_data = pd.read_csv(f"{url}lorenz_data.csv")
lorenz_X = pd.read_csv(f"{url}lorenz_X.csv")
lorenz_augmented = pd.read_csv(f"{url}lorenz_augmented.csv")
lorenz_targets = pd.read_csv(f"{url}lorenz_targets.csv")
lorenz_weights = pd.read_csv(f"{url}lorenz_weights.csv", index_col=0)
lorenz_dtargets = pd.read_csv(f"{url}lorenz_dtargets.csv")
lorenz_dweights = pd.read_csv(f"{url}lorenz_dweights.csv", index_col=0)


class TestAugmentRow(unittest.TestCase):

    def test1(self):
        np.testing.assert_almost_equal(np.array([1, 2, 4, 8]), augment_row(np.array([2]), 3))
        np.testing.assert_almost_equal(np.array([1, 2, 1, 4, 2, 1]), augment_row(np.array([2, 1]), 2))


class TestProcessInput(unittest.TestCase):

    f = io.StringIO(requests.get(f"{url}linear_oscillator_data.csv").text)
    f_mt = io.StringIO(requests.get(f"{url}lorenz_data.csv").text)
    nan_corrupted = io.StringIO(requests.get(f"{url}data_with_nan_inconsistency.csv").text)
    str_corrupted = io.StringIO(requests.get(f"{url}data_with_string.csv").text)

    def test_good_file(self):
        output = process_input_file(self.f)
        pd.testing.assert_frame_equal(output, data)

    def test_good_file_mt(self):
        output = process_input_file(self.f_mt)
        pd.testing.assert_frame_equal(output, lorenz_data)

    def test_nan_corrupted(self):
        output = process_input_file(self.nan_corrupted)
        pd.testing.assert_frame_equal(output, pd.DataFrame(['The input csv must have all NaNs on same lines'], index=['error']))

    def test_str_corrupted(self):
        output = process_input_file(self.str_corrupted)
        pd.testing.assert_frame_equal(output, pd.DataFrame(['The input csv must contain only numerical columns'], index=['error']))


class TestMakeTargets(unittest.TestCase):

    simple_df = pd.DataFrame([[1., 1., 1.],
                              [2., 2., 2.],
                              [3., 3., 3.]],
                             columns=['a', 'b', 'c'])
    nan_df = pd.DataFrame([[1., 1., 1.],
                           [2., 2., 2.],
                           [np.nan, np.nan, np.nan],
                           [2., 2., 2.],
                           [3., 3., 3.]],
                          columns=['a', 'b', 'c'])
    diff_df = pd.DataFrame([[1., 1., 1.],
                           [2., 1., 2.],
                           [np.nan, np.nan, np.nan],
                           [2., 2., 2.],
                           [3., 1., 3.]],
                          columns=['a', 'b', 'c'])
    X = pd.DataFrame([[1., 1., 1.],
                      [2., 2., 2.]],
                     columns=['a', 'b', 'c'])
    X2 = pd.DataFrame([[2., 2., 2.],
                       [3., 3., 3.]],
                      columns=['a', 'b', 'c'])
    X2_d = pd.DataFrame([[1., 0., 1.],
                       [1., -1., 1.]],
                      columns=['a', 'b', 'c'])

    def test_simple_case(self):
        X, X2 = make_targets(self.simple_df)
        pd.testing.assert_frame_equal(X.reset_index(drop=True), self.X)
        pd.testing.assert_frame_equal(X2.reset_index(drop=True), self.X2)

    def test_nan_case(self):
        X, X2 = make_targets(self.nan_df)
        pd.testing.assert_frame_equal(X.reset_index(drop=True), self.X)
        pd.testing.assert_frame_equal(X2.reset_index(drop=True), self.X2)

    def test_diff_case(self):
        X, X2_d = make_targets(self.diff_df, derivative=True)
        pd.testing.assert_frame_equal(X.reset_index(drop=True), self.X)
        pd.testing.assert_frame_equal(X2_d.reset_index(drop=True), self.X2_d)
    
    def test_error_passing(self):
        error = pd.DataFrame(['Some error'], index=['error'])
        output1, output2 = make_targets(error)

        pd.testing.assert_frame_equal(error, output1)
        pd.testing.assert_frame_equal(error, output2)

    def test_error_raising(self):
        error = pd.DataFrame(['The input csv must have more than 1 row'], index=['error'])
        output1, output2 = make_targets(pd.DataFrame())

        pd.testing.assert_frame_equal(error, output1)
        pd.testing.assert_frame_equal(error, output2)

    def test_real(self):
        output1, output2 = make_targets(data)
        pd.testing.assert_frame_equal(X, output1)
        pd.testing.assert_frame_equal(targets, output2)

    def test_real_lorenz(self):
        output1, output2 = make_targets(lorenz_data)
        pd.testing.assert_frame_equal(lorenz_X, output1.reset_index(drop=True))
        pd.testing.assert_frame_equal(lorenz_targets, output2.reset_index(drop=True))

    def test_real_dlorenz(self):
        output1, output2 = make_targets(lorenz_data, derivative=True)
        pd.testing.assert_frame_equal(lorenz_X, output1.reset_index(drop=True))
        pd.testing.assert_frame_equal(lorenz_dtargets, output2.reset_index(drop=True))


class TestAugment(unittest.TestCase):
    simple_df = pd.DataFrame([[1., 2.],
                              [1., 4.],
                              [1., 3.]],
                             columns=['a', 'b'])
    expected2 = pd.DataFrame([[1., 1., 2., 1., 2., 4.],
                              [1., 1., 4., 1., 4., 16.],
                              [1., 1., 3., 1., 3., 9.]],
                             columns=['1*1', '1*a', '1*b', 'a*a', 'a*b', 'b*b'])
    expected4 = pd.DataFrame([[  1.,  1.,   2.,   1.,   2.,   4.,   1.,   2.,   4.,   8.,   1.,   2.,   4.,   8.,  16.],
                              [  1.,  1.,   4.,   1.,   4.,  16.,   1.,   4.,  16.,  64.,   1.,   4.,  16.,  64., 256.],
                              [  1.,  1.,   3.,   1.,   3.,   9.,   1.,   3.,   9.,  27.,   1.,   3.,   9.,  27.,  81.]],
                             columns=['1*1*1*1', '1*1*1*a', '1*1*1*b', '1*1*a*a', '1*1*a*b', '1*1*b*b', '1*a*a*a',
                                      '1*a*a*b', '1*a*b*b', '1*b*b*b', 'a*a*a*a', 'a*a*a*b', 'a*a*b*b', 'a*b*b*b', 'b*b*b*b'])
    
    def test_degree_2(self):
        pd.testing.assert_frame_equal(augment(self.simple_df, max_degree=2), self.expected2, check_like=True, check_dtype=False)
    
    def test_degree_4(self):
        pd.testing.assert_frame_equal(augment(self.simple_df, max_degree=4), self.expected4, check_like=True, check_dtype=False)
    
    def test_error_passing(self):
        error = pd.DataFrame(['Some error'], index=['error'])
        output = augment(error, 3)

        pd.testing.assert_frame_equal(error, output)

    def test_real(self):
        output = augment(X, max_degree=3)
        pd.testing.assert_frame_equal(augmented, output, check_like=True, check_dtype=False)

    def test_real_lorenz(self):
        output = augment(lorenz_X, max_degree=4)
        pd.testing.assert_frame_equal(lorenz_augmented, output, check_like=True, check_dtype=False)


class TestSparseRegression(unittest.TestCase):

    def test_spreg_with_real_data(self):
        output = sparse_regression(augmented, targets, cutoff=2e-3)
        pd.testing.assert_frame_equal(weights, output, check_like=True, check_dtype=False)

    def test_spreg_with_lorenz(self):
        output = sparse_regression(lorenz_augmented, lorenz_targets, cutoff=2e-3)
        self.assertLess((output.values - lorenz_weights.values).mean(), 3e-3)

    def test_spreg_with_dlorenz(self):
        output = sparse_regression(lorenz_augmented, lorenz_dtargets, cutoff=2e-3)
        self.assertLess((output.values - lorenz_dweights.values).mean(), 3e-3)

class TestIdentifySystem(unittest.TestCase):

    f = io.StringIO(requests.get(f"{url}linear_oscillator_data.csv").text)

    def test_good_file(self):
        output = identify_system(self.f, 2e-3, 3)
        pd.testing.assert_frame_equal(pd.read_csv(io.StringIO(output), index_col=0), weights)

    # def test_random_function(self):
    #     # won't work because generated systems are too unstable

    #     max_degree = 3

    #     # first we need to create data
    #     weights = np.random.uniform(size=(10, 2))
    #     weights[weights < 0.4] = 0

    #     t = np.linspace(0, 1, 200)

    #     res = solve_ivp(lambda t, y: augment_row(y, max_degree) @ weights, (t[0], t[-1]), [2, 3], t_eval=t)
    #     print(res)


if __name__ == '__main__':
    unittest.main()
