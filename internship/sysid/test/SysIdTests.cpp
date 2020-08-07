#include "../SysId.hpp"
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <vector> 
#include <valarray>
  
using namespace testing; 

bool isEqual( const std::valarray< bool >& aResult )
{
    bool equals = true;
    for ( auto item : aResult )
    {
        equals &= item;
    }
    return equals;
}

bool areClose(std::valarray<double> result) {
    if (result.max() > 1e-3) {
        return false;
    } else {
        return true;
    }
}

    const int n_osc = 300;
    const int d_osc = 2;
    const std::valarray<double> cubic_oscillator = {2.00000000e+00,  0.00000000e+00,  1.97136237e+00, -5.24137473e-01,
        1.91253877e+00, -1.01600761e+00,  1.76176527e+00, -1.43206495e+00,
        1.48544077e+00, -1.71337979e+00,  1.09550772e+00, -1.84404249e+00,
        6.61248093e-01, -1.86939775e+00,  2.29160970e-01, -1.85269313e+00,
       -1.89259923e-01, -1.83175754e+00, -5.92257336e-01, -1.80652717e+00,
       -9.70339081e-01, -1.75324600e+00, -1.29502947e+00, -1.63641274e+00,
       -1.53286586e+00, -1.43624235e+00, -1.66858154e+00, -1.15218416e+00,
       -1.71883912e+00, -8.20973730e-01, -1.71741394e+00, -4.80081520e-01,
       -1.70060264e+00, -1.46338203e-01, -1.68432523e+00,  1.78043090e-01,
       -1.66542968e+00,  4.92566576e-01, -1.63171764e+00,  7.92202308e-01,
       -1.56209876e+00,  1.06426660e+00, -1.44174304e+00,  1.28766699e+00,
       -1.26474675e+00,  1.44792164e+00, -1.03490178e+00,  1.54075914e+00,
       -7.76922648e-01,  1.57912871e+00, -5.11494057e-01,  1.58212865e+00,
       -2.49491464e-01,  1.56996062e+00,  6.25825751e-03,  1.55742091e+00,
        2.56027359e-01,  1.54455454e+00,  4.98667212e-01,  1.52844024e+00,
        7.30749317e-01,  1.50072964e+00,  9.44805766e-01,  1.44908756e+00,
        1.12856139e+00,  1.36490426e+00,  1.27280308e+00,  1.24389375e+00,
        1.37266415e+00,  1.08544959e+00,  1.42973564e+00,  8.96802481e-01,
        1.45394708e+00,  6.93994535e-01,  1.45591029e+00,  4.87263719e-01,
        1.44690497e+00,  2.82631811e-01,  1.43704722e+00,  8.21123973e-02,
        1.42718618e+00, -1.14426988e-01,  1.41672686e+00, -3.06894294e-01,
        1.40286381e+00, -4.94150769e-01,  1.38021407e+00, -6.73979045e-01,
        1.34162798e+00, -8.41997106e-01,  1.28216147e+00, -9.91107939e-01,
        1.19897036e+00, -1.11563802e+00,  1.09094557e+00, -1.21196400e+00,
        9.58781790e-01, -1.27854299e+00,  8.09314325e-01, -1.31816564e+00,
        6.51293961e-01, -1.33672438e+00,  4.90384662e-01, -1.34012850e+00,
        3.30280499e-01, -1.33460969e+00,  1.72708819e-01, -1.32668039e+00,
        1.78787419e-02, -1.31905677e+00, -1.34389696e-01, -1.31136908e+00,
       -2.83918940e-01, -1.30314146e+00, -4.30022431e-01, -1.29268694e+00,
       -5.71504607e-01, -1.27710751e+00, -7.06430622e-01, -1.25236969e+00,
       -8.31002110e-01, -1.21507532e+00, -9.41453635e-01, -1.16312529e+00,
       -1.03498506e+00, -1.09524123e+00, -1.10976347e+00, -1.01096297e+00,
       -1.16492314e+00, -9.10648596e-01, -1.20145891e+00, -7.97297739e-01,
       -1.22270652e+00, -6.76601787e-01, -1.23188230e+00, -5.52222440e-01,
       -1.23235096e+00, -4.26883759e-01, -1.22762914e+00, -3.02380700e-01,
       -1.22138540e+00, -1.79579115e-01, -1.21549670e+00, -5.85990022e-02,
       -1.20952412e+00,  6.06717560e-02, -1.20345506e+00,  1.78240452e-01,
       -1.19670593e+00,  2.93874309e-01, -1.18812189e+00,  4.07100467e-01,
       -1.17597690e+00,  5.17205980e-01, -1.15797602e+00,  6.23156474e-01,
       -1.13207330e+00,  7.22899756e-01, -1.09695784e+00,  8.14181270e-01,
       -1.05171137e+00,  8.95196955e-01, -9.95801534e-01,  9.64598987e-01,
       -9.29081852e-01,  1.02149577e+00, -8.51791765e-01,  1.06545196e+00,
       -7.65283457e-01,  1.09683141e+00, -6.73058219e-01,  1.11750457e+00,
       -5.77412062e-01,  1.12925715e+00, -4.80136677e-01,  1.13391993e+00,
       -3.82585532e-01,  1.13339536e+00, -2.85673868e-01,  1.12965751e+00,
       -1.89878697e-01,  1.12475212e+00, -9.52900515e-02,  1.12017807e+00,
       -1.86069028e-03,  1.11553071e+00,  9.04684273e-02,  1.11087990e+00,
        1.81648426e-01,  1.10609272e+00,  2.71517177e-01,  1.10076685e+00,
        3.59799304e-01,  1.09423055e+00,  4.46106176e-01,  1.08554263e+00,
        5.29934569e-01,  1.07348300e+00,  6.10385901e-01,  1.05672377e+00,
        6.86119590e-01,  1.03437840e+00,  7.55956871e-01,  1.00578867e+00,
        8.18934196e-01,  9.70478361e-01,  8.74303225e-01,  9.28153241e-01,
        9.21530837e-01,  8.78701085e-01,  9.60299120e-01,  8.22191666e-01,
        9.90507204e-01,  7.58881025e-01,  1.01275755e+00,  6.90221073e-01,
        1.02816075e+00,  6.18109063e-01,  1.03770092e+00,  5.43766250e-01,
        1.04239596e+00,  4.68207191e-01,  1.04329754e+00,  3.92239753e-01,
        1.04149110e+00,  3.16465104e-01,  1.03809590e+00,  2.41277720e-01,
        1.03426493e+00,  1.66865380e-01,  1.03072098e+00,  9.32470110e-02,
        1.02710589e+00,  2.03970789e-02,  1.02348822e+00, -5.17269871e-02,
        1.01983825e+00, -1.23116591e-01,  1.01599915e+00, -1.93709713e-01,
        1.01168705e+00, -2.63390913e-01,  1.00649097e+00, -3.31991329e-01,
        9.99872868e-01, -3.99288674e-01,  9.91166536e-01, -4.65007728e-01,
        9.79586908e-01, -5.28744116e-01,  9.64558297e-01, -5.89764183e-01,
        9.45660529e-01, -6.47347799e-01,  9.22559265e-01, -7.00876349e-01,
        8.95005997e-01, -7.49832742e-01,  8.62838056e-01, -7.93801407e-01,
        8.25978603e-01, -8.32468294e-01,  7.84436637e-01, -8.65620872e-01,
        7.38306987e-01, -8.93148132e-01,  6.87811857e-01, -9.15058798e-01,
        6.34066891e-01, -9.31858664e-01,  5.78062839e-01, -9.44156231e-01,
        5.20487750e-01, -9.52498861e-01,  4.61932186e-01, -9.57449841e-01,
        4.02889215e-01, -9.59588385e-01,  3.43754417e-01, -9.59509632e-01,
        2.84825883e-01, -9.57824648e-01,  2.26304211e-01, -9.55160423e-01,
        1.68292511e-01, -9.52159873e-01,  1.10804730e-01, -9.49373793e-01,
        5.38355346e-02, -9.46577862e-01, -2.64525495e-03, -9.43759013e-01,
       -5.86507634e-02, -9.40943280e-01, -1.14168915e-01, -9.38096754e-01,
       -1.69162434e-01, -9.35125590e-01, -2.23568844e-01, -9.31876005e-01,
       -2.77300469e-01, -9.28134274e-01, -3.30244432e-01, -9.23626735e-01,
       -3.82262656e-01, -9.18019789e-01, -4.33192687e-01, -9.10917436e-01,
       -4.82788033e-01, -9.01872348e-01, -5.30624460e-01, -8.90573189e-01,
       -5.76292657e-01, -8.76779111e-01, -6.19431199e-01, -8.60289747e-01,
       -6.59726553e-01, -8.40945212e-01, -6.96913075e-01, -8.18626099e-01,
       -7.30773011e-01, -7.93253484e-01, -7.61136497e-01, -7.64788922e-01,
       -7.87881558e-01, -7.33234450e-01, -8.10934110e-01, -6.98632582e-01,
       -8.30267957e-01, -6.61066317e-01, -8.45966575e-01, -6.20796378e-01,
       -8.58417958e-01, -5.78615278e-01, -8.67936114e-01, -5.34991964e-01,
       -8.74826286e-01, -4.90309135e-01, -8.79401221e-01, -4.44903510e-01,
       -8.81981178e-01, -3.99065823e-01, -8.82893923e-01, -3.53040828e-01,
       -8.82474730e-01, -3.07027294e-01, -8.81066383e-01, -2.61178010e-01,
       -8.79019172e-01, -2.15599781e-01, -8.76690898e-01, -1.70353431e-01,
       -8.74446303e-01, -1.25453842e-01, -8.72301821e-01, -8.08987502e-02,
       -8.70113955e-01, -3.66781355e-02, -8.67919820e-01,  7.22482611e-03,
       -8.65728260e-01,  5.08150714e-02, -8.63519847e-01,  9.40856494e-02,
       -8.61246883e-01,  1.37017722e-01, -8.58833399e-01,  1.79580562e-01,
       -8.56175154e-01,  2.21731557e-01, -8.53139638e-01,  2.63416206e-01,
       -8.49566069e-01,  3.04568120e-01, -8.45265393e-01,  3.45109023e-01,
       -8.40020287e-01,  3.84948752e-01, -8.33574969e-01,  4.23975906e-01,
       -8.25723430e-01,  4.61973928e-01, -8.16319646e-01,  4.98700720e-01,
       -8.05236697e-01,  5.33936769e-01, -7.92366754e-01,  5.67485154e-01,
       -7.77621077e-01,  5.99171543e-01, -7.60930021e-01,  6.28844196e-01,
       -7.42243028e-01,  6.56373964e-01, -7.21528634e-01,  6.81654290e-01,
       -6.98774463e-01,  7.04601206e-01, -6.73987233e-01,  7.25153337e-01,
       -6.47192750e-01,  7.43271899e-01, -6.18435914e-01,  7.58940697e-01,
       -5.87790882e-01,  7.72170519e-01, -5.55667521e-01,  7.83143234e-01,
       -5.22429549e-01,  7.92065748e-01, -4.88307589e-01,  7.99105382e-01,
       -4.53510578e-01,  8.04432998e-01, -4.18225761e-01,  8.08222997e-01,
       -3.82618698e-01,  8.10653321e-01, -3.46833260e-01,  8.11905450e-01,
       -3.10991628e-01,  8.12164405e-01, -2.75194297e-01,  8.11618746e-01,
       -2.39520073e-01,  8.10460574e-01, -2.04026074e-01,  8.08885526e-01,
       -1.68747731e-01,  8.07092784e-01, -1.33698783e-01,  8.05285066e-01,
       -9.88754650e-02,  8.03613974e-01, -6.42796879e-02,  8.01928632e-01,
       -2.99005653e-02,  8.00222970e-01,  4.27014530e-03,  7.98514970e-01,
        3.82350786e-02,  7.96809278e-01,  7.19912618e-02,  7.95097208e-01,
        1.05530114e-01,  7.93356736e-01,  1.38837448e-01,  7.91552506e-01,
        1.71893466e-01,  7.89635828e-01,  2.04672766e-01,  7.87544677e-01,
        2.37144335e-01,  7.85203691e-01,  2.69271556e-01,  7.82524178e-01,
        3.01012201e-01,  7.79404109e-01,  3.32318437e-01,  7.75728120e-01,
        3.63137285e-01,  7.71366419e-01,  3.93395439e-01,  7.66170818e-01,
        4.22959499e-01,  7.60038861e-01,  4.51694742e-01,  7.52889370e-01,
        4.79477100e-01,  7.44650171e-01,  5.06193164e-01,  7.35258095e-01,
        5.31740181e-01,  7.24658972e-01,  5.56026055e-01,  7.12807640e-01,
        5.78969348e-01,  6.99667938e-01,  6.00499277e-01,  6.85212709e-01,
        6.20555717e-01,  6.69423799e-01,  6.39089202e-01,  6.52292056e-01,
        6.56060921e-01,  6.33817335e-01,  6.71442719e-01,  6.14008491e-01,
        6.85217101e-01,  5.92883384e-01,  6.97377226e-01,  5.70468876e-01,
        7.07926917e-01,  5.46800843e-01,  7.16950744e-01,  5.22078751e-01,
        7.24584359e-01,  4.96563750e-01,  7.30920159e-01,  4.70389735e-01,
        7.36052211e-01,  4.43680369e-01,  7.40076250e-01,  4.16549087e-01,
        7.43089680e-01,  3.89099093e-01,  7.45191572e-01,  3.61423363e-01,
        7.46482668e-01,  3.33604643e-01,  7.47065377e-01,  3.05715448e-01,
        7.47043779e-01,  2.77818067e-01,  7.46523619e-01,  2.49964555e-01,
        7.45612315e-01,  2.22196742e-01,  7.44418950e-01,  1.94546224e-01,
        7.43054277e-01,  1.67034373e-01,  7.41630718e-01,  1.39672325e-01,
        7.40262364e-01,  1.12460993e-01,  7.38973945e-01,  8.53980776e-02,
        7.37659316e-01,  5.84848005e-02,  7.36331840e-01,  3.17140029e-02,
        7.35001959e-01,  5.08091232e-03,  7.33673826e-01, -2.14165982e-02,
        7.32345304e-01, -4.77780104e-02,  7.31007967e-01, -7.40001606e-02,
        7.29647099e-01, -1.00077240e-01,  7.28241696e-01, -1.26000794e-01,
        7.26764463e-01, -1.51759723e-01,  7.25181817e-01, -1.77340282e-01,
        7.23453885e-01, -2.02726081e-01,  7.21534504e-01, -2.27898085e-01,
        7.19371224e-01, -2.52834612e-01,  7.16905302e-01, -2.77511336e-01,
        7.14071708e-01, -3.01901285e-01,  7.10799123e-01, -3.25974843e-01,
        7.06990657e-01, -3.49696688e-01,  7.02570628e-01, -3.72998856e-01,
        6.97500821e-01, -3.95803899e-01,  6.91746139e-01, -4.18039446e-01,
        6.85274582e-01, -4.39638213e-01,  6.78057253e-01, -4.60537998e-01,
        6.70068352e-01, -4.80681685e-01,  6.61285180e-01, -5.00017241e-01,
        6.51688136e-01, -5.18497718e-01,  6.41260721e-01, -5.36081249e-01,
        6.29989535e-01, -5.52731055e-01,  6.17864277e-01, -5.68415439e-01,
        6.04877746e-01, -5.83107787e-01,  5.91025843e-01, -5.96786573e-01,
        5.76307564e-01, -6.09435350e-01,  5.60725009e-01, -6.21042758e-01,
        5.44283376e-01, -6.31602522e-01,  5.26990963e-01, -6.41113448e-01,
        5.08859168e-01, -6.49579428e-01,  4.89902488e-01, -6.57009437e-01};



