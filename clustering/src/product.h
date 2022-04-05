#pragma once

#include <stdint.h>

#include <memory>
#include <optional>
#include <set>
#include <string>
#include <vector>

using tokens_t = std::set<std::string>;

class StoreProduct {
   public:
    const int32_t id;
    const std::string name;
    const tokens_t tokens;

    StoreProduct(int32_t id, std::string name, tokens_t tokens = {});
};

class Product {
   public:
    std::vector<std::unique_ptr<const StoreProduct>> items;

    Product();
    Product(std::unique_ptr<const StoreProduct> singleton);
    Product(Product&& first, Product&& second);
    std::size_t hash() const;
};
