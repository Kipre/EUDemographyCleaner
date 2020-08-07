#include "SysId.hpp"
#include <stdlib.h> /* Just for rand */

#include <iostream>
#include <cstdlib>
#include <time.h>


std::valarray<double> Transpose(std::valarray<double> matrix, int n, int m) {
    
    std::valarray<double> t_matrix (matrix.size());
 
    for (int i = 0; i<n; i++) {
        for (int j = 0; j<m; j++) {
            t_matrix[j * n + i] = matrix[i * m + j];
        }
    }
    return t_matrix;
}

std::valarray<double> MatMul(std::valarray<double> a, std::valarray<double> b, int n, int m) {
    
    std::valarray<double> result (n * m);
    std::size_t shared_dim = a.size()/n;
    if (b.size()/m != shared_dim) {
        std::cout << "Dimensions do not match: " << n << " " << shared_dim << " " << b.size() << " " << m << " " << std::endl;
        throw 1;
    }
    for (int i = 0; i<n; i++) {
        for (int j = 0; j<m; j++) {
            for (int k = 0; k<shared_dim; k++) {
                result[i * m + j] += a[i * shared_dim + k] * b[k * m + j];
            }
        }
    }
    return result;
}
 
 
std::valarray<double> getCofactor(std::valarray<double>  A, int p, int q, int n)
{
    int i = 0, j = 0;
    std::valarray<double> temp ((n-1)*(n-1));

 
    // Looping for each element of the matrix
    for (int row = 0; row < n; row++)
    {
        for (int col = 0; col < n; col++)
        {
            // Copying into temporary matrix only those element
            // which are not in given row and column
            if (row != p && col != q)
            {
                temp[i * (n-1) + j++] = A[row * n + col];
 
                // Row is filled, so increase row index and
                // reset col index
                if (j == n - 1)
                {
                    j = 0;
                    i++;
                }
            }
        }
    }
    return temp;
}
 
// Recursive function for finding determinant of matrix.
double determinant(std::valarray<double> a, int n)
{
    double result = 0; // Initialize result
 
    // Base case : if matrix contains single element
    if (n == 1)
        return a[0];
 
    std::valarray<double> temp ((n-1)*(n-1));
 
    int sign = 1; // To store sign multiplier
 
    // Iterate for each element of first row
    for (int f = 0; f < n; f++)
    {
        // Getting Cofactor of A[0][f]
        temp = getCofactor(a, 0, f, n);
        result += sign * a[0 * n + f] * determinant(temp, n - 1);
 
        // terms are to be added with alternate sign
        sign = -sign;
    }
 
    return result;
}
 
// Function to get adjugate
std::valarray<double> adjugate(std::valarray<double> A, int n)
{
    std::valarray<double> adj (n*n);
    if (n == 1) {
        adj[0] = 1;
        return adj;
    }
 
    // temp is used to store cofactors 
    int sign = 1;
    std::valarray<double> temp ((n-1)*(n-1));
 
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        {
            // Get cofactor
            temp = getCofactor(A, i, j, n);
 
            // sign of adj positive if sum of row
            // and column indexes is even.
            sign = ((i+j)%2==0)? 1: -1;
 
            // Interchanging rows and columns to get the
            // transpose of the cofactor matrix
            adj[j * n + i] = (sign)*(determinant(temp, n-1));
        }
    }
    return adj;
}
 

std::valarray<double> inverse(std::valarray<double> A, int n)
{
    double det = determinant(A, n); 
    if (det == 0)
    {
        std::cout << "Singular matrix, can't find its inverse";
        throw 1;
    }
 
    // Find adjugate
    std::valarray<double> adj = adjugate(A, n);
 
    // Find Inverse using formula "inverse(A) = adj(A)/det(A)"
    return adj/det;
}

std::valarray<double> pseudoinverse(std::valarray<double> A, int n) {

    std::size_t m = A.size()/n;

    std::valarray<double> A_t = Transpose(A, n, m);
    std::valarray<double> product = MatMul(A_t, A, m, m);
    std::valarray<double> inv = inverse(product, m);
    std::valarray<double> result = MatMul(inv, A_t, m, n);
    
    return result;
}
 
std::valarray<double> lstsq(std::valarray<double> a, std::valarray<double> b, int n) {

    std::size_t a_rows = a.size()/n;

    if (a.size() % n != 0) {
        std::cout << "Sizes do not match: " << a.size() << " " << n << std::endl;
        throw 1;
    }
    std::size_t runs = b.size()/n;
    std::valarray<double> result (runs * a_rows);

    for (int run=0; run<runs; run++) {
        result[std::slice(run, a_rows, runs)] = MatMul(pseudoinverse(a, n), b[std::slice(run*n, n, 1)], a_rows, 1);
    }
    
    return result;
}

std::valarray<double> makePolynomials(std::valarray<double> a, int max_degree, int n) {

    std::size_t a_cols = a.size()/n;
    int output_size = fact(a_cols + max_degree)/(fact(max_degree)*fact(a_cols));

    std::valarray<double> result (output_size*n);
    std::valarray<double> current (a_cols + 1);

    for (int i=0; i<n; i++) {
        current[0] = 1;
        current[std::slice(1, a_cols, 1)] = std::valarray(a[std::slice(i*a_cols, a_cols, 1)]);
        std::valarray<double> augmented = CombinationsWithReplacement(current, max_degree);
        result[std::slice(i * output_size, output_size, 1)] = reduceProd(augmented, output_size);
    }
    return result;

}

double prod(std::valarray<double> a) {
    double product = 1;
    for (std::size_t i = 0; i < a.size(); i++) {
        product *= a[i];
    }
    return product;
}


std::valarray<double> reduceProd(std::valarray<double> a, int n) {

    int n_cols = a.size()/n;
    std::valarray<double> result (n);

    for (int k=0; k<n; k++) {
        result[k] = prod(a[std::slice(k*n_cols, n_cols, 1)]);
    }

    return result;

}

int fact(int n) {
    if (n <= 0) {
        return 1;
    } else {
        return fact(n-1) * n;
    }
}

std::valarray<double> CombinationsWithReplacement(std::valarray<double> inputs, int r) {

    std::size_t n = inputs.size();
    int output_size = fact(n + r - 1)/(fact(r)*fact(n-1))*r;

    if (r == 1) {
        return inputs;
    } else if (r < 1) {
        return std::valarray<double> {};
    } else {
        int current_index = 0;
        std::valarray<double> values (output_size);
        for(std::size_t i = 0; i < inputs.size(); ++i) {
            std::valarray<double> result = CombinationsWithReplacement(inputs[std::slice(i, n-i, 1)], r-1); 
            for (std::size_t j = 0; j < result.size(); j += (r-1)) {
                values[current_index++] = inputs[i];
                values[std::slice(current_index, r-1, 1)] = std::valarray(result[std::slice(j, r-1, 1)]);
                current_index += r-1;
            }
        }
        return values;
    }
}

std::valarray<double> sparseRegression(std::valarray<double> a, std::valarray<double> b, double cutoff, int n) {
    std::valarray<double> weights = lstsq(a, b, n);
    std::valarray<double> new_weights (weights.size());

    // for (int i = 0; i < 10; i++) {
    //     std::valarray<double> big_weights = weights[abs(weights) > cutoff];
    //     i++;
    // }
    return weights;
}