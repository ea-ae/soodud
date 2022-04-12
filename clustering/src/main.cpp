#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <format>
#include <iostream>
#include <memory>
#include <set>
#include <string>

#include "analyser.h"
#include "matcher.h"
#include "product.h"

namespace py = pybind11;
using namespace py::literals;

int test() {
    auto sp = std::make_unique<StoreProduct>();
    auto sp2 = std::make_unique<StoreProduct>();
    auto sp3 = std::make_unique<StoreProduct>();

    auto p = Product(std::move(sp));
    auto p2 = Product(std::move(sp2));
    auto p3 = Product(std::move(sp3));
    auto p4 = Product(std::move(p), std::move(p2));
    auto p5 = Product(std::move(p3), std::move(p4));
    std::cout << p5.items.size() << "\n";

    // auto analyser = Analyser(std::make_shared<SingleLinkageMatcher>());

    // return analyser;
    return 123;
}

int main() {
    std::cout << "hi\n";
    auto analyser = Analyser();
    analyser.create_product(1, 1, std::set<std::string>{"a", "b", "c", "d", "e", "f"});
    analyser.create_product(2, 2, std::set<std::string>{"a", "b", "c", "d", "1", "2"});
    analyser.create_product(3, 2, std::set<std::string>{"a", "b", "c", "d", "e", "3"});
    analyser.create_product(4, 3, std::set<std::string>{"a", "b", "c", "d", "4", "5"});
    analyser.create_product(5, 1, std::set<std::string>{"x", "y", "z"});
    analyser.create_product(6, 2, std::set<std::string>{"x", "y", "6"});
    analyser.analyse();
    return 0;
}

PYBIND11_MODULE(clustering, m) {
    m.doc() = "Cluster analysis algorithm.";

    m.def("test", &test);

    py::class_<Matcher, std::shared_ptr<Matcher>>(m, "Matcher")
        .def("__repr__", [](const Matcher& o) {
            return "Matcher()";
        });

    py::class_<SingleLinkageMatcher, std::shared_ptr<SingleLinkageMatcher>>(m, "SingleLinkageMatcher")
        .def(py::init<>())
        .def("__repr__", [](const SingleLinkageMatcher& o) {
            return "SingleLinkageMatcher()";
        });

    py::class_<Analyser>(m, "Analyser")
        .def(py::init<std::shared_ptr<SingleLinkageMatcher>, double>(),
             "matcher"_a = std::make_shared<SingleLinkageMatcher>(),
             "threshold"_a = 0.8)
        .def("create_product", &Analyser::create_product)
        .def("analyse", &Analyser::analyse)
        .def("__repr__", [](const Analyser& o) {
            return std::format("Analyser(threshold={}, product_amount={})", o.threshold, o.get_product_amount());
        });

    py::class_<StoreProduct>(m, "StoreProduct")
        .def(py::init<int32_t, int32_t, tokens_t>(),
             "id"_a, "store_id"_a, "tokens"_a = tokens_t{})
        .def_readonly("id", &StoreProduct::id)
        .def_readonly("store_id", &StoreProduct::store_id)
        .def("__repr__", [](const StoreProduct& o) {
            return std::format("StoreProduct(id={}, store_id={})", o.id, o.store_id);
        });
}
