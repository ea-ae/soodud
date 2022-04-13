#include "analyser.h"

#include <iostream>

Match::Match(double score, Product& a, Product& b)
    : score(score), a(a), b(b) {}

bool Match::contains_merged_products() const {
    return a.merged || b.merged;
}

bool compare(const std::unique_ptr<Match>& a, const std::unique_ptr<Match>& b) {
    return a->score < b->score;
}

Analyser::Analyser(std::shared_ptr<Matcher> linkage_criterion, double threshold)
    : threshold(threshold), matcher(linkage_criterion) {}

void Analyser::create_product(int32_t id, int32_t store_id, tokens_t tokens, quantities_t quantities) {
    products.push_back(std::make_unique<Product>(std::make_unique<StoreProduct>(id, store_id, tokens, quantities)));
}

void Analyser::analyse() {
    std::vector<std::unique_ptr<Match>> initial_matches;

    for (size_t i = 0; i < products.size(); i++) {
        for (size_t j = i + 1; j < products.size(); j++) {  // process all combinations of items
            auto a = products[i].get();
            auto b = products[j].get();

            auto score = matcher->match(*a, *b);
            if (score >= threshold) {
                initial_matches.push_back(std::make_unique<Match>(score, *a, *b));  // retrospective sorting is faster
            }
        }
    }

    merge_queue = std::make_unique<match_queue_t>(
        [](const std::unique_ptr<Match>& a, const std::unique_ptr<Match>& b) -> bool {
            return a->score < b->score;
        },
        std::move(initial_matches));

    while (!merge_queue->empty()) {
        process_match();
    }
    std::cout << "end\n";
}

std::vector<Product*> Analyser::get_clusters() {
    std::vector<Product*> clusters;
    for (auto& product : products) {
        if (!product->merged) {
            clusters.push_back(product.get());
        }
    }
    return clusters;
}

size_t Analyser::get_product_amount() const {
    return products.size();
}

void Analyser::process_match() {
    auto match = merge_queue->top().get();
    if (match->contains_merged_products()) {
        merge_queue->pop();
        return;
    }

    match->a.merged = true;
    match->b.merged = true;
    auto new_product = std::make_unique<Product>(std::move(match->a), std::move(match->b));
    merge_queue->pop();

    for (auto& product : products) {  // add new products
        auto score = matcher->match(*new_product, *product);
        if (score >= threshold) {
            merge_queue->push(std::make_unique<Match>(score, *new_product, *product));
        }
    }

    products.push_back(std::move(new_product));
}

void Analyser::update_queue() {}
