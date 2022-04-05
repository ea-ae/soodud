#include <pybind11/pybind11.h>
// #include <pybind11/stl.h>

#include "analyser.h"

using namespace pybind11::literals;

Match::Match(double score, std::shared_ptr<Product> a, std::shared_ptr<Product> b)
    : score(score), a(a), b(b) {}

Analyser::Analyser(std::shared_ptr<Matcher> linkage_criterion, double threshold)
    : matcher(linkage_criterion), threshold(threshold) {}

bool MatchComparator::operator()(const std::shared_ptr<Match>& a, const std::shared_ptr<Match>& b) {
    return a->score < b->score;
}

double Analyser::compare(std::shared_ptr<Product> a, std::shared_ptr<Product> b) {
    auto score = matcher->match(*a.get(), *b.get());
    if (score >= threshold) {
        merge_queue.push(std::make_unique<Match>(score, std::move(a), std::move(b)));
    }

    return 12345;
}

void Analyser::update_queue() {}
