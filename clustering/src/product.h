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
    const int32_t store_id;
    const tokens_t tokens;

    StoreProduct();
    StoreProduct(int32_t id, int32_t store_id, tokens_t tokens = {});
};

class Product {
   public:
    std::vector<std::unique_ptr<const StoreProduct>> items;
    bool merged = false;

    Product();
    Product(std::unique_ptr<const StoreProduct> singleton);  // todo: ref it, store elsewhere
    Product(Product&& first, Product&& second);
    std::size_t hash() const;
};

// class Store {
//    public:
//     std::string name;
//     std::vector<std::unique_ptr<Product>> products;
//
//     Store(std::string name);
//     // void add_product();
// };
