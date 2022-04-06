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

void Analyser::create_store_product(int32_t id, int32_t store_id, tokens_t tokens) {
    products.push_back(std::make_unique<Product>(std::make_unique<StoreProduct>(id, store_id, tokens)));
}

double Analyser::compare(Product& a, Product& b) {
    auto score = matcher->match(a, b);
    if (score >= threshold) {
        merge_queue.push(std::make_unique<Match>(score, a, b));
    }

    return 12345;
}

size_t Analyser::get_product_amount() const {
    return products.size();
}

void Analyser::update_queue() {}
