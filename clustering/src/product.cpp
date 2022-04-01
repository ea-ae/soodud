#include "product.h"

StoreProduct::StoreProduct(int32_t id, std::string name) : id(id), name(name) {}

int32_t StoreProduct::getId() const {
    return this->id;
}

std::string StoreProduct::getName() const {
    return this->name;
}

std::vector<StoreProduct> StoreProduct::linearize() const {
    return std::vector<StoreProduct>{*this};
}

Product::Product(std::unique_ptr<BaseProduct> left, std::unique_ptr<BaseProduct> right)
    : left(std::move(left)), right(std::move(right)) {}

BaseProduct* Product::getLeft() const {
    return this->left.get();
}

BaseProduct* Product::getRight() const {
    return this->right.get();
}

std::vector<StoreProduct> Product::linearize() const {
    auto merged = this->getLeft()->linearize();
    auto second = this->getRight()->linearize();
    merged.insert(merged.end(), second.begin(), second.end());
    return merged;
}
