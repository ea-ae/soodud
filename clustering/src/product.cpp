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

#pragma warning(push)
#pragma warning(disable : 26451)
// stackoverflow.com/a/27216842/4362799
std::size_t Product::hash() const {
    std::size_t seed = this->items.size();
    for (auto& item : this->items) {
        seed ^= item.get()->id + 0x9e3779b9 + (seed << 6) + (seed >> 2);
    }
    return seed;
}
#pragma warning(pop)
