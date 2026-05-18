"""Curated constants for Stage 3R Discord lead promotion."""

from __future__ import annotations

PROMOTION_CLASSES = {
    "source_to_lock",
    "observation_to_review",
    "experiment_candidate",
    "negative_control_candidate",
    "debunk_or_false_positive",
    "duplicate_of_existing_work",
    "too_speculative",
    "unsafe_or_private",
    "ignore_for_now",
}

STAGE3R_SOURCE = "discord_admin_export_stage3q_lead_audit"

PUBLIC_SOURCE_TARGETS = [
    {
        "promoted_id": "stage3r-source-rtkd-iddqd",
        "source_title": "rtkd/iddqd Liber Primus technical reference",
        "source_url": "https://github.com/rtkd/iddqd",
        "source_class": "strong_community_technical",
        "corroboration_basis": "Known public repository and existing source registry reference.",
        "discord_lead_reference": "stage3q/source-links-and-datasets",
    },
    {
        "promoted_id": "stage3r-source-scream314-cicada3301",
        "source_title": "scream314/cicada3301 reference repository",
        "source_url": "https://github.com/scream314/cicada3301",
        "source_class": "strong_community_technical",
        "corroboration_basis": "Known public repository and existing source registry reference.",
        "discord_lead_reference": "stage3q/tools-code-and-repositories",
    },
    {
        "promoted_id": "stage3r-source-complete-cicada-archive",
        "source_title": "The Complete Cicada 3301 Archive",
        "source_url": "https://github.com/cicada-solvers/The-Complete-Cicada3301-Archive",
        "source_class": "secondary_archive",
        "corroboration_basis": "Public archive repository and existing Stage 3K source record.",
        "discord_lead_reference": "stage3q/source-links-and-datasets",
    },
    {
        "promoted_id": "stage3r-source-solved-pages",
        "source_title": "How the solved pages of the Liber Primus were solved",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/How_the_solved_pages_of_the_Liber_Primus_were_solved",
        "source_class": "secondary_archive",
        "corroboration_basis": "Public Fandom reference useful for solved-baseline provenance review.",
        "discord_lead_reference": "stage3q/solved-pages-and-method-history",
    },
    {
        "promoted_id": "stage3r-source-unsolved-pages",
        "source_title": "Liber Primus Unsolved Pages",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/Liber_Primus_Unsolved_Pages",
        "source_class": "secondary_archive",
        "corroboration_basis": "Public Fandom reference useful for source-discovery triage only.",
        "discord_lead_reference": "stage3q/source-links-and-datasets",
    },
    {
        "promoted_id": "stage3r-source-onion7-page15",
        "source_title": "Onion 7: numbers on page 15",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/Onion_7:_numbers_on_page_15",
        "source_class": "secondary_archive",
        "corroboration_basis": "Public page-specific table reference for bounded Onion 7 manifest setup.",
        "discord_lead_reference": "stage3q/number-squares-and-onion7",
    },
    {
        "promoted_id": "stage3r-source-2014-puzzle",
        "source_title": "CICADA 3301 2014 PUZZLE",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/CICADA_3301_2014_PUZZLE",
        "source_class": "secondary_archive",
        "corroboration_basis": "Public historical reference for signed text and image artefact leads.",
        "discord_lead_reference": "stage3q/source-links-and-datasets",
    },
    {
        "promoted_id": "stage3r-source-2015-twitter-message",
        "source_title": "2015 Twitter Message",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/2015_Twitter_Message",
        "source_class": "secondary_archive",
        "corroboration_basis": "Public historical reference; reviewable lead only.",
        "discord_lead_reference": "stage3q/source-links-and-datasets",
    },
    {
        "promoted_id": "stage3r-source-2016-message",
        "source_title": "2016 Message",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/2016_Message",
        "source_class": "secondary_archive",
        "corroboration_basis": "Public historical reference; reviewable lead only.",
        "discord_lead_reference": "stage3q/source-links-and-datasets",
    },
    {
        "promoted_id": "stage3r-source-2017-pgp-message",
        "source_title": "PGP Signed Message April 2017",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/PGP_Signed_Message_April_2017",
        "source_class": "primary_signed",
        "corroboration_basis": "Public signed-message reference for future exact string review.",
        "discord_lead_reference": "stage3q/source-links-and-datasets",
    },
    {
        "promoted_id": "stage3r-source-what-happened-2012",
        "source_title": "What Happened (2012)",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/What_Happened_(2012)",
        "source_class": "secondary_archive",
        "corroboration_basis": "Public timeline reference; source/reference only.",
        "discord_lead_reference": "stage3q/source-links-and-datasets",
    },
    {
        "promoted_id": "stage3r-source-what-happened-2013-part1",
        "source_title": "What Happened Part 1 (2013)",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2013)",
        "source_class": "secondary_archive",
        "corroboration_basis": "Public timeline reference; source/reference only.",
        "discord_lead_reference": "stage3q/source-links-and-datasets",
    },
    {
        "promoted_id": "stage3r-source-possible-hints-never-used",
        "source_title": "Possible hints never used",
        "source_url": "https://uncovering-cicada.fandom.com/wiki/Possible_hints_never_used",
        "source_class": "speculative_observation",
        "corroboration_basis": "Public speculative-reference page; not treated as proof.",
        "discord_lead_reference": "stage3q/open-questions-and-strong-leads",
    },
]

ONION7_SOURCE_URL = "https://uncovering-cicada.fandom.com/wiki/Onion_7:_numbers_on_page_15"
