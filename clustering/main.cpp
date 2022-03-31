#include <pybind11/pybind11.h>

#include "product.h"

namespace py = pybind11;
using namespace py::literals;

int main() {
}

PYBIND11_MODULE(clusters, m) {
    m.doc() = "Cluster analysis algorithm.";

    py::class_<StoreProduct>(m, "StoreProduct")
	.def(py::init<uint32_t, std::string>())
	.def_property_readonly("id", &StoreProduct::getId)
	.def_property_readonly("name", &StoreProduct::getName);
}
