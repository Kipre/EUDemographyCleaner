# System identification including a time variable

## Introduction

In this we want to study how including a time variable in our dynamics will change the identification. Our goal is to find a function $f$ so that the the number of cumulative cases in a given country $\mathbf{x}$ verifies the following ODE: 

$$\mathbf{x}_{t+1} = f(\mathbf{x}_t, t)$$

The idea behind this model is that the systems that we study include lots of time-dependent characteristics. For example, modeling the COVID evolutions with a simple SIR model without time-dependent parameters gives very poor results while having an $R_0$ value with just three different values as a staircase function gives much better fitting. 

## Implementation


We just add a variable $t$ to the system of variables so that our state is $\mathbf{x_t} = (x_t, t)$ and our observed data becomes:

$$X = 
\begin{bmatrix}
x_0 & 0 \\
x_1 & 1 \\
x_2 & 2 \\
\vdots \\
x_m & m
\end{bmatrix}
$$

In this setting, if we use polynomial terms as candidate functions we will have the following kind of terms $(1, x, t, x^2, xt, t^2, x^3, x^2t, \dots)$

## Visual results

