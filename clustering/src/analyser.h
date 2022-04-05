#pragma once

#include <memory>
#include <queue>
#include <string>

#include "matcher.h"
#include "product.h"

class Match {
   public:
    double score;

    Match(double score, std::shared_ptr<Product> a, std::shared_ptr<Product> b);

   private:
    std::shared_ptr<Product> a;
    std::shared_ptr<Product> b;
};

class MatchComparator {
   public:
    bool operator()(const std::shared_ptr<Match>& a, const std::shared_ptr<Match>& b);
};

class Analyser {
   public:
    const double threshold;
    const std::shared_ptr<Matcher> matcher;

    Analyser(std::shared_ptr<Matcher> linkage_criterion, double threshold = 0.8);
    double compare(std::shared_ptr<Product> a, std::shared_ptr<Product> b);

   private:
    std::priority_queue<std::unique_ptr<Match>, std::vector<std::unique_ptr<Match>, MatchComparator>> merge_queue;

    void update_queue();
};
