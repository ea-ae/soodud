#include <pybind11/pybind11.h>
// #include <pybind11/stl.h>

#include "product.h"

namespace py = pybind11;
using namespace py::literals;

int main() {
}

PYBIND11_MODULE(clustering, m) {
    m.doc() = "Cluster analysis algorithm.";

    py::class_<StoreProduct>(m, "StoreProduct")
	.def(py::init<uint32_t, std::string>())
	.def_readonly("id", &StoreProduct::id)
	.def_readonly("name", &StoreProduct::name);
}