// TEST(SysIdTests, CombinationsWithReplacement) {
    
//     std::vector<int> input {1, 2, 3};
//     std::vector<int> result = CombinationsWithReplacement(input, 2);

//     ASSERT_THAT(result, ElementsAre(1, 1, 1, 2, 1, 3, 2, 2, 2, 3, 3, 3));
    
//     std::vector<float> floatInput {1.2, 3.2};
//     std::vector<float> floatResult = CombinationsWithReplacement(floatInput, 3);

//     ASSERT_THAT(floatResult, ElementsAre(1.2, 1.2, 1.2, 1.2, 1.2, 3.2, 1.2, 3.2, 3.2, 3.2, 3.2, 3.2));

//     std::vector<char> charInput {'a', 'b', 'c'};
//     std::vector<char> charResult = CombinationsWithReplacement(charInput, 2);

//     ASSERT_THAT(charResult, ElementsAre('a', 'a', 'a', 'b', 'a', 'c', 'b', 'b', 'b', 'c', 'c', 'c'));

//     std::vector<int> fiveInput {1, 2, 3};
//     std::vector<int> fiveResult = CombinationsWithReplacement(fiveInput, 5);

//     ASSERT_THAT(fiveResult, ElementsAre(1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 2, 2,
//      1, 1, 1, 2, 3, 1, 1, 1, 3, 3, 1, 1, 2, 2, 2, 1, 1, 2, 2, 3, 1, 1, 2, 3, 3, 1, 1, 3, 3, 3, 1, 2,
//      2, 2, 2, 1, 2, 2, 2, 3, 1, 2, 2, 3, 3, 1, 2, 3, 3, 3, 1, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2,
//      3, 2, 2, 2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3));

