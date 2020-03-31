# Different settings for sparse regression

## Introduction

In this document we analyze how the integartion solver and the number of trajectories affect the results of system identification.

But first how we do system identification ?

Two ways of using sparse regression for system identification: (1) finding the coefficients to compute the next time step or (2) numerically computing the time derivative of the states and finding the coefficients for the time derivative. In terms of maths this translates to:

$$(1): \; X_2 = \Theta(X_1)\xi$$

Where $X_2$ is the matrix of the states that follow those that are in $X_1$ and $\Theta$ is the augmentation by all the candidate functions. This is the first formulation of the problem, it might be the best method if replicating the behaviour of the system is important. Because it gives the very simple discrete integration method where we can compute $x_{k+1}$ based of $x_k$. More precisely: $x_{k+1} = \Theta(x_k)\xi$.

The second formlations requires to first compute a matrix $\dot{X}$ of the time derivtives of the states of the system $X_1$ and then we can do the same kind of sparse regression:

$$(2): \; \dot{X} = \Theta(X_1)\xi$$

This approach is much more useful if we want to have access the formulas that govern the system of interest. But it has the drawback of introducing additionnal errors into the result because of a numerical derivation.



## Linear oscillator

\begin{align}
\dot{x} & = -0.1x + 2y \\
\dot{y} & = -2x -0.1y 
\end{align}

<table>
<tr><th>python data</th><th>octave data</th><th>multiple trajectories</th><th>predicting next state</th></tr>
<tr>
<td>

|   iterations |   examples |        loss |
|-------------:|-----------:|------------:|
|            1 |        298 | 3.05342e-06 |

| function   |   $\dot{x}$ |   $\dot{y}$ |
|:-----------|------------:|------------:|
| $1$        |   0         |   0         |
| $ x$       |  -0.0999018 |  -1.99904   |
| $ y$       |   1.99899   |  -0.0999838 |
| $ x^2$     |   0         |   0         |
| ...   |     ...       |   ...         |
| $ y^5$     |   0         |   0         |

</td>
<td>

|   iterations |   examples |        loss |
|-------------:|-----------:|------------:|
|            1 |        298 | 1.79815e-06 |

| function   |   $\dot{x}$ |   $\dot{y}$ |
|:-----------|------------:|------------:|
| $1$        |   0         |   0         |
| $ x$       |  -0.0998644 |  -1.99869   |
| $ y$       |   1.99868   |  -0.0998814 |
| $ x^2$     |   0         |   0         |
| ...   |     ...       |   ...         |
| $ y^5$     |   0         |   0         |

</td>
<td>

|   iterations |   examples |        loss |
|-------------:|-----------:|------------:|
|            1 |       2980 | 2.57861e-06 |

| function   |   $\dot{x}$ |   $\dot{y}$ |
|:-----------|------------:|------------:|
| $1$        |   0         |   0         |
| $ x$       |  -0.0999064 |  -1.99904   |
| $ y$       |   1.99899   |  -0.0999806 |
| $ x^2$     |   0         |   0         |
| ...   |     ...       |   ...         |
| $ y^5$     |   0         |   0         |

</td>
<td>

|   iterations |   examples |        loss |
|-------------:|-----------:|------------:|
|            1 |        298 | 2.38053e-06 |

| function   |   $x_{k+1}$ |   $y_{k+1}$ |
|:-----------|------------:|------------:|
| $1$        |   0         |   0         |
| $ x$       |   0.994427  |  -0.0666338 |
| $ y$       |   0.0666318 |   0.994424  |
| $ x^2$     |   0         |   0         |
| ...   |     ...       |   ...         |
| $ y^5$     |   0         |   0         |

</td></tr> </table>


## Cubic oscillator

\begin{align}
\dot{x} & = -0.1x^3 + 2y^3 \\
\dot{y} & = -2x^3 -0.1y^3
\end{align}

<table>
<tr><th>python data</th><th>octave data</th><th>multiple trajectories</th><th>predicting next state</th></tr>
<tr><td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            1 |        298 | 0.00188431 |

