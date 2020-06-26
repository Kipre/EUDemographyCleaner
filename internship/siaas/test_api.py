import requests 
import unittest
import pandas as pd
import io
  
API_ENDPOINT = "http://127.0.0.1:5000/"

test_data_url = "https://raw.githubusercontent.com/Kipre/files/master/hosted/test_data/"



class TestApi(unittest.TestCase):

	def test_good_request(self):

		r = requests.get(f"{test_data_url}linear_oscillator_data.csv")
		f = r.text

		files = {'trajectories': f} 
		data = {'cutoff_value': 2e-3,
		        'max_degree': 3,
		        'derivative': False}

		r = requests.post(url=API_ENDPOINT, data=data, files=files) 

		pd.testing.assert_frame_equal(pd.read_csv(io.StringIO(r.text), index_col=0), 
			                          pd.read_csv(f"{test_data_url}linear_oscillator_weights.csv", index_col=0))




if __name__ == '__main__':
    unittest.main()
