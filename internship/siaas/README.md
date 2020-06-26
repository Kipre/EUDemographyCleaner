# System Identification as a service

This folder contains a working example of a service to identify ODEs from data.



## Under the hood (`sysiden`)

The module that implements all of the functionality is called `sysiden` and is in the folder with the same name.

__Dependencies__:

- recent Pandas
- recent NumPy


This server-side app is meant to identify governing equations from data. The implementation relies on the method proposed by Brunton et al. in [this paper](https://www.pnas.org/content/113/15/3932). 

## Error handling

If the imput is not 


## Service

In order to interact with the service the user must perform a GET request with a file and some parameters.

### Inputs 

1 csv file with the trajectories of the system and each column corresponding to a variable labaled as `trajectories`. 
For example if the system is a Lorenz oscillator and it has 3 variables then the csv should be like:

|            x |            y |         z |
|-------------:|-------------:|----------:|
|  -8          |   7          |  27       |
|  -3.84067    |   6.2606     |  23.4642  |
|  -1.07199    |   5.62093    |  21.0143  |
|   0.787232   |   5.42176    |  19.2094  |
|   2.138      |   5.71571    |  17.8374  |
|   3.25886    |   6.48417    |  16.8459  |
|   4.34854    |   7.70897    |  16.2737  |
|   5.54335    |   9.36954    |  16.2365  |
|   6.93005    |  11.4108     |  16.9281  |
|   8.5369     |  13.6544     |  18.5924  |
|  10.3046     |  15.7027     |  21.444   |
|  12.0438     |  16.8416     |  25.5092  |
|  13.387      |  16.3329     |  30.1905  |

If the csv contains multiple trajectories, then they must be separated by a row of NaNs:

```
            x ,            y ,         z 
  -8          ,   7          ,  27       
  -3.84067    ,   6.2606     ,  23.4642  
  -1.07199    ,   5.62093    ,  21.0143  
   0.787232   ,   5.42176    ,  19.2094  
   2.138      ,   5.71571    ,  17.8374  
   3.25886    ,   6.48417    ,  16.8459  
              ,              ,            # row to separate trajectories
   5.54335    ,   9.36954    ,  16.2365  
   6.93005    ,  11.4108     ,  16.9281  
   8.5369     ,  13.6544     ,  18.5924  
  10.3046     ,  15.7027     ,  21.444   
  12.0438     ,  16.8416     ,  25.5092  
  13.387      ,  16.3329     ,  30.1905  
```
otherwise the sequentiality will be misinterpreted and will introduce error.

And the POST request must contain the hyperparameters if the model:

 - the `cutoff_value` (a float in the [0, 100] range) which is the threshold for the weight matrix;
 - the `max_degree` of polynomial terms (an integer in the range [1, 10]), default value: 3;
 - boolean `derivative` to decide whether to use the iterative or the derivative formulation.

An example of a valid request:

```python
import requests 
  
API_ENDPOINT = "http://127.0.0.1:5000/" # or your api address

# input csv
f = '''x,y,z
-8.00,7.00,27.00
-3.84,6.26,23.46
-1.07,5.62,21.01
0.79,5.42,19.21
2.14,5.72,17.84
3.26,6.48,16.85
4.35,7.71,16.27
5.54,9.37,16.24
6.93,11.41,16.93
8.54,13.65,18.59
10.30,15.70,21.44
12.04,16.84,25.51
13.39,16.33,30.19
13.90,13.83,34.29
13.32,10.05,36.60
'''

# data to be sent to api 
files = {'trajectories': f} 
data = {'cutoff_value': 0.1,
        'max_degree': 2
        'derivative': False}

  
# sending post request
r = requests.post(url=API_ENDPOINT, data=data, files=files) 
  
# extracting response text  
print(r.text) 
```

### Output 


The output of the aforementioned example will be:
```
,x,y,z
1*1,2.143193720191059,5.924951824394656,9.421008315110305
1*x,0.8727887493382916,-0.10244788391827639,-0.14955910940162997
1*y,0.0,1.2398107655684192,1.3637065514879356
1*z,0.0,-0.35035942037156714,0.0
x*x,0.0,0.0,0.0
x*y,0.0,0.0,0.0
x*z,0.0,0.0,0.0
y*y,0.0,0.0,0.0
y*z,0.0,0.0,0.0
z*z,0.0,0.0,0.0
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

which means that the 





