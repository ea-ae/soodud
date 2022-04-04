#include <pybind11/pybind11.h>

#include <format>
#include <iostream>

#include "analyser.h"
#include "matcher.h"
#include "product.h"

namespace py = pybind11;
using namespace py::literals;

Analyser& test() {
    std::cout << "start!\n";

    auto sp = std::make_unique<StoreProduct>(1, "product one");
    auto sp2 = std::make_unique<StoreProduct>(2, "product two");
    auto sp3 = std::make_unique<StoreProduct>(3, "product three");

    auto p = Product(std::move(sp));
    auto p2 = Product(std::move(sp2));
    auto p3 = Product(std::move(sp3));
    auto p4 = Product(std::move(p), std::move(p2));
    auto p5 = Product(std::move(p3), std::move(p4));
    std::cout << p5.items.size() << "\n";

    auto stuff = std::make_unique<SingleLinkageMatcher>();
    auto analyser = Analyser(std::move(stuff));
    return analyser;
}

PYBIND11_MODULE(clustering, m) {
    m.doc() = "Cluster analysis algorithm.";

    m.def("test", &test);

    py::class_<Matcher>(m, "Matcher")
        .def("__repr__", [](const Analyser& o) {
            return "Matcher()";
        });

    py::class_<SingleLinkageMatcher>(m, "SingleLinkageMatcher")
        .def(py::init<>())
        .def("__repr__", [](const Analyser& o) {
            return "SingleLinkageMatcher()";
        });

    py::class_<Analyser>(m, "Analyser")
        .def(py::init<std::shared_ptr<Matcher>, double>(), "matcher"_a, "threshold"_a = 0.8)
        .def("__repr__", [](const Analyser& o) {
            return std::format("Analyser(threshold={})", o.threshold);
        });

    py::class_<StoreProduct>(m, "StoreProduct")
        .def(py::init<uint32_t, std::string>(), "id"_a, "name"_a)
        .def_readonly("id", &StoreProduct::id)
        .def_readonly("name", &StoreProduct::name)
        .def("__repr__", [](const StoreProduct& o) {
            return std::format("StoreProduct(id={}, name='{}')", o.id, o.name);
        });
}
