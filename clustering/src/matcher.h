#pragma once

#include <memory>
#include <set>
#include <string>

#include "product.h"

class Matcher {
   public:
    double match_tokens(const tokens_t& a, const tokens_t& b) const;
    virtual double match(const Product& a, const Product& b) const = 0;
};

class SingleLinkageMatcher : public Matcher {
   public:
    // double match(std::vector<std::string> a, std::vector<std::string> b);
    double match(const Product& a, const Product& b) const;
};
