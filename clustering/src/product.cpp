#include "product.h"

StoreProduct::StoreProduct() : StoreProduct(0, 0) {}

StoreProduct::StoreProduct(int32_t id, int32_t store_id, tokens_t tokens, quantities_t quantities)
    : id(id), store_id(store_id), tokens(tokens), quantities(quantities) {}

Product::Product() {}

Product::Product(std::unique_ptr<StoreProduct> singleton) {
    items.push_back(std::move(singleton));
}

Product::Product(Product&& first, Product&& second) {
    items = std::move(first.items);
    items.insert(
        items.end(),
        std::make_move_iterator(second.items.begin()),
        std::make_move_iterator(second.items.end()));
}

std::vector<StoreProduct*> Product::get_items() {
    std::vector<StoreProduct*> raw_items;
    for (auto& item : items) {
        raw_items.push_back(item.get());
    }
    return raw_items;
}
