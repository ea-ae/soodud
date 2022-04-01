#pragma once

#include <memory>
#include <string>

#include "matcher.h"
#include "product.h"

class Analyser {
   public:
    const double threshold;

    Analyser(std::shared_ptr<Matcher> linkage_criterion, double threshold = 0.8);
    double compare(const Product& a, const Product& b);
    std::shared_ptr<Matcher> matcher;

   private:
    std::unordered_map<std::size_t, double> cached_matches;
    /// const std::function<double(const std::string, const std::string)> match_strings;
};
