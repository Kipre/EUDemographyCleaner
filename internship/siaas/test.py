import requests 
  
API_ENDPOINT = "http://127.0.0.1:5000/"
test_data_url = "https://raw.githubusercontent.com/Kipre/files/master/hosted/test_data/"

r = requests.get(f"{test_data_url}linear_oscillator_data.csv")
f = r.text

# f = open('../indicators.csv', 'r')

# data to be sent to api 
files = {'trajectories': f} 
data = {'cutoff_value': 0.01,
        'max_degree': 2}

  
# sending post request and saving response as response object 
r = requests.post(url=API_ENDPOINT, data=data, files=files) 
  
# extracting response text  
print(r.text ) 