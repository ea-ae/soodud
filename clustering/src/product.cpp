#include "product.h"

StoreProduct::StoreProduct(int32_t id, std::string name) : id(id), name(name) {}

Product::Product() {}

Product::Product(std::unique_ptr<StoreProduct> singleton) {
    items.push_back(std::move(singleton));
}

Product::Product(Product&& first, Product&& second) {
    this->items = std::move(first.items);
    this->items.insert(
        this->items.end(),
        std::make_move_iterator(second.items.begin()),
        std::make_move_iterator(second.items.end()));
}
