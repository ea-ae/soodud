#pragma once

#include <stdint.h>

#include <memory>
#include <optional>
#include <string>

class BaseProduct {
    virtual std::optional<uint32_t> getId();
    virtual std::optional<std::string> getName();
    virtual BaseProduct* getLeft();
    virtual BaseProduct* getRight();
};

class StoreProduct : BaseProduct {
   public:
    uint32_t id;  // public fields due to pybind STL property issues
    std::string name;

    StoreProduct(uint32_t id, std::string name);
    std::optional<uint32_t> getId();
    std::optional<std::string> getName();
};

class Product : BaseProduct {
   public:
    std::unique_ptr<BaseProduct> left;
    std::unique_ptr<BaseProduct> right;

    Product(std::unique_ptr<BaseProduct> left, std::unique_ptr<BaseProduct> right);
    BaseProduct* getLeft();
    BaseProduct* getRight();
};