| function   |   $\dot{x}$ |   $\dot{y}$ |
|:-----------|------------:|------------:|
| $1$        |     0       |   0         |
| ...        |    ...       |   ...        |
| $ y^2$     |     0       |   0         |
| $ x^3$     |    -0.10289 |  -1.983     |
| $ x^2 y$   |     0       |   0         |
| $ x y^2$   |     0       |   0         |
| $ y^3$     |     1.98221 |  -0.0941117 |

</td>
<td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            1 |        298 | 0.00193742 |

| function   |   $\dot{x}$ |   $\dot{y}$ |
|:-----------|------------:|------------:|
| $1$        |    0        |   0         |
| ...        |    ...       |   ...        |
| $ y^2$     |    0        |   0         |
| $ x^3$     |   -0.101967 |  -1.98388   |
| $ x^2 y$   |    0        |   0         |
| $ x y^2$   |    0        |   0         |
| $ y^3$     |    1.98186  |  -0.0938488 |

</td>
<td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            1 |       2980 | 0.00408497 |

| function   |   $\dot{x}$ |   $\dot{y}$ |
|:-----------|------------:|------------:|
| $1$        |    0        |   0         |
| ...        |    ...       |   ...        |
| $ y^2$     |    0        |   0         |
| $ x^3$     |   -0.102783 |  -1.97802   |
| $ x^2 y$   |    0        |   0         |
| $ x y^2$   |    0        |   0         |
| $ y^3$     |    1.97699  |  -0.0923548 |

</td>
<td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            1 |        298 | 0.00377152 |

| function   |   $x_{k+1}$ |   $y_{k+1}$ |
|:-----------|------------:|------------:|
| $1$        |  0          |  0          |
| $ x$       |  1.00577    |  0          |
| $ y$       |  0          |  1.00579    |
| $ x^2$     |  0          |  0          |
| $ x y$     |  0          |  0          |
| $ y^2$     |  0          |  0          |
| $ x^3$     | -0.00816922 | -0.0652496  |
| $ x^2 y$   |  0          | -0.00944947 |
| $ x y^2$   | -0.00826491 |  0          |
| $ y^3$     |  0.0654499  | -0.00740292 |

</td></tr> </table>

## 3D oscillator

\begin{align}
\dot{x} & = -0.1x + 2y \\
\dot{y} & = -2x -0.1y \\
\dot{z} & = -0.3z
\end{align}

<table>
<tr><th>python data</th><th>octave data</th><th>multiple trajectories</th><th>predicting next state</th></tr>
<tr><td>

|   iterations |   examples |        loss |
|-------------:|-----------:|------------:|
|            3 |        298 | 7.52076e-07 |

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |   0         |   0         |    0        |
| $ x$       |  -0.0999137 |  -1.99918   |    0        |
| $ y$       |   1.99913   |  -0.0999876 |    0        |
| $ z$       |   0         |   0         |   -0.300005 |
| $ x^2$     |   0         |   0         |    0        |
| ...     |   ...        |   ...         |    ...        |
| $ z^3$     |   0         |   0         |    0        |

</td>
<td>

|   iterations |   examples |        loss |
|-------------:|-----------:|------------:|
|            2 |        298 | 4.21278e-07 |

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |   0         |   0         |    0        |
| $ x$       |  -0.0998644 |  -1.99869   |    0        |
| $ y$       |   1.99868   |  -0.0998814 |    0        |
| $ z$       |   0         |   0         |   -0.300005 |
| $ x^2$     |   0         |   0         |    0        |
| ...     |   ...        |   ...         |    ...        |
| $ z^3$     |   0         |   0         |    0        |

</td>
<td>

|   iterations |   examples |        loss |
|-------------:|-----------:|------------:|
|            1 |       2980 | 7.35067e-07 |

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |   0         |   0         |    0        |
| $ x$       |  -0.0999077 |  -1.99918   |    0        |
| $ y$       |   1.99913   |  -0.0999942 |    0        |
| $ z$       |   0         |   0         |   -0.300005 |
| $ x^2$     |   0         |   0         |    0        |
| ...     |   ...        |   ...         |    ...        |
| $ z^3$     |   0         |   0         |    0        |

</td>
<td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            3 |        298 | 6.7859e-07 |

