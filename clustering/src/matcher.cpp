#include "matcher.h"

#include <stdint.h>

#include <algorithm>
#include <execution>

double Matcher::match_products(const StoreProduct& a, const StoreProduct& b) const {
    double quantity_matches = 0;  // the more quantities match, the higher the score
    for (auto& a_qty : a.quantities) {
        auto b_qty = std::find_if(b.quantities.begin(), b.quantities.end(),
                                  [a_qty](quantity_t q) { return a_qty.second == q.second; });
        if (b_qty != b.quantities.end()) {
            quantity_matches++;
            if (a_qty.first != b_qty->first && a_qty.second == b_qty->second)
                return -1;  // product quantities are non-matching
        }
    }

    // e.g. match {6l, 3tk} with {6l, 3tk} over {6l, 5%}
    auto higher_quantity = std::max<size_t>(a.quantities.size(), b.quantities.size());
    auto quantity_score = higher_quantity == 0 ? 1.0 : quantity_matches / higher_quantity;

    double matches = std::count_if(std::execution::par_unseq, a.tokens.begin(), a.tokens.end(),
                                   [&b](std::string i) {
                                       return std::find(b.tokens.begin(), b.tokens.end(), i) != b.tokens.end();
                                   });

    auto sizes = std::minmax<size_t>(a.tokens.size(), b.tokens.size());
    if (sizes.first == 0) {  // ignore matches with zero tokens
        return -1;
    }

    auto token_score = matches / ((sizes.first >= 4) ? sizes.first : sizes.second);
    return 0.8 * token_score + 0.2 * quantity_score;  // todo: reserve 0.01 for 100% product code matches
}

double SingleLinkageMatcher::match(const Product& a, const Product& b) const {
    if (a.merged || b.merged) return 0;

    double most_similar = 0;
    for (const auto& a_product : a.items) {
        for (const auto& b_product : b.items) {
            if (a_product->store_id == b_product->store_id) return 0;
            if (a_product->barcode != "" && b_product->barcode != "") {  // proceed with EAN match
                return a_product->barcode == b_product->barcode ? 999 : 0;
            }

            double new_match = this->match_products(*a_product, *b_product);
            if (new_match == -1) return 0;

            most_similar = std::max<double>(most_similar, new_match);
        }
    }
    return most_similar;
}
