#include "product.h"

StoreProduct::StoreProduct(int32_t id, std::string name, tokens_t)
    : id(id), name(name), tokens(tokens) {}

Product::Product() {}

Product::Product(std::unique_ptr<const StoreProduct> singleton) {
    items.push_back(std::move(singleton));
}

Product::Product(Product&& first, Product&& second) {
    items = std::move(first.items);
    items.insert(
        items.end(),
        std::make_move_iterator(second.items.begin()),
        std::make_move_iterator(second.items.end()));
}

#pragma warning(push)
#pragma warning(disable : 26451)
// stackoverflow.com/a/27216842/4362799
std::size_t Product::hash() const {
    std::size_t seed = items.size();
    for (auto& item : items) {
        seed ^= item.get()->id + 0x9e3779b9 + (seed << 6) + (seed >> 2);
    }
    return seed;
}
#pragma warning(pop)

// Store::Store(std::string name, std::vector<std::unique_ptr<Product>> products)
//     : name(name), products(products) {}
