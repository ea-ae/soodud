#pragma once

#include <memory>
#include <queue>
#include <string>

#include "matcher.h"
#include "product.h"

class Match {
   public:
    double score;
    Product& a;
    Product& b;

    Match(double score, Product& a, Product& b);
    bool contains_merged_products() const;
};

using match_queue_t = std::priority_queue<std::unique_ptr<Match>, std::vector<std::unique_ptr<Match>>, auto(*)(const std::unique_ptr<Match>& a, const std::unique_ptr<Match>& b)->bool>;

class Analyser {
   public:
    const double threshold;
    const std::shared_ptr<Matcher> matcher;

    Analyser(std::shared_ptr<Matcher> linkage_criterion = std::make_shared<SingleLinkageMatcher>(),
             double threshold = 0.5);
    void create_product(int32_t id, int32_t store_id, tokens_t tokens = {});
    void analyse();
    size_t get_product_amount() const;

   private:
    std::vector<std::unique_ptr<Product>> products;
    std::unique_ptr<match_queue_t> merge_queue;

    void process_match();
    void update_queue();
};