//     std::vector<char> emptyInput {};
//     std::vector<char> emptyResult = CombinationsWithReplacement(emptyInput, 2);

//     ASSERT_THAT(emptyResult, ElementsAre());

//     std::vector<char> nullInput {'a', 'b', 'c'};
//     std::vector<char> nullResult = CombinationsWithReplacement(nullInput, 0);

//     ASSERT_THAT(nullResult, ElementsAre());
// }

TEST(SysIdTests, CombinationsWithReplacement2) {
    
    std::valarray<double> input {1, 2, 3};
    std::valarray<double> result = CombinationsWithReplacement(input, 2);
    std::valarray<double> expected {1, 1, 1, 2, 1, 3, 2, 2, 2, 3, 3, 3};

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_EQ(result.size(), expected.size());
    EXPECT_TRUE(isEqual(result == expected));
}

TEST(SysIdTests, CombinationsWithReplacement3) {
    
    std::valarray<double> input {1, 1, 2};
    std::valarray<double> result = CombinationsWithReplacement(input, 3);
    std::valarray<double> expected {1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2};

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_EQ(result.size(), expected.size());
    EXPECT_TRUE(isEqual(result == expected));
}



TEST(SysIdTests, Transpose) {

    std::valarray<double> a = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0};
    std::valarray<double> expected = {1.0, 4.0, 2.0, 5.0, 3.0, 6.0};
    std::valarray<double> expectedC = {1.0, 3.0, 5.0, 2.0, 4.0, 6.0};


    std::valarray<double> b = Transpose(a, 2, 3);
    std::valarray<double> c = Transpose(a, 3, 2);

    std::cout << "b contains:";
    for (auto it = begin(b); it!=end(b); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_TRUE(isEqual(expected == b));
    EXPECT_TRUE(isEqual(expectedC == c));
}

