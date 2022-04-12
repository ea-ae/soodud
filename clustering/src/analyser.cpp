#include <pybind11/pybind11.h>
// #include <pybind11/stl.h>

#include <iostream>

#include "analyser.h"

using namespace pybind11::literals;

Match::Match(double score, Product& a, Product& b)
    : score(score), a(a), b(b) {}

// bool MatchComparator::operator()(const std::unique_ptr<Match>& a, const std::unique_ptr<Match>& b) {
//     return a->score < b->score;
// }

bool compare(const std::unique_ptr<Match>& a, const std::unique_ptr<Match>& b) {
    return a->score < b->score;
}

Analyser::Analyser(std::shared_ptr<Matcher> linkage_criterion, double threshold)
    : matcher(linkage_criterion), threshold(threshold) {}

void Analyser::create_product(int32_t id, int32_t store_id, tokens_t tokens) {
    products.push_back(std::make_unique<Product>(std::make_unique<StoreProduct>(id, store_id, tokens)));
}

void Analyser::analyse() {
    std::vector<std::unique_ptr<Match>> initial_matches;

    for (int i = 0; i < products.size(); i++) {
        for (int j = i + 1; j < products.size(); j++) {  // process all combinations of items
            auto a = products[i].get();
            auto b = products[j].get();

            auto score = matcher->match(*a, *b);
            if (score >= threshold) {
                // merge_queue.push(std::make_unique<Match>(score, a, b));
                initial_matches.push_back(std::make_unique<Match>(score, *a, *b));  // retrospective sorting is faster
            }
        }
    }

    merge_queue = std::make_unique<match_queue_t>(
        [](const std::unique_ptr<Match>& a, const std::unique_ptr<Match>& b) -> bool {
            return a->score < b->score;
        },
        std::move(initial_matches));

    std::cout << merge_queue->top()->score << "\n";
    merge_queue->pop();
    std::cout << merge_queue->top()->score << "\n";
    merge_queue->pop();
    std::cout << merge_queue->top()->score << "\n";
    merge_queue->pop();
    std::cout << merge_queue->top()->score << "\n";
}

size_t Analyser::get_product_amount() const {
    return products.size();
}

void Analyser::update_queue() {}
