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

PYBIND11_MODULE(clustering, m) {
    m.doc() = "Cluster analysis algorithm.";

    m.def("test", &test);

    /*py::class_<Matcher>(m, "Matcher")
        .def("__repr__", [](const Analyser& o) {
            return "Matcher()";
        });

    py::class_<SingleLinkageMatcher>(m, "SingleLinkageMatcher")
        .def(py::init<>())
        .def("__repr__", [](const Analyser& o) {
            return "SingleLinkageMatcher()";
        });

    py::class_<Analyser>(m, "Analyser")
        .def(py::init<std::shared_ptr<Matcher>, double>(),
             "matcher"_a, "threshold"_a = 0.8)
        .def("__repr__", [](const Analyser& o) {
            return std::format("Analyser(threshold={})", o.threshold);
        });*/

    py::class_<StoreProduct>(m, "StoreProduct")
        .def(py::init<int32_t, int32_t, std::set<std::string>>(),
             "id"_a, "store_id"_a, "tokens"_a = std::set<std::string>{})
        .def_readonly("id", &StoreProduct::id)
        .def_readonly("store_id", &StoreProduct::store_id)
        .def("__repr__", [](const StoreProduct& o) {
            return std::format("StoreProduct(id={}, store_id={})", o.id, o.store_id);
        });
}
