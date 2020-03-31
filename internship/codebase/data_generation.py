import numpy as np
from scipy.integrate import solve_ivp
from scipy.io import savemat

## Be sure to be in the right directory before executiong

## Time intervals
t = np.linspace(0, 10, 300)

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

def gererate_initial_conditions(seeds, nb_augmentations=9, dispersion=0.1):
	result = {}
	for function, condition in seeds.items():
		conditions = [condition]
		magnitude = max(condition)*dispersion
		for k in range(nb_augmentations):
			conditions.append(condition + magnitude*np.random.randn(len(condition)))
		result[function] = conditions
	return result


## Integration
if __name__ == "__main__":
	# only one trajectory
	results = {'t': t}
	for function in functions.keys():
		res = solve_ivp(functions[function], (t[0], t[-1]), 
			            initial_conditions[function],
			            t_eval=t)
		if res['success'] == True:
			results[function] = res['y'].T
		else:
			raise Exception(f'Integration failed for {function}')

	savemat('py_odes.mat', results)

	# multiple tajectories
	results = {'t': t}
	for function, conditions in gererate_initial_conditions(initial_conditions).items():
		result = []
		for initial_condition in conditions:
			res = solve_ivp(functions[function], (t[0], t[-1]), 
				            initial_condition,
				            t_eval=t)
			if res['success'] == True:
				result.append(res['y'].T)
			else:
				raise Exception(f'Integration failed for {function}')
		results[function] = np.array(result, dtype=np.float32)

	savemat('py_odes_mult_traj.mat', results)
