#include "matcher.h"

#include <stdint.h>

#include <algorithm>
#include <execution>
//#include <numeric>

double Matcher::match_tokens(const tokens_t& a, const tokens_t& b) const {
    // todo: quantity check
    auto matches = std::count_if(std::execution::par_unseq, a.cbegin(), a.cend(),
                                 [&b](std::string i) { return b.find(i) != b.end(); });
    auto shorter = std::min<size_t>(a.size(), b.size());
    return matches / ((shorter >= 4) ? shorter : std::max<size_t>(a.size(), b.size()));
}

double SingleLinkageMatcher::match(const Product& a, const Product& b) const {
    double most_similar = 0;
    for (const auto& a_product : a.items) {
        for (const auto& b_product : b.items) {
            most_similar = std::max<double>(most_similar, this->match_tokens(a_product->tokens, b_product->tokens));
        }
    }
    return most_similar;
}