TEST(SysIdTests, MatMul) {
    
    std::valarray<double> a = {1, 2, 3, 4};
    std::valarray<double> b = {2, 1, 4, 3};
    std::valarray<double> expected = {10, 7, 22, 15};
    std::valarray<double> expected2 = {28};

    std::valarray<double> result = MatMul(a, b, 2, 2);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_TRUE(isEqual(expected == result));

    EXPECT_TRUE(isEqual(expected2 == MatMul(a, b, 1, 1)));
}

TEST(SysIdTests, MatMul2) {

    std::valarray<double> A = {1, 2, 3, 4, 5, 6};
    std::valarray<double> At = {1, 3, 5, 2, 4, 6};
    std::valarray<double> expected = {35, 44, 44, 56};

    std::valarray<double> result = MatMul(At, A, 2, 2);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_TRUE(isEqual(expected == result));
}

TEST(SysIdTests, getCofactor) {
    std::valarray<double> a = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    std::valarray<double> expected = {1, 3, 7, 9};

    std::valarray<double> result = getCofactor(a, 1, 1, 3);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_TRUE(isEqual(expected == result));

}

TEST(SysIdTests, determinant) {
    std::valarray<double> a = {1, 2, 3, 4};
    EXPECT_EQ(determinant(a, 2), -2);

    std::valarray<double> b = {1, 2, 3, 4, 5, 6, 2, 8, 9};
    EXPECT_EQ(determinant(b, 3), 15);

    std::valarray<double> c = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    EXPECT_EQ(determinant(c, 3), 0);
}

