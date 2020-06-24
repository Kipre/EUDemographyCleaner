import requests 
  
API_ENDPOINT = "http://127.0.0.1:5000/"
  
f = open('../indicators.csv', 'r')

# data to be sent to api 
files = {'the_file': f} 
data = {'cutoff_value': 0.001}

  
# sending post request and saving response as response object 
r = requests.get(url=API_ENDPOINT, data=data, files=files) 
  
# extracting response text  
print(r.text ) 