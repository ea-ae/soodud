#include <string>
#include <stdint.h>
#include <memory>
#include <optional>


class BaseProduct {
    virtual std::optional<std::string> getName();
    virtual BaseProduct* getLeft();
    virtual BaseProduct* getRight();
};


class StoreProduct : BaseProduct {
    uint32_t id;
    std::string name;

    StoreProduct(uint32_t id, std::string name);
    std::optional<std::string> getName();
};


class Product : BaseProduct {
    std::unique_ptr<BaseProduct> left;
    std::unique_ptr<BaseProduct> right;

    Product(std::unique_ptr<BaseProduct> left, std::unique_ptr<BaseProduct> right);
    BaseProduct* getLeft();
    BaseProduct* getRight();
};
