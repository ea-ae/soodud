#include "matcher.h"

#include <stdint.h>

#include <algorithm>

double Matcher::match(std::unordered_set<std::string> a, std::unordered_set<std::string> b) {
    // todo: quantity check
    auto matches = std::count_if(a.begin(), a.end(), [&b](std::string i) { return b.find(i) != b.end(); });
    auto shorter = std::min<size_t>(a.size(), b.size());
    return matches / ((shorter >= 4) ? shorter : std::max<size_t>(a.size(), b.size()));
}

double SingleLinkageMatcher::match(Product& a, Product& b) {
    return 0.2;
}
