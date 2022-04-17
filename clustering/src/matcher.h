#pragma once

#include <memory>
#include <set>
#include <string>

#include "product.h"

class Matcher {
   public:
    Matcher() = default;
    virtual ~Matcher() = default;

    virtual double match(const Product& a, const Product& b) const = 0;

   protected:
    double match_products(const StoreProduct& a, const StoreProduct& b) const;
};

class SingleLinkageMatcher : public Matcher {
   public:
    SingleLinkageMatcher() = default;

    double match(const Product& a, const Product& b) const;
};
