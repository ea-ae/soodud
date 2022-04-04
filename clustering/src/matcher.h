#pragma once

#include <memory>
#include <string>
#include <unordered_set>

#include "product.h"

class Matcher {
   public:
    double match(std::unordered_set<std::string> a, std::unordered_set<std::string> b);
    virtual double match(Product& a, Product& b) = 0;
};

class SingleLinkageMatcher : public Matcher {
   public:
    // double match(std::vector<std::string> a, std::vector<std::string> b);
    double match(Product& a, Product& b);
};
