#pragma once

#include <memory>
#include <queue>
#include <string>

#include "matcher.h"
#include "product.h"

class Match {
   public:
    double score;

    Match(double score, Product& a, Product& b);

   private:
    Product& a;
    Product& b;
};

class MatchComparator {
   public:
    bool operator()(const std::unique_ptr<Match>& a, const std::unique_ptr<Match>& b);
};

class Analyser {
   public:
    const double threshold;
    const std::shared_ptr<Matcher> matcher;

    Analyser(std::shared_ptr<Matcher> linkage_criterion, double threshold = 0.8);
    void create_store_product(int32_t id, int32_t store_id, tokens_t tokens = {});
    double compare(Product& a, Product& b);
    size_t get_product_amount() const;

   private:
    std::vector<std::unique_ptr<Product>> products;
    std::priority_queue<std::unique_ptr<Match>, std::vector<std::unique_ptr<Match>>, MatchComparator> merge_queue;

    void update_queue();
};