| function   |   $x_{k+1}$ |   $y_{k+1}$ |   $z_{k+1}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |   0         |   0         |    0        |
| $ x$       |   0.994426  |  -0.0666383 |    0        |
| $ y$       |   0.0666364 |   0.994424  |    0        |
| $ z$       |   0         |   0         |    0.990017 |
| $ x^2$     |   0         |   0         |    0        |
| ...     |   ...        |   ...         |    ...        |
| $ z^3$     |   0         |   0         |    0        |

</td></tr> </table>


## Lorenz system

\begin{align}
\dot{x} & = \sigma(y-x) \\
\dot{y} & = x (\rho - z) - y \\
\dot{z} & = -\beta z + xy
\end{align}

$\sigma = 10, \beta = 8/3, \rho = 28$

<table>
<tr><th>python data</th><th>octave data</th><th>multiple trajectories</th><th>predicting next state</th></tr>
<tr><td>

|   iterations |   examples |    loss |
|-------------:|-----------:|--------:|
|            3 |        298 | 5.46505 |

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |     0       |    0        |    0        |
| $ x$       |    -9.78027 |   25.6873   |    0        |
| $ y$       |     9.77918 |   -0.54969  |    0        |
| $ z$       |     0       |    0        |   -2.58648  |
| $ x^2$     |     0       |    0        |    0        |
| $ x y$     |     0       |    0        |    0.968372 |
| $ x z$     |     0       |   -0.934577 |    0        |
| $ y^2$     |     0       |    0        |    0        |
| ...        |    ...       |   ...        | ... |
| $ z^3$     |     0       |    0        |    0        |

</td>
<td>

|   iterations |   examples |   loss |
|-------------:|-----------:|-------:|
|            3 |        298 | 5.6519 |

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |     0       |    0        |    0        |
| $ x$       |    -9.7712  |   25.7177   |    0        |
| $ y$       |     9.77124 |   -0.560339 |    0        |
| $ z$       |     0       |    0        |   -2.58106  |
| $ x^2$     |     0       |    0        |    0        |
| $ x y$     |     0       |    0        |    0.967175 |
| $ x z$     |     0       |   -0.935804 |    0        |
| $ y^2$     |     0       |    0        |    0        |
| ...        |    ...       |   ...        | ... |
| $ z^3$     |     0       |    0        |    0        |

</td>
<td>

|   iterations |   examples |    loss |
|-------------:|-----------:|--------:|
|            3 |       2980 | 5.43403 |

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |     0       |    0        |    0        |
| $ x$       |    -9.78071 |   25.7569   |    0        |
| $ y$       |     9.77942 |   -0.573698 |    0        |
| $ z$       |     0       |    0        |   -2.5843   |
| $ x^2$     |     0       |    0        |    0        |
| $ x y$     |     0       |    0        |    0.967858 |
| $ x z$     |     0       |   -0.935538 |    0        |
| $ y^2$     |     0       |    0        |    0        |
| ...        |    ...       |   ...        | ... |
| $ z^3$     |     0       |    0        |    0        |

</td>
<td>

|   iterations |   examples |    loss |
|-------------:|-----------:|--------:|
|            1 |        298 | 5.02598 |

| function   |   $x_{k+1}$ |   $y_{k+1}$ |   $z_{k+1}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |    0        |   0         |   1.15365   |
| $ x$       |    0.656943 |   1.10817   |   0         |
| $ y$       |    0.324933 |   0.861263  |   0         |
| $ z$       |    0        |   0         |   0.864372  |
| $ x^2$     |    0        |   0         |   0         |
| $ x y$     |    0        |   0         |   0.0323595 |
| $ x z$     |    0        |  -0.0361065 |   0         |
| $ y^2$     |    0        |   0         |   0         |
| ...        |    ...       |   ...        | ... |
| $ z^3$     |    0        |   0         |   0         |

</td></tr> </table>

## Mean field

\begin{align}
\dot{x} & = \mu x - \omega y + Axz \\
\dot{y} & = \omega x + \mu y + Ayz \\
\dot{z} & = -\lambda (z - x^2 - y^2)
\end{align}

$\mu=-0.01, \omega=9, \lambda=0.01, A=-0.01$

