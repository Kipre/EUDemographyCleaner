import numpy as np
from scipy.integrate import solve_ivp
from scipy.io import savemat


## Time intervals
t = np.linspace(1, 10, 300)

## Parameters
linear_oscillator_params = np.array([[-0.1, 2],
	                                 [-2, -0.1]])
oscillator_3d_params = np.array([[-0.1, 2, 0],
                                 [-2, -0.1, 0],
                                 [0, 0, -0.3]])

## Functions
def linear_oscillator(t, y):
	[x, y] = y 
	return np.array([-0.1*x + 2*y,
	                 -2*x + -0.1*y])

def cubic_oscillator(t, y):
	[x, y] = y 
	return np.array([-0.1*x**3 + 2*y**3,
	                 -2*x**3 + -0.1*y**3])

def oscillator_3d(t, y):
	[x, y, z] = y 
	return np.array([-0.1*x + 2*y,
	                 -2*x + -0.1*y,
	                 - 0.3*z])

def lorenz(t, y, sigma=10, beta=8/3, rho=28):
	[x, y, z] = y
	return np.array([sigma*(y - x),
		             x*(rho - z) - y,
		             x*y - beta*z])

def mean_field(t, y, mu=-0.01, omega=9, lambd=0.01, A=-0.01):
	[x, y, z] = y
	return np.array([mu*x - omega*y + A*x*z,
		             omega*x + mu*y + A*y*z,
		             -lambd*(z - x**2 - y**2)])

def van_der_pol(t, y):
	[x, y] = y
	return np.array([y,
		             (1 - x**2)*y - x])

functions = {'linear_oscillator': linear_oscillator,
             'cubic_oscillator': cubic_oscillator,
             'oscillator_3d': oscillator_3d,
             'lorenz': lorenz,
             'mean_field': mean_field,
             'van_der_pol': van_der_pol}

## Initial conditions
initial_conditions = {'linear_oscillator': [2, 0],
                      'cubic_oscillator': [2, 0],
                      'oscillator_3d':[1, 0, 1],
                      'lorenz': [-8, 7, 27],
                      'mean_field': [-100, 0, 0],
                      'van_der_pol': [2, 0]}

## Integration
results = {}
for function in functions.keys():
	res = solve_ivp(functions[function], (t[0], t[-1]), 
		            initial_conditions[function],
		            t_eval=t)
	if res['success'] == True:
		results[function] = res['y'].T

savemat('py_odes.mat', results)
