#include <pybind11/pybind11.h>
// #include <pybind11/stl.h>

#include "analyser.h"

using namespace pybind11::literals;

Analyser::Analyser(std::shared_ptr<Matcher> linkage_criterion, double threshold)
    : matcher(linkage_criterion), threshold(threshold) {}

double Analyser::compare(const Product& a, const Product& b) {
    // auto similarity = this->matcher->match(a, b);
    return 12345;
}