<table>
<tr><th>real values</th><th>python data</th><th>octave data</th><th>multiple trajectories</th><th>predicting next state</th></tr>
<tr><td>

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |  0          |  0          |  0          |
| $ x$       | -0.01       |  9.0        |  0          |
| $ y$       | -9.0        | -0.01       |  0          |
| $ z$       |  0          |  0          | -0.01       |
| $ x^2$     |  0          |  0          |  0.01       |
| $ x y$     |  0          |  0          |  0          |
| $ x z$     | -0.01       |  0          |  0          |
| $ y^2$     |  0          |  0          |  0.01       |
| $ y z$     |  0          | -0.01       |  0          |
| $ z^2$     |  0          |  0          |  0          |

</td><td>

|   iterations |   examples |     loss |
|-------------:|-----------:|---------:|
|            2 |        298 | 0.015513 |

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        | -0.00680483 |  0          |  1.1217     |
| $ x$       | -0.00659201 |  8.86592    |  0          |
| $ y$       | -8.86596    | -0.00965879 |  0          |
| $ z$       |  0          |  0          | -0.0219288  |
| $ x^2$     |  0          |  0          |  0.00986824 |
| $ x y$     |  0          |  0          |  0          |
| $ x z$     | -0.00960459 |  0          |  0          |
| $ y^2$     |  0          |  0          |  0.00986877 |
| $ y z$     |  0          | -0.00955777 |  0          |
| $ z^2$     |  0          |  0          |  0          |

</td>
<td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            2 |        298 | 0.00966993 |

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        |  0          |   0         |  0.185604   |
| $ x$       | -0.00818584 |   8.86408   |  0          |
| $ y$       | -8.864      |  -0.0100836 |  0          |
| $ z$       |  0          |   0         | -0.011962   |
| $ x^2$     |  0          |   0         |  0.00996986 |
| $ x y$     |  0          |   0         |  0          |
| $ x z$     | -0.00957633 |   0         |  0          |
| $ y^2$     |  0          |   0         |  0.00997246 |
| $ y z$     |  0          |  -0.0095474 |  0          |
| $ z^2$     |  0          |   0         |  0          |

</td>
<td>

|   iterations |   examples |      loss |
|-------------:|-----------:|----------:|
|            2 |       2980 | 0.0145385 |

| function   |   $\dot{x}$ |   $\dot{y}$ |   $\dot{z}$ |
|:-----------|------------:|------------:|------------:|
| $1$        | -0.0068085  |  0          |  1.12172    |
| $ x$       | -0.00659032 |  8.86593    |  0          |
| $ y$       | -8.86597    | -0.00965871 |  0          |
| $ z$       |  0          |  0          | -0.0219291  |
| $ x^2$     |  0          |  0          |  0.00986825 |
| $ x y$     |  0          |  0          |  0          |
| $ x z$     | -0.00960463 |  0          |  0          |
| $ y^2$     |  0          |  0          |  0.00986878 |
| $ y z$     |  0          | -0.00955781 |  0          |
| $ z^2$     |  0          |  0          |  0          |

</td>
<td>

|   iterations |   examples |      loss |
|-------------:|-----------:|----------:|
|            2 |        298 | 0.0135736 |

| function   |    $x_{k+1}$ |    $y_{k+1}$ |   $z_{k+1}$ |
|:-----------|-------------:|-------------:|------------:|
| $1$        |  0.150093    |  0.000624424 | 0.164015    |
| $ x$       |  0.953064    |  0.291349    | 0           |
| $ y$       | -0.291104    |  0.955123    | 0           |
| $ z$       | -0.00164159  |  0           | 0.997915    |
| $ x^2$     |  0           |  0           | 0.000316569 |
| $ x y$     |  0           |  0           | 0           |
| $ x z$     | -0.000296289 |  0           | 0           |
| $ y^2$     |  0           |  0           | 0.000316754 |
| $ y z$     |  0           | -0.000326283 | 0           |
| $ z^2$     |  0           |  0           | 0           |
    
</td></tr> </table>

## Van der Pol

\begin{align}
\dot{x} & = y \\
\dot{y} & = (1 - x^2)y - x 
\end{align}

<table>
<tr><th>python data</th><th>octave data</th><th>multiple trajectories</th><th>predicting next state</th></tr>
<tr><td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            2 |        298 | 0.00338224 |

