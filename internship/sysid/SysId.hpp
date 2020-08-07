#include <vector>
#include <valarray>
#ifndef SYSID_HPP
#define SYSID_HPP

// template <typename G>
// std::vector<G> CombinationsWithReplacement(std::vector<G> inputs, int number) {
//     if (number == 1) {
//         return inputs;
//     } else if (number < 1) {
//         return std::vector<G>();
//     } else {
//         std::vector<G> values {};
//         for(std::size_t i = 0; i < inputs.size(); ++i) {
//             std::vector<G> slice = std::vector<G>(inputs.begin() + i, inputs.end());
//             std::vector<G> result = CombinationsWithReplacement(slice, number-1);
//             for (std::size_t j = 0; j < result.size(); j += (number-1)) {
//                 values.push_back(inputs[i]);
//                 std::vector<G> subslice = std::vector<G>(result.begin() + j, result.begin() + j + (number-1));
//                 values.reserve(values.size() + distance(subslice.begin(), subslice.end()));
//                 values.insert(values.end(), subslice.begin(), subslice.end());
//             }
//         }
//         return values;
//     }
// }


std::valarray<double> Transpose(std::valarray<double> matrix, int m, int n);
std::valarray<double> MatMul(std::valarray<double> a, std::valarray<double> b, int n, int m);
std::valarray<double> getCofactor(std::valarray<double>  A, int p, int q, int n);
double determinant(std::valarray<double> a, int n);
std::valarray<double> adjugate(std::valarray<double> A, int n);
std::valarray<double> inverse(std::valarray<double> A, int n);
std::valarray<double> pseudoinverse(std::valarray<double> A, int n);
std::valarray<double> lstsq(std::valarray<double> a, std::valarray<double> b, int n);
std::valarray<double> makePolynomials(std::valarray<double> a, int max_degree, int n);
int fact(int n);
std::valarray<double> CombinationsWithReplacement(std::valarray<double> inputs, int r);
std::valarray<double> reduceProd(std::valarray<double> a, int n);
double prod(std::valarray<double> a);
std::valarray<double> sparseRegression(std::valarray<double> a, std::valarray<double> b, double cutoff, int n);

#endif /* SYSID_HPP */
