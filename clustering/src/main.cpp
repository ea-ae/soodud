//#include <pybind11/pybind11.h>
//#include <pybind11/stl.h>

#include <format>
#include <iostream>
#include <memory>
#include <set>
#include <string>

#include "analyser.h"
#include "matcher.h"
#include "product.h"

// namespace py = pybind11;
// using namespace py::literals;

int main() {
    using q = std::pair<int32_t, std::string>;
    auto q1 = quantities_t{q{3, "kg"}, q{2, "tk"}};
    auto q2 = quantities_t{q{2, "kg"}, q{55, "%"}};

    auto analyser = Analyser();
    analyser.create_product(1, 1, std::set<std::string>{"a", "b", "c", "d", "e", "f"}, q1);
    analyser.create_product(2, 10, std::set<std::string>{"a", "b", "c", "d", "e", "f"}, q2);
    analyser.create_product(3, 2, std::set<std::string>{"a", "b", "c", "d", "1", "2"});
    analyser.create_product(4, 2, std::set<std::string>{"a", "b", "c", "d", "e", "3"}, q1);
    analyser.create_product(5, 3, std::set<std::string>{"a", "b", "c", "d", "4", "5"});
    analyser.create_product(6, 1, std::set<std::string>{"x", "y", "z"});
    analyser.create_product(7, 2, std::set<std::string>{"x", "y", "6"});
    analyser.analyse();
    return 0;
}

// PYBIND11_MODULE(clustering, m) {
//     m.doc() = "Cluster analysis algorithm.";
//
//     py::class_<Matcher, std::shared_ptr<Matcher>>(m, "Matcher")
//         .def("__repr__", [](const Matcher& o) {
//             return "Matcher()";
//         });
//
//     py::class_<SingleLinkageMatcher, std::shared_ptr<SingleLinkageMatcher>>(m, "SingleLinkageMatcher")
//         .def(py::init<>())
//         .def("__repr__", [](const SingleLinkageMatcher& o) {
//             return "SingleLinkageMatcher()";
//         });
//
//     py::class_<Analyser>(m, "Analyser")
//         .def(py::init<std::shared_ptr<SingleLinkageMatcher>, double>(),
//              "matcher"_a = std::make_shared<SingleLinkageMatcher>(),
//              "threshold"_a = 0.8)
//         .def("create_product", &Analyser::create_product,
//              "id"_a, "store_id"_a, "tokens"_a, "quantities"_a)
//         .def("analyse", &Analyser::analyse)
//         //.def("get_clusters", &Analyser::get_clusters)
//         .def("__repr__", [](const Analyser& o) {
//             return std::format("Analyser(threshold={}, product_count={})", o.threshold, o.get_product_amount());
//         });
//
//     py::class_<StoreProduct>(m, "StoreProduct")
//         .def(py::init<int32_t, int32_t, tokens_t>(),
//              "id"_a, "store_id"_a, "tokens"_a = tokens_t{})
//         .def_readonly("id", &StoreProduct::id)
//         .def_readonly("store_id", &StoreProduct::store_id)
//         .def_readonly("tokens", &StoreProduct::tokens)
//         .def_readonly("quantities", &StoreProduct::quantities)
//         .def("__repr__", [](const StoreProduct& o) {
//             return std::format("StoreProduct(id={}, store_id={})", o.id, o.store_id);
//         });
//
//     py::class_<Product>(m, "Product")
//         .def(py::init<>())
//         .def_readonly("merged", &Product::merged)
//         .def("get_items", &Product::get_items)
//         .def("__repr__", [](const Product& o) {
//             return std::format("Product(merged={}, item_count={})", o.merged, o.items.size());
//         });
// }
