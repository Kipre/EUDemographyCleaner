I documented myself on how MATLAB does for input/output and apparently the two build-in functions `save` and `load` are exactly for this purpose.
So I went ahead and used this format to store all the different values we talked about.
If you feel like this is not a good idea just tell me and I will send all the data as comma-separated values as you suggested.
Also I dont think we talked about what exact network to use so I ran everything on the Greece network but it can be done for any of them.

The `network.mat` file contains all the information about the network:
 - `incidence_matrix`
 - `roughness`
 - `diameter`
 - `temperature`
 - `pressure_min`
 - `pressure_max`
 - `height`

And two additionnal arrays of chars: `nodes_order` and `connections_order`. 
Those two arrays list the nodes and the connections in the right order so that you can check to which id a parameter belongs.
For example if you want to find the connection at index 3: `connections_order(3, :)` will give you the id `node_11_ld5`.

As for the scenarios, I put a big matrix `scenarios` $\in \mathbb{R}^{|scenarios| \times |nodes|}$ in the `scenarios.mat` file where the $i$th row is the scenario from the file called by the name on the $i$th row of the `scenarios_order` char array.
And each column corresponds to a node in the same order as before. 
The inputs are the negative values.

For the `scenario-v2.mat` file everything is the same. Beware that the variables names inside both of the scenarios files are the same.

I tried to load the data in octave and it worked fine for me.

