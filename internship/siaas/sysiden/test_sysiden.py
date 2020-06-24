import unittest
from sysiden import *
import pandas as pd
import numpy as np

data = pd.read_csv("https://raw.githubusercontent.com/Kipre/files/master/hosted/test_data/linear_oscillator_data.csv")
X = pd.read_csv("https://raw.githubusercontent.com/Kipre/files/master/hosted/test_data/linear_oscillator_X.csv")
augmented = pd.read_csv("https://raw.githubusercontent.com/Kipre/files/master/hosted/test_data/linear_oscillator_augmented.csv")
targets = pd.read_csv("https://raw.githubusercontent.com/Kipre/files/master/hosted/test_data/linear_oscillator_targets.csv")
weights = pd.read_csv("https://raw.githubusercontent.com/Kipre/files/master/hosted/test_data/linear_oscillator_weights.csv", index_col=0)



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

class TestSparseRegression(unittest.TestCase):

    def test_spreg_with_real_data(self):
        output = sparse_regression(augmented, targets, cutoff=2e-3)
        pd.testing.assert_frame_equal(weights, output, check_like=True, check_dtype=False)






if __name__ == '__main__':
    unittest.main()
