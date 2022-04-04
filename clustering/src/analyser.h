#pragma once

#include <memory>
#include <queue>
#include <string>

#include "matcher.h"
#include "product.h"

class Analyser {
   public:
    const double threshold;
    const std::shared_ptr<Matcher> matcher;

    Analyser(std::shared_ptr<Matcher> linkage_criterion, double threshold = 0.8);
    double compare(const Product& a, const Product& b);

   private:
    std::priority_queue<std::unique_ptr<Product>> merge_queue;

    void update_queue();
};
