#pragma once

#include <functional>
#include <string>

#include "product.h"

class Analyser {
   public:
    const double threshold;

    Analyser(std::function<double(const std::string, const std::string)> linkage_criterion, double threshold = 0.8);
    double compare(const Product& a, const Product& b);

   private:
    std::unordered_map<std::size_t, double> cached_matches;
    const std::function<double(const std::string, const std::string)> match_strings;

    static std::size_t cluster_hash(std::vector<std::int32_t> products);
};
