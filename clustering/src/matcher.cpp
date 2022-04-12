#include "matcher.h"

#include <stdint.h>

#include <algorithm>
#include <execution>
//#include <numeric>

double Matcher::match_tokens(const tokens_t& a, const tokens_t& b) const {
    // todo: quantity check
    double matches = std::count_if(std::execution::par_unseq, a.begin(), a.end(),
                                   [&b](std::string i) { return b.find(i) != b.end(); });
    double shorter = std::min<size_t>(a.size(), b.size());

    if (shorter == 0) {
        return 0;
    }

    return matches / ((shorter >= 4) ? shorter : std::max<size_t>(a.size(), b.size()));
}

double SingleLinkageMatcher::match(const Product& a, const Product& b) const {
    double most_similar = 0;
    for (const auto& a_product : a.items) {
        for (const auto& b_product : b.items) {
            double new_match = this->match_tokens(a_product->tokens, b_product->tokens);
            most_similar = std::max<double>(most_similar, new_match);
        }
    }
    return most_similar;
}
