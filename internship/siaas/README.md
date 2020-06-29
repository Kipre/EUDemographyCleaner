# System Identification as a service

This folder contains a working example of a service to identify ODEs from data.

The module that implements all of the functionality is called `sysiden` and is in the folder with the same name.

__Dependencies__:

- recent Pandas
- recent NumPy


This server-side app is meant to identify governing equations from data. The implementation relies on the method proposed by Brunton et al. in [this paper](https://www.pnas.org/content/113/15/3932). 

## Service deployment

The app is hosted using Flask. 
It can be deployed by executing the `deploy.py` file (warning: this will create a service in debug mode, in order to make it run for production one has to consult Flask's documentation). 
In order to check that the server runs well, one can execute `test_api.py` to check that the server treats the request correctly.

## API

In order to interact with the service the user must perform a POST request with a file and some parameters.

### Inputs 

The POST request must contain 1 csv file with the trajectories of the system and each column corresponding to a variable labeled as `trajectories`. 
For example if the system is a Lorenz oscillator and it has 3 variables then the csv should be like:

|            x |            y |         z |
|-------------:|-------------:|----------:|
|  -8          |   7          |  27       |
|  -3.84067    |   6.2606     |  23.4642  |
|  -1.07199    |   5.62093    |  21.0143  |
|   0.787232   |   5.42176    |  19.2094  |
|   2.138      |   5.71571    |  17.8374  |
|   3.25886    |   6.48417    |  16.8459  |

If the csv contains multiple trajectories, then they must be separated by a row of NaNs:

```
            x ,            y ,         z 
  -8          ,   7          ,  27       
  -3.84067    ,   6.2606     ,  23.4642  
  -1.07199    ,   5.62093    ,  21.0143  
   0.787232   ,   5.42176    ,  19.2094   
              ,              ,            # row to separate trajectories
   5.54335    ,   9.36954    ,  16.2365  
   6.93005    ,  11.4108     ,  16.9281  
   8.5369     ,  13.6544     ,  18.5924  
  10.3046     ,  15.7027     ,  21.444   
```
otherwise the sequentiality will be misinterpreted and will introduce error.
The first line of the csv must contain the names of the variables, the result is visually better if the names are short and without '*' or ' '(space).

And the POST request must contain the hyperparameters of the model:

 - the `cutoff_value` (a float in the [0, 10] range) which is the threshold for the weight matrix;
 - the `max_degree` of polynomial terms (an integer in the range [1, 10]), default value: 3;
 - boolean `derivative` to decide whether to use the iterative or the derivative formulation, default value is `false`.

### Examples

An example of a valid request in python:

```python
import requests 
  
API_ENDPOINT = "http://127.0.0.1:5000/" # or your api address

# input csv
csv = '''x,y,z
-8.00,7.00,27.00
-3.84,6.26,23.46
-1.07,5.62,21.01
0.79,5.42,19.21
2.14,5.72,17.84
3.26,6.48,16.85
4.35,7.71,16.27
5.54,9.37,16.24
'''

# data to be sent to api 
files = {'trajectories': csv} 
data = {'cutoff_value': 0.1,
        'max_degree': 2,
        'derivative': False}

  
# sending post request
r = requests.post(url=API_ENDPOINT, data=data, files=files) 
  
# extracting response text  
print(r.text) 
```

And one in JS (doesn't work because of CORS but the request is valid):
```javascript
var csv = `x,y,z
-8.00,7.00,27.00
-3.84,6.26,23.46
-1.07,5.62,21.01
0.79,5.42,19.21
2.14,5.72,17.84
3.26,6.48,16.85
4.35,7.71,16.27
5.54,9.37,16.24`

var data = new FormData()
data.append('trajectories', csv)
data.append('cutoff_value', 0.001)
data.append('max_degree', 3)

var myInit = { method: 'POST',
               body: data,
               mode: 'no-cors'};

var myRequest = new Request('http://127.0.0.1:5000/', myInit);

fetch(myRequest, myInit)
.then((response) => {
  console.log(response);
});
```

### Output 


The output of the aforementioned example will be:
```
,x,y,z
1*1,0.0,59.682481901541614,0.0
1*x,0.7298136699801716,-0.6164837544419073,0.16165098858544485
1*y,0.34203527283702495,1.5550319830339248,0.15561696075274623
1*z,-0.015692693821673764,-9.335181149892428,0.878181705565331
x*x,0.0,0.0,0.0
x*y,0.0,-0.2665996746542967,0.0
x*z,0.0,0.26971879022396406,0.0
y*y,0.0,0.0,0.0
y*z,0.0,0.0,0.0
z*z,0.0,0.31020575053020144,0.0
```

The output will always have the following form:

|     |        variable1 |         variable2 |
|:----|---------:|----------:|
| 1*1 | 2.14319  |  5.92495  |
| 1*variable1 | 0.872789 | -0.102448 |
| 1*variable2 | 0        |  1.23981  |
| variable1*variable1 | 0        |  0        |
| variable1*variable2 | 0        |  0        |
| variable2*variable2 | 0        |  0        |

and in each column one can find the coefficients of the different terms in the identified dynamics.

## Error handling

If the request is not valid a 400 (bad request) response will be thrown. If data is not well formed or an error occurs during the processing, a csv with the error description well be returned.


## TODO

- Add other candidate functions support
- Add cutoff value optimization

