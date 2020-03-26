%% Time steps
t = linspace(0, 10, 300)

%% Functions and initial values
linear_oscillator_f = @(t,y) [-0.1*y(1) + 2*y(2); -2*y(1) - 0.1*y(2)];
linear_oscillator_initial = [2, 0];

cubic_oscillator_f = @(t,y) [-0.1*y(1)**3 + 2*y(2)**3; -2*y(1)**3 - 0.1*y(2)**3];
cubic_oscillator_initial = [2, 0];

oscillator_3d_f = @(t,y) [-0.1*y(1) + 2*y(2); -2*y(1) - 0.1*y(2); -0.3*y(3)];
oscillator_3d_initial = [1, 0, 1];

% sigma=10, beta=8/3, rho=28
lorenz_f= @(t,y) [10*(y(2) - y(1)); y(1)*(28 - y(3)) - y(2); -(8/3)*y(3) + y(2)*y(1)];
lorenz_initial = [-8, 7, 27];

% mu=-0.01, omega=9, lambda=0.01, A=-0.01
mean_field_f = @(t,y) [-0.01*y(1) - 9*y(2) + -0.01*y(1)*y(3); 9*y(1) + -0.01*y(2) + -0.01*y(2)*y(3); - 0.01*(y(3) - y(1)^2 - y(2)^2)];
mean_field_initial = [-100, 0, 0];

van_der_pol_f = @(t,y) [y(2); (1 - y(1)^2) * y(2) - y(1)];
van_der_pol_initial = [2, 0];

%% Integration
[t0,linear_oscillator] = ode45(linear_oscillator_f, t, linear_oscillator_initial);
[t0,cubic_oscillator] = ode45(cubic_oscillator_f, t, cubic_oscillator_initial);
[t0,oscillator_3d] = ode45(oscillator_3d_f, t, oscillator_3d_initial);
[t0,lorenz] = ode45(lorenz_f, t, lorenz_initial);
[t0,mean_field] = ode45(mean_field_f, t, mean_field_initial);
[t0,van_der_pol] = ode45(van_der_pol_f, t, van_der_pol_initial);

save('oct_odes.mat', 
     'linear_oscillator',
     'cubic_oscillator',
     'oscillator_3d',
     'lorenz',
     'mean_field',
     'van_der_pol',
     version='-v4')
