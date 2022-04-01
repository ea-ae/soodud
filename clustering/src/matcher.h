#pragma once

#include <string>

#include "product.h"

class Matcher {
   public:
    double match(std::string a, std::string b);
    virtual double match(Product a, Product b) = 0;
};

class SingleLinkageMatcher : public Matcher {
   public:
    // double match(std::string a, std::string b);
    double match(Product a, Product b);
};
