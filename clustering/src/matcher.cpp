#include "matcher.h"

#include <stdint.h>

#include <algorithm>
#include <execution>

double Matcher::match_products(const StoreProduct& a, const StoreProduct& b) const {
    for (auto a_qty : a.quantities) {
        auto b_qty = std::find_if(b.quantities.begin(), b.quantities.end(),
                                  [a_qty](quantity_t q) { return a_qty.second == q.second; });
        if (b_qty != b.quantities.end() && a_qty.first != b_qty->first && a_qty.second == b_qty->second) {
            return 0;  // product quantities are non-matching
        }
    }

    double matches = std::count_if(std::execution::par_unseq, a.tokens.begin(), a.tokens.end(),
                                   [&b](std::string i) { return b.tokens.find(i) != b.tokens.end(); });

    auto sizes = std::minmax<size_t>(a.tokens.size(), b.tokens.size());

    if (sizes.first == 0) {  // ignore matches with zero tokens
        return 0;
    }

    return matches / ((sizes.first >= 4) ? sizes.first : sizes.second);
}

double SingleLinkageMatcher::match(const Product& a, const Product& b) const {
    if (a.merged || b.merged) return 0;

    double most_similar = 0;
    for (const auto& a_product : a.items) {
        for (const auto& b_product : b.items) {
            if (a_product->store_id == b_product->store_id) return 0;

            double new_match = this->match_products(*a_product, *b_product);
            most_similar = std::max<double>(most_similar, new_match);
        }
    }
    return most_similar;
}