| function   |   $\dot{x}$ |   $\dot{y}$ |
|:-----------|------------:|------------:|
| $1$        |    0        |    0        |
| $ x$       |    0        |   -0.99125  |
| $ y$       |    0.999718 |    0.98747  |
| $ x^2$     |    0        |    0        |
| $ x y$     |    0        |    0        |
| $ y^2$     |    0        |    0        |
| $ x^3$     |    0        |    0        |
| $ x^2 y$   |    0        |   -0.983185 |
| $ x y^2$   |    0        |    0        |
| $ y^3$     |    0        |    0        |

</td>
<td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            1 |        298 | 0.00194558 |

| function   |   $\dot{x}$ |   $\dot{y}$ |
|:-----------|------------:|------------:|
| $1$        |    0        |    0        |
| $ x$       |    0        |   -1.00186  |
| $ y$       |    0.999593 |    0.996675 |
| $ x^2$     |    0        |    0        |
| $ x y$     |    0        |    0        |
| $ y^2$     |    0        |    0        |
| $ x^3$     |    0        |    0        |
| $ x^2 y$   |    0        |   -0.997846 |
| $ x y^2$   |    0        |    0        |
| $ y^3$     |    0        |    0        |

</td>
<td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            1 |       2980 | 0.00149393 |

| function   |   $\dot{x}$ |   $\dot{y}$ |
|:-----------|------------:|------------:|
| $1$        |     0       |    0        |
| $ x$       |     0       |   -0.995309 |
| $ y$       |     0.99968 |    0.993841 |
| $ x^2$     |     0       |    0        |
| $ x y$     |     0       |    0        |
| $ y^2$     |     0       |    0        |
| $ x^3$     |     0       |    0        |
| $ x^2 y$   |     0       |   -0.989418 |
| $ x y^2$   |     0       |    0        |
| $ y^3$     |     0       |    0        |

</td>
<td>

|   iterations |   examples |       loss |
|-------------:|-----------:|-----------:|
|            1 |        298 | 0.00137975 |

| function   |   $x_{k+1}$ |   $y_{k+1}$ |
|:-----------|------------:|------------:|
| $1$        |   0         |   0         |
| $ x$       |   0.999445  |  -0.0331721 |
| $ y$       |   0.0334359 |   1.0319    |
| $ x^2$     |   0         |   0         |
| $ x y$     |   0         |   0         |
| $ y^2$     |   0         |   0         |
| $ x^3$     |   0         |   0         |
| $ x^2 y$   |   0         |  -0.0328635 |
| $ x y^2$   |   0         |   0         |
| $ y^3$     |   0         |   0         |

</td></tr> </table>

## Conclusions

The few conclusions we can draw from all of those tables are:

1. The choice of the integration solver (Python or Matlab) has no significative impact on the quality of the result of the identification. We can however notice that the loss is usually slightly lower for the Matlab setting but that the coefficients are slightly closer to the truth in the Python setting.

2. There is no significant difference between idetifying the system from a sigle trajectory and from multiple trajectories, at least at the level of the problems we considered.

3. The influence of the integration method on the identification of the system by targetting the next step is not yet understood.


## Code 

```python
cutoff = 1e-1
max_degree = 3
function = 'van_der_pol'
loss = tf.keras.metrics.MeanSquaredError()

data = py_data[function]
derivatives, dm, m = make_targets(data)
derivatives = derivatives/timestep
nb_variables = m.shape[1]
X, nb_funcs = make_polynomials(m, max_degree=max_degree)
weights, iterations = sparse_regression(X, derivatives, cutoff=cutoff)

    
metrics = {'iterations':[iterations],
           'examples':[len(dm)],
           'loss':[loss(derivatives, tf.matmul(X, weights))]} # tf.matmul(X, weights)
params = [[reduce(''.join(name), variables)] + list(val)
          for name, val in zip(combinations_with_replacement(variables[:1 + nb_variables], 5), weights.numpy())]
print('<td>')
print()
print(tabulate(metrics, headers=metrics.keys(), tablefmt="pipe"))
print()
print(tabulate(params, headers=['function', '$\dot{x}$', '$\dot{y}$', '$\dot{z}$'], tablefmt="pipe"))
print()
print('</td>')
```