#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include <algorithm>
#include <format>
#include <iostream>
#include <memory>
#include <numeric>
#include <set>
#include <string>

#include "analyser.h"
#include "matcher.h"
#include "product.h"

namespace py = pybind11;
using namespace py::literals;

int main() {
    using q = std::pair<int32_t, std::string>;
    auto q1 = quantities_t{q{3, "kg"}, q{2, "tk"}};
    auto q2 = quantities_t{q{2, "kg"}, q{55, "%"}};

    auto analyser = Analyser();
    analyser.create_product(1, 1, std::vector<std::string>{"a", "b", "c", "d", "e", "f"}, q1);
    analyser.create_product(2, 10, std::vector<std::string>{"a", "b", "c", "d", "e", "f"}, q2);
    analyser.create_product(3, 2, std::vector<std::string>{"a", "b", "c", "d", "1", "2"});
    analyser.create_product(4, 2, std::vector<std::string>{"a", "b", "c", "d", "e", "3"}, q1);
    analyser.create_product(5, 3, std::vector<std::string>{"a", "b", "c", "d", "4", "5"});
    analyser.create_product(6, 1, std::vector<std::string>{"x", "y", "z"});
    analyser.create_product(7, 2, std::vector<std::string>{"x", "y", "6"});
    analyser.analyse();
    return 0;
}

// auto join = []<typename T>(T cont, std::string delimiter) -> std::string {
auto join = [](const auto& cont, std::string delimiter = ", ") -> std::string {
    return std::accumulate(
        cont.begin(),
        cont.end(),
        std::string(""),
        [&delimiter](std::string a, std::string b) {
            return a + (a.length() > 0 ? delimiter : "") + b;
        });
};

// PYBIND11_MAKE_OPAQUE(std::vector<Product*>);

PYBIND11_MODULE(clustering, m) {
    m.doc() = "Cluster analysis algorithm.";

    // py::bind_vector<std::vector<Product*>>(m, "ProductVector", py::module_local(false));
    // py::implicitly_convertible<py::list, std::vector<Product*>>();
    // py::implicitly_convertible<std::vector<Product*>, py::list>();

    py::class_<Matcher, std::shared_ptr<Matcher>>(m, "Matcher")
        .def("__repr__", [](const Matcher&) {
            return "Matcher()";
        });

    py::class_<SingleLinkageMatcher, std::shared_ptr<SingleLinkageMatcher>>(m, "SingleLinkageMatcher")
        .def(py::init<>())
        .def("__repr__", [](const SingleLinkageMatcher&) {
            return "SingleLinkageMatcher()";
        });

    py::class_<Analyser>(m, "Analyser")
        .def(py::init<std::shared_ptr<SingleLinkageMatcher>, double>(),
             "matcher"_a = std::make_shared<SingleLinkageMatcher>(),
             "threshold"_a = 0.8)
        .def("create_product", &Analyser::create_product,
             "id"_a, "store_id"_a, "tokens"_a, "quantities"_a)
        .def("analyse", &Analyser::analyse)
        .def("get_clusters", &Analyser::get_clusters, py::return_value_policy::reference)
        .def("__repr__", [](const Analyser& o) {
            return std::format("Analyser(threshold={}, product_count={})", o.threshold, o.get_product_amount());
        });

    py::class_<StoreProduct>(m, "StoreProduct")
        .def(py::init<int32_t, int32_t, tokens_t, quantities_t>(),
             "id"_a, "store_id"_a, "tokens"_a = tokens_t{}, "quantities"_a = quantities_t{})
        .def_readonly("id", &StoreProduct::id)
        .def_readonly("store_id", &StoreProduct::store_id)
        .def_readonly("tokens", &StoreProduct::tokens)
        .def_readonly("quantities", &StoreProduct::quantities)
        .def("__repr__", [](const StoreProduct& o) {
            std::vector<std::string> quantities;
            std::for_each(o.quantities.begin(), o.quantities.end(),
                          [&quantities](auto& q) { quantities.push_back(std::to_string(q.first) + q.second); });
            return std::format("StoreProduct(id={}, store_id={}, tokens=({}), quantities=({}))",
                               o.id, o.store_id, join(o.tokens), join(quantities));
        });

    py::class_<Product>(m, "Product")
        .def_readonly("merged", &Product::merged)
        .def("get_items", &Product::get_items, py::return_value_policy::reference)  // RVPs unnecessary
        .def("__repr__", [](const Product& o) {
            std::vector<std::string> item_ids;
            std::for_each(o.items.begin(), o.items.end(),
                          [&item_ids](auto& p) { item_ids.push_back(std::to_string(p->id)); });
            return std::format("Product(merged={}, items=({}))",
                               o.merged, join(item_ids));
        });
}
