#include <pybind11/pybind11.h>

#include <format>
#include <iostream>

#include "analyser.h"
#include "product.h"

namespace py = pybind11;
using namespace py::literals;

int test() {
    std::cout << "start!\n";

    auto sp = std::make_unique<StoreProduct>(1, "product one");
    auto sp2 = std::make_unique<StoreProduct>(2, "product two");
    auto sp3 = std::make_unique<StoreProduct>(3, "product three");

    auto p = Product(std::move(sp));
    auto p2 = Product(std::move(sp2));
    auto p3 = Product(std::move(sp3));
    auto p4 = Product(std::move(p), std::move(p2));
    std::cout << p4.items.size() << "\n";

    auto p5 = Product(std::move(p3), std::move(p4));
    std::cout << p5.items.size() << "\n";

    return 123;

    /*auto analyzer = Analyser([](std::string a, std::string b) {
        return 1;
    });*/

    // return analyzer.compare(p, *sp3.get());
}

PYBIND11_MODULE(clustering, m) {
    m.doc() = "Cluster analysis algorithm.";

    m.def("test", &test);

    py::class_<Analyser>(m, "Analyser")
        .def(py::init<std::function<float_t(std::string, std::string)>, float_t>())
        .def("__repr__", [](const Analyser& o) {
            return std::format("Analyser(threshold={})", o.threshold);
        });

    py::class_<StoreProduct>(m, "StoreProduct")
        .def(py::init<uint32_t, std::string>(), "id"_a, "name"_a)
        .def_readonly("id", &StoreProduct::id)
        .def_readonly("name", &StoreProduct::name)
        .def("__repr__", [](const StoreProduct& o) {
            return std::format("StoreProduct(id={}, name=\"{}\")", o.id, o.name);
        });
}
