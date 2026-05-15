#include "libreprimus/build_config.hpp"
#include "libreprimus/cipher_placeholder.hpp"
#include "libreprimus/corpus_placeholder.hpp"
#include "libreprimus/gematria_placeholder.hpp"
#include "libreprimus/report_placeholder.hpp"
#include "libreprimus/scoring_placeholder.hpp"
#include "libreprimus/search_placeholder.hpp"
#include "libreprimus/sqlite_placeholder.hpp"
#include "libreprimus/version.hpp"

#include <iostream>
#include <string_view>

namespace {

int expect(bool condition, std::string_view message) {
    if (condition) {
        return 0;
    }

    std::cerr << "FAILED: " << message << '\n';
    return 1;
}

bool contains_stage_0a(std::string_view value) {
    return value.find("Stage 0A") != std::string_view::npos;
}

}  // namespace

int main() {
    int failures = 0;
    failures += expect(!libreprimus::project_name().empty(), "project name is non-empty");
    failures += expect(!libreprimus::version().empty(), "version is non-empty");
    failures += expect(libreprimus::stage() == "Stage 0A", "stage is Stage 0A");
    failures += expect(!libreprimus::build_mode_summary().empty(), "build summary is non-empty");
    failures += expect(contains_stage_0a(libreprimus::corpus_placeholder_status()), "corpus placeholder");
    failures += expect(contains_stage_0a(libreprimus::gematria_placeholder_status()), "gematria placeholder");
    failures += expect(contains_stage_0a(libreprimus::cipher_placeholder_status()), "cipher placeholder");
    failures += expect(contains_stage_0a(libreprimus::scoring_placeholder_status()), "scoring placeholder");
    failures += expect(contains_stage_0a(libreprimus::search_placeholder_status()), "search placeholder");
    failures += expect(contains_stage_0a(libreprimus::report_placeholder_status()), "report placeholder");
    failures += expect(contains_stage_0a(libreprimus::sqlite_placeholder_status()), "sqlite placeholder");

    return failures == 0 ? 0 : 1;
}