TEST(SysIdTests, adjugate) {
    std::valarray<double> a = {1, 2, 3, 4};
    std::valarray<double> expected = {4, -2, -3, 1};
    std::valarray<double> result = adjugate(a, 2);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_TRUE(isEqual(result == expected));

}

TEST(SysIdTests, inverse) {
    
    std::valarray<double> a = {1, 2, 3, 4};
    std::valarray<double> expected = {-2, 1, 1.5, -0.5};
    std::valarray<double> result = inverse(a, 2);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_TRUE(isEqual(result == expected));
}


TEST(SysIdTests, pseudoinverse) {
    
    std::valarray<double> a = {1, 2, 3, 4, 5, 6};
    std::valarray<double> expected = {-1.33333, -0.333333, 0.666667, 1.08333, 0.333333, -0.416667};
    std::valarray<double> result = pseudoinverse(a, 3);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_TRUE(areClose(abs(result - expected)));
}

TEST(SysIdTests, lstsq) {
    std::valarray<double> a = {1, 2, 3, 4, 5, 6};
    std::valarray<double> b = {3, 4, 5};
    std::valarray<double> expected = {-2, 2.5};
    std::valarray<double> result = lstsq(a, b, 3);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_EQ(result.size(), expected.size());
    EXPECT_TRUE(areClose(abs(result - expected)));
}

