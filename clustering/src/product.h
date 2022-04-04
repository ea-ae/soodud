#pragma once

#include <stdint.h>

#include <memory>
#include <optional>
#include <string>
//#include <unordered_map>
#include <vector>

class StoreProduct {
   public:
    const int32_t id;
    const std::string name;

    StoreProduct(int32_t id, std::string name);
};

class Product {
   public:
    std::vector<std::unique_ptr<StoreProduct>> items;
    // std::unordered_map<int32_t, double> cached_matches;

    Product();
    Product(std::unique_ptr<StoreProduct> singleton);
    Product(Product&& first, Product&& second);
    std::size_t hash() const;
};
