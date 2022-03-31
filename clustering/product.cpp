#include "product.h"


std::optional<std::string> BaseProduct::getName() {
    return {};
}

BaseProduct* BaseProduct::getLeft() {
    return nullptr;
}

BaseProduct* BaseProduct::getRight() {
    return nullptr;
}


StoreProduct::StoreProduct(uint32_t id, std::string name) : id(id), name(name) {}

std::optional<std::string> StoreProduct::getName() {
    return this->name;
}


BaseProduct* Product::getLeft() {
    return this->left.get();
}

BaseProduct* Product::getRight() {
    return this->right.get();
}