TEST(SysIdTests, lstsq2) {
    std::valarray<double> a = {1, 2, 3, 4, 5, 6};
    std::valarray<double> b = {3, 4, 5, 0.1, 0.3, 0.22};
    std::valarray<double> expected = {-2, -0.08666667, 2.5, 0.11666667};
    std::valarray<double> result = lstsq(a, b, 3);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_EQ(result.size(), expected.size());
    EXPECT_TRUE(areClose(abs(result - expected)));
}

TEST(SysIdTests, makePolynomials) {
    
    std::valarray<double> a = {1, 2, 3, 4, 5, 6};
    std::valarray<double> expected = {1., 1., 2., 1., 2., 4., 1., 2., 4., 8., 1., 3., 4., 9., 12., 16., 27., 36., 48., 64., 1., 5., 6., 25., 30., 36., 125., 150., 180., 216.};
    std::valarray<double> result = makePolynomials(a, 3, 3);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_EQ(result.size(), expected.size());
    EXPECT_TRUE(areClose(abs(result - expected)));


}

TEST(SysIdTests, reduceProd) {
    
    std::valarray<double> a = {1, 2, 3, 4, 5, 6};
    std::valarray<double> expected = {2, 12, 30};
    std::valarray<double> result = reduceProd(a, 3);

    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_EQ(result.size(), expected.size());
    EXPECT_TRUE(isEqual(result == expected));
}

TEST(SysIdTests, prod) {
    
    std::valarray<double> a = {1, 2, 3, 4};
    double expected = 24;
    EXPECT_EQ(prod(a), expected);
}

TEST(SysIdTests, sparseRegression) {

    std::valarray<double> x = cubic_oscillator[std::slice(0, (n_osc-1)*d_osc, 1)];
    std::valarray<double> targets = cubic_oscillator[std::slice(d_osc, (n_osc-1)*d_osc, 1)];

    int n = n_osc - d_osc;

    std::valarray<double> augmented = makePolynomials(x, 3, n);
    
    std::valarray<double> expected = {};

    std::valarray<double> result = sparseRegression(augmented, targets, 4e-3, n);


    std::cout << "result contains:";
    for (auto it = begin(result); it!=end(result); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    EXPECT_EQ(result.size(), expected.size());
}