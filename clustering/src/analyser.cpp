#include <pybind11/pybind11.h>
// #include <pybind11/stl.h>

#include "analyser.h"

using namespace pybind11::literals;

Analyser::Analyser(std::function<double(const std::string, const std::string)> linkage_criterion,
                   double threshold)
    : match_strings(linkage_criterion), threshold(threshold) {}

double Analyser::compare(const BaseProduct& a, const BaseProduct& b) {
    /*if (a.getName() == std::nullopt) {

    }*/
    return 111;
    // auto similarity = this->match_strings(a, b);
}

#pragma warning(push)
#pragma warning(disable : 26451)
// questions/20511347/a-good-hash-function-for-a-vector
std::size_t Analyser::cluster_hash(std::vector<std::int32_t> products) {
    std::size_t seed = products.size();
    for (auto& i : products) {
        seed ^= i + 0x9e3779b9 + (seed << 6) + (seed >> 2);
    }
    return seed;
}
#pragma warning(pop)
