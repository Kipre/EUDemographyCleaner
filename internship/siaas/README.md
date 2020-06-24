# System Identification as a service

This folder contains a working example of a service to identify ODEs from data.



## Under the hood (`sysiden`)

The module that implements all of the functionality is called `sysiden` and is in the folder with the same name.

__Dependencies__:

- recent Pandas
- recent NumPy


This server-side app is mean to identify governing equations from data. The implementation relies on the method proposed by Brunton et al. in [this paper](https://www.pnas.org/content/113/15/3932). 


### Inputs 

## Service

In order to interact with the service the user must perform a GET request with a file and some parameters.

