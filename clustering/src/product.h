#pragma once

#include <stdint.h>

#include <memory>
#include <optional>
#include <set>
#include <string>
#include <utility>
#include <vector>

using tokens_t = std::vector<std::string>;
using quantity_t = std::pair<double, std::string>;
using quantities_t = std::set<quantity_t>;

class StoreProduct {
   public:
    const int32_t id;
    const int32_t store_id;
    const std::string barcode;
    const tokens_t tokens;
    const quantities_t quantities;

    StoreProduct();

    StoreProduct(int32_t id, int32_t store_id, std::string barcode, tokens_t tokens = {}, quantities_t quantities = {});
};

class Product {
   public:
    bool merged = false;
    std::vector<std::shared_ptr<StoreProduct>> items;

    Product();
    Product(std::shared_ptr<StoreProduct> singleton);  // todo: ref it, store elsewhere
    Product(Product&& first, Product&& second);

    std::vector<StoreProduct*> get_items();
};
