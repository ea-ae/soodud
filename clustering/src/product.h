#pragma once

#include <stdint.h>

#include <memory>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

class StoreProduct;

class BaseProduct {
   public:
    virtual std::vector<StoreProduct> linearize() const = 0;

   private:
    virtual int32_t getId() const = 0;
    virtual std::string getName() const = 0;
    virtual BaseProduct* getLeft() const = 0;
    virtual BaseProduct* getRight() const = 0;
};

class StoreProduct : public BaseProduct {
   public:
    const int32_t id;  // public fields due to pybind STL property issues
    const std::string name;

    StoreProduct(int32_t id, std::string name);
    int32_t getId() const;
    std::string getName() const;
    std::vector<StoreProduct> linearize() const;
};

class Product : public BaseProduct {
   public:
    const std::unique_ptr<BaseProduct> left;
    const std::unique_ptr<BaseProduct> right;

    Product(std::unique_ptr<BaseProduct> left, std::unique_ptr<BaseProduct> right);
    BaseProduct* getLeft() const;
    BaseProduct* getRight() const;
    std::vector<StoreProduct> linearize() const;
};
