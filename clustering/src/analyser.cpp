#include <pybind11/pybind11.h>
// #include <pybind11/stl.h>

#include "analyser.h"

using namespace pybind11::literals;

Match::Match(double score, Product& a, Product& b)
    : score(score), a(a), b(b) {}

bool MatchComparator::operator()(const std::unique_ptr<Match>& a, const std::unique_ptr<Match>& b) {
    return a->score < b->score;
}

Analyser::Analyser(std::shared_ptr<Matcher> linkage_criterion, double threshold)
    : matcher(linkage_criterion), threshold(threshold) {}

void Analyser::add_store_product(std::unique_ptr<StoreProduct> product) {
    // products.push_back(std::make_unique<Product>(std::move(product)));
}

double Analyser::compare(Product& a, Product& b) {
    auto score = matcher->match(a, b);
    if (score >= threshold) {
        merge_queue.push(std::make_unique<Match>(score, a, b));
    }

    return 12345;
}

void Analyser::update_queue() {}
