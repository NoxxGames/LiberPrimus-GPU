# Stage 4A Discord Research-Bundle Review for LiberPrimus-GPU

> Stage 4B note: This is a research input derived from the redacted Stage 4A review site. Discord/site-derived leads require public-source corroboration before promotion. This document is not a solve claim, does not activate the canonical corpus, and does not make visual readings canonical.

## Executive summary

The Stage 4A site is genuinely useful. It is not just theatrical scaffolding with a shinier coat of paint. The split-channel design solves the exact failure mode of earlier review attempts: instead of forcing a browser through giant Discord exports, it exposes 43 redacted channels, 1,327 channel shards, 12 topic views, and review indexes for links, methods, numbers, visuals, and debunks. The largest channels are enormous â€” `general` alone is split into 573 parts, `general-solving` into 265, and `solving-lp-general-discussion` into 122 â€” so the topic/index-first strategy is the right one. îˆ€citeîˆ‚turn30view0îˆ‚turn34view4îˆ‚turn34view5îˆ‚turn34view6îˆ

The repository direction still looks sound. The current `main` branch documentation says Stage 4A is complete and that the next planned stage is **Stage 4B: website-derived source-lock triage and visual observation intake**. The same docs keep CUDA deferred, keep the canonical corpus inactive, and continue the â€œbounded, reviewable, reproducible firstâ€ approach. The commit `1bd7ad7` exists as a child of `6266d87`, which is consistent with the Stage 4A milestone the site claims to represent. îˆ€citeîˆ‚turn42view1îˆ‚turn42view2îˆ‚turn42view3îˆ

The strongest practical conclusion is simple: the next work should not be â€œmore cipher cleverness.â€ It should be **triage, locking, annotation, and narrow verification**. The best immediate leads are not another round of free-range VigenÃ¨re keys or numerology aerobics. They are: source-locking high-value public artefacts; turning cuneiform/dot claims into structured observation records; running tiny deterministic audits on ambiguous visual encodings; and promoting only exact, source-backed numeric and hash seeds into bounded experiments. îˆ€citeîˆ‚turn30view0îˆ‚turn42view3îˆ

The strongest warnings are equally simple. The site contains a lot of community energy and a lot of crypto pareidolia. The cuneiform/base-60 story is mathematically neat but visually unverified; the 13/31 dot story is not unique; braille and constellation readings proliferate because they are cheap to see and expensive to falsify; OutGuess and MP3 stego produce seductive garbage; and some geometry/symmetry material looks like speculation accreted into pseudo-structure. Treat all of that as leads, not truth. îˆ€citeîˆ‚turn14view0îˆ‚turn14view3îˆ‚turn13view0îˆ‚turn13view1îˆ‚turn23view0îˆ‚turn23view3îˆ‚turn33view1îˆ

The site should not remain wide-open and indexable in its current form. It is redacted, which is good, but it still exposes a large derived corpus from Discord, and its attachment-reference index includes opaque identifiers and file-name fragments that are unnecessary for public search engines. Immediate answer: **noindex now; access-control next**. îˆ€citeîˆ‚turn30view0îˆ‚turn29view0îˆ

## Site coverage and source-lock map

The reviewed site index was reachable and clearly states its purpose: **â€œRedacted public review modeâ€**, with raw Discord logs, usernames, IDs, private URLs, and raw LP source images excluded from committed repository state. It also explicitly warns that the site is a generated review aid, not source truth and not a solve claim. That warning is exactly right and should stay. îˆ€citeîˆ‚turn30view0îˆ

I reviewed the site index; the listed topic views; the public-link, image-reference, attachment-reference, method-claim, numeric-claim, visual-claim, and debunk indexes; and sampled priority channel part pages from `33-39-cuneiform`, `page-art-dots`, `number-squares`, and `the-deep-web-hash`. I also checked the current repository `README.md`, `STATUS.md`, and the Stage 4A follow-up commit page on `main`. The homepageâ€™s â€œDeep Research manifestâ€ and â€œREADME for Deep Researchâ€ links were not fetchable through this browser session, so those remain a limitation rather than a confirmed site defect. îˆ€citeîˆ‚turn30view0îˆ‚turn34view0îˆ‚turn34view1îˆ‚turn34view2îˆ‚turn34view3îˆ‚turn43view0îˆ‚turn43view1îˆ‚turn43view2îˆ‚turn31view0îˆ‚turn31view1îˆ‚turn42view2îˆ‚turn42view3îˆ

One immediate site-quality finding is that the raw public-link index is noisy. Its first lines are cluttered with emoji CDN links, which means the raw link count is not the same thing as the count of useful public sources. Stage 4B should therefore start with domain allow-listing, deduplication, and source-class tagging rather than naÃ¯vely mirroring everything the site calls a public link. îˆ€citeîˆ‚turn31view2îˆ

A second site-quality finding is privacy-related. The attachment-reference index includes safe filenames such as `The_Instar_Emergence.pdf` and `joutguess`, but it also includes opaque attachment identifiers and token-like values. Even without usernames, that is the kind of derived surface that should not be globally indexed. îˆ€citeîˆ‚turn29view0îˆ

The highest-value public sources surfaced by the site are below.

| Source | Class | Why it matters | Already known in project direction | Recommended action | Evidence |
|---|---|---|---|---|---|
| `rtkd/iddqd` GitHub repository | strong_community_technical | Repeatedly cited as original files/transcripts anchor; should remain a core lock target. | Yes | Source-lock now; keep hash/metadata. | îˆ€citeîˆ‚turn19view0îˆ‚turn35view0îˆ |
| `scream314/cicada3301` GitHub repository | strong_community_technical | Useful secondary technical corpus, especially puzzle-history markdown and LP notes. | Yes | Source-lock now as reference corpus. | îˆ€citeîˆ‚turn19view2îˆ‚turn32view1îˆ |
| `The Complete Cicada3301 Archive` GitHub archive | secondary_archive | Best practical public dump for historical assets, PDFs, and old-side materials; not primary, but crucial. | Yes | Lock selected files first, not whole blind mirror. | îˆ€citeîˆ‚turn18view8îˆ |
| Uncovering Cicada page on solved LP methods | strong_community_technical | Best public summary of solved-page mechanics and skip-F handling. | Yes | Lock now and cite in method docs/tests. | îˆ€citeîˆ‚turn18view1îˆ‚turn39search0îˆ |
| Uncovering Cicada page on LP unsolved pages | strong_community_technical | Useful unsolved inventory and page references. | Yes | Lock now. | îˆ€citeîˆ‚turn19view2îˆ‚turn39search6îˆ |
| Uncovering Cicada page on LP unsolved page transliteration | strong_community_technical | Explicitly notes cross-page word continuation, which matters for corpus boundaries. | Yes | Lock now; reference in corpus docs. | îˆ€citeîˆ‚turn39search12îˆ |
| Uncovering Cicada page on frequency analysis of unsolved pages | strong_community_technical | Good anti-fantasy reference for cipher-family triage. | Yes | Lock now; use in negative-control docs. | îˆ€citeîˆ‚turn39search14îˆ |
| Uncovering Cicada page on Instar emergence | strong_community_technical | Historical anchor for `761.mp3`, hidden-poem context, and audio claims. | Yes | Lock now; use for audio/stego fixtures. | îˆ€citeîˆ‚turn20view8îˆ‚turn39search1îˆ‚turn39search15îˆ |
| Uncovering Cicada page on What Happened Part 1 (2014) | strong_community_technical | Historical anchor for Interconnectedness, OpenPuff, and the magic squares. | Yes | Lock now; use for number-square/stego fixtures. | îˆ€citeîˆ‚turn39search2îˆ‚turn39search5îˆ |
| Uncovering Cicada page on OutGuess | strong_community_technical | Central historical stego reference. | Yes | Lock now with version notes. | îˆ€citeîˆ‚turn19view5îˆ‚turn39search11îˆ |
| Google spreadsheet `tranlsations` workbook | secondary_archive | Widely referenced for solved-page summaries and transcripts, but needs provenance caution. | Partly | Lock metadata and sheet snapshots, not blind trust. | îˆ€citeîˆ‚turn19view3îˆ‚turn32view7îˆ |
| Wayback snapshot of `outguess.org` | reference_only_tooling | Historical documentation source for tool behaviour. | Partly | Lock now for stego notes. | îˆ€citeîˆ‚turn32view6îˆ |
| Cygwin OutGuess package page | reference_only_tooling | Useful for install and packaging provenance, not puzzle truth. | Partly | Lock as tooling note. | îˆ€citeîˆ‚turn32view6îˆ |
| `Charleswyt/MP3Stego` repository | reference_only_tooling | Useful only for reproducing MP3Stego claims and false-positive controls. | Partly | Lock as tooling reference, not evidence. | îˆ€citeîˆ‚turn22view3îˆ |
| `rtkd/iddqd` 2013/02 tree | strong_community_technical | Important source location for `761.mp3` and related 2013 artefacts. | Yes | Lock now with file hashes. | îˆ€citeîˆ‚turn20view8îˆ‚turn32view0îˆ |
| Archive/Wayback copy of `infotomb` text | secondary_archive | Fragile historical mirror; useful for link rot mitigation. | Partly | Lock metadata/hash only. | îˆ€citeîˆ‚turn32view9îˆ |
| `magicsquares.txt` in the Complete Archive | secondary_archive | Concrete asset for deterministic number-square experiments. | Partly | Lock now. | îˆ€citeîˆ‚turn18view8îˆ‚turn23view4îˆ |
| `li676-224_server-status_orig.txt` in the Complete Archive | secondary_archive | Historical server-status artefact that the community still mines. | Partly | Lock later, reference-only. | îˆ€citeîˆ‚turn18view8îˆ |
| `3301archive` and old forum essays on number squares | speculative | Worth preserving for historiography but not as evidence. | Partly | Reference-only; do not promote into experiments by default. | îˆ€citeîˆ‚turn32view8îˆ |
| Boxentriq / binary translators / generic online tools | reference_only_tooling | Helpful utilities, not source truth. | Partly | Cite or wrap locally if needed; do not lock as evidence. | îˆ€citeîˆ‚turn19view5îˆ‚turn32view5îˆ |

## Method, numeric, and visual lead review

The best method lead on the site is not new; it is the projectâ€™s caution getting better. Public solved-page history says multiple solved ciphers skip plaintext `F` values, but the skip rule applies in keyed/stream contexts rather than everything everywhere. The siteâ€™s solved-method-history discussion echoes that distinction: skip behaviour belongs with VigenÃ¨re/running-key and prime/totient families, not universal Atbash/shift handling. That means future reset/interruptor experiments should stay family-specific and never be applied as a global default. îˆ€citeîˆ‚turn39search0îˆ‚turn17view2îˆ

The cuneiform/base-60 material is the strongest numeric lead and the easiest trap. The siteâ€™s cuneiform topic explicitly says enthusiasm can outrun evidence and that the visual reading is â€œnot as obviousâ€ as people wanted it to be. The topic also records that the candidate full value `3722101` produced no convincing text output in prior experiments. The maths is fine if the readout is accepted: `17:13` gives `1033`, `55:1` gives `3301`, and `17:13:55:1` gives `3,722,101`; those values are internally consistent, and the full value is prime. The problem is not arithmetic; it is that the glyph segmentation is still an observation, not a verified fact. That makes this an **observation-to-review first**, and only then a tiny seed-pack candidate. îˆ€citeîˆ‚turn14view0îˆ‚turn14view3îˆ‚turn37view0îˆ

The dot/binary/braille story is weaker than the dot/delimiter story. The siteâ€™s page-art topic helpfully does the thing the internet almost never does: it shows the ambiguity. For one five-dot motif, a clockwise reading from a chosen anchor gives `01101 = 13`, but the same motif under other rotations yields `26, 21, 11, 22`. For a three-dot motif, the same topic page lists multiple possible values and not just the headline-friendly `31`. In other words: **13 and 31 are not forced readings**. By contrast, the mirrored three-dot delimiters on pages such as page 5 and page 56 are an actual textual feature, not a post-hoc overlay game. That makes delimiter asymmetry a much better research target than binary, braille, or constellation decoding. îˆ€citeîˆ‚turn13view0îˆ‚turn13view1îˆ‚turn26view2îˆ‚turn38view3îˆ

The number-square material splits cleanly into a strong core and a swamp. The strong core is historical and public: Interconnectedness/OpenPuff led to `magicsquares.txt`, containing two order-5 and one order-7 magic squares summing to `3301`, `1033`, and `1033`. The swamp is the layer above it: `3301 - x = prime`, eigenvalue-to-English stories, Fibonacci spirals, and other arithmetic massages. The right next move is to lock the raw squares and only test small, deterministic transform families on those raw values. It is not to keep re-enacting numerology CrossFit. îˆ€citeîˆ‚turn23view4îˆ‚turn39search2îˆ‚turn39search5îˆ‚turn14view1îˆ

Cookie/hash leads remain concrete but narrow. The site records a specific `p7amjopgric7dfdi` context for two concrete 64-hex values keyed as `167=` and `761=`; those are plausible SHA-256-like targets. The same topic also circles exact candidate families such as signed messages, HTML comments, onion references, filenames, timestamps, and named strings, while community discussion elsewhere records repeated zero-match outcomes for earlier exact-match packs. The right response is a **new exact-candidate pack only if the strings are explicit, historically anchored, and deduplicated against prior runs**. The wrong response is broad cracking. îˆ€citeîˆ‚turn12view0îˆ‚turn12view1îˆ‚turn43view0îˆ‚turn42view3îˆ

The literature-key layer is mostly background colour. The site repeatedly references Blake, Emerson, Crowley, Agrippa, the Mabinogion, and related text traditions. Some of that is historically relevant to Cicadaâ€™s earlier puzzles and imagery, but as a Stage 4A takeaway it mostly argues for **source-locking literature references and tightening historical annotations**, not for another large key search. The repository `STATUS.md` already records multiple tiny motif and historical VigenÃ¨re packs through Stages 3D, 3F, and 3I; that is enough to justify a pause on more literature-key fishing unless a new key is tiny, explicit, and directly source-backed. îˆ€citeîˆ‚turn20view2îˆ‚turn21view4îˆ‚turn20view8îˆ‚turn42view3îˆ

The strongest leads, classified conservatively, are below.

| Lead | Class | Evidence strength | False-positive risk | Why it matters | Recommended action | Evidence |
|---|---|---|---|---|---|---|
| Family-specific skip-`F` handling | experiment_candidate | high | low | Public solved-page history and site discussion align: skip logic is not universal. | Keep as constrained ablation only. | îˆ€citeîˆ‚turn39search0îˆ‚turn17view2îˆ |
| Raw Interconnectedness magic squares | public_source_to_lock | high | low | Concrete historical artefact, already known to be puzzle-relevant. | Lock and build deterministic transforms. | îˆ€citeîˆ‚turn23view4îˆ‚turn39search2îˆ‚turn39search5îˆ |
| Cuneiform `[17,13]` / `[55,1]` reading | observation_to_review | medium | high | Arithmetic is clean, visual certainty is not. | Human coordinate annotation first. | îˆ€citeîˆ‚turn14view0îˆ‚turn37view0îˆ |
| Full cuneiform value `3,722,101` | experiment_candidate | low | high | Derived cleanly from the archived reading, but prior attempts were noisy. | Only tiny seed tests after annotation. | îˆ€citeîˆ‚turn14view3îˆ‚turn37view0îˆ |
| Mirrored three-dot delimiters | observation_to_review | medium | medium | Actual page punctuation asymmetry is stronger than free-form dot symbolism. | Inventory and test boundary/reset hypotheses. | îˆ€citeîˆ‚turn26view2îˆ‚turn38view5îˆ |
| 13/31 dot-binary readings | debunk_or_false_positive | medium | extreme | Site itself shows multiple valid readings under rotation and polarity changes. | Preserve as ambiguity control, not seed truth. | îˆ€citeîˆ‚turn13view0îˆ‚turn13view1îˆ |
| Constellation readings | debunk_or_false_positive | low | extreme | Orion/Capella/Crux/Eurion claims are resemblance-driven and unstable. | Preserve as negative controls only. | îˆ€citeîˆ‚turn35view0îˆ‚turn38view6îˆ |
| Exact cookie-hash strings from known HTML/comments/file names | experiment_candidate | medium | medium | Concrete hash targets exist; explicit variants may still be worth exact-match testing. | Tiny exact-match pack only. | îˆ€citeîˆ‚turn12view0îˆ‚turn12view1îˆ‚turn21view6îˆ |
| GP/rune count claims with exact spans | experiment_candidate | medium | low | Good verifier fodder; safer than new decryption fishing. | Add to claim-verifier queue. | îˆ€citeîˆ‚turn16view1îˆ‚turn43view1îˆ |
| Mayfly-dot â€œskip indices for all pagesâ€ claim | too_speculative | low | extreme | Eye-catching but unsupported and unverified. | Quarantine until public evidence exists. | îˆ€citeîˆ‚turn26view8îˆ |
| Geometry/mirror-sequence overlay tables | too_speculative | low | extreme | Looks structured, but source backing is weak and contamination risk is high. | Quarantine. | îˆ€citeîˆ‚turn33view1îˆ |
| Historical source pages on Instar/OpenPuff/OutGuess | public_source_to_lock | high | low | Better for fixtures and regressions than for new text solving. | Lock immediately. | îˆ€citeîˆ‚turn39search1îˆ‚turn39search2îˆ‚turn39search11îˆ |

## Stego, audio, and false-positive control review

The siteâ€™s stego/audio material says one useful thing very loudly: **positive controls first**. Public historical pages support three specific facts that matter operationally: `761.mp3` is historically tied to â€œThe Instar Emergenceâ€; public write-ups say a hexdump revealed the hidden poem text; and the 2014 Interconnectedness asset yielded `magicsquares.txt` via OpenPuff. Those are real fixture opportunities. They are far more valuable than spiralling into fresh speculation about â€œmaybe a spectrogram this timeâ€. îˆ€citeîˆ‚turn39search1îˆ‚turn39search15îˆ‚turn39search2îˆ‚turn39search5îˆ

The site also preserves the communityâ€™s bad habits, which is useful if you treat them as warnings instead of quests. In the stego/audio topic, people explicitly note that OutGuess can throw false positives â€œbasically every timeâ€, that brute-forced page outputs return garbage or fake file types, and that repeated spectrogram checking of Instar/related audio did not produce anything meaningful. That does not mean â€œnever test stego/audio.â€ It means **build a regression harness for known positives and known negatives, then stop when the harness cannot discriminate**. îˆ€citeîˆ‚turn23view0îˆ‚turn23view2îˆ‚turn23view3îˆ

The current repo state fits that view. `STATUS.md` on `main` says Stage 3V added an OutGuess regression harness, and it still treats broad stego scanning as out of scope; Stage 4A then produced the website bundle for source/observation work, with Stage 4B planned next. That is the right order. OutGuess/source-locking should come before any broader audio or image fishing. îˆ€citeîˆ‚turn42view3îˆ

The highest-value false-positive controls to preserve are below.

| False-positive path | Why it is dangerous | Recommended encoding in repo | Evidence |
|---|---|---|---|
| OutGuess brute-force file-type hits on LP pages | The site repeatedly records fake file types and garbage outputs after arbitrary passwords. | Add explicit negative-control cases and â€œgarbage-filetypeâ€ examples. | îˆ€citeîˆ‚turn23view0îˆ‚turn23view3îˆ‚turn24view0îˆ |
| MP3Stego/`Brendelia` enthusiasm | Site discussion shows extraction excitement, but not a public, reproducible, source-anchored success standard for LP-related solving. | Keep as reference-only test case, not evidence. | îˆ€citeîˆ‚turn23view0îˆ‚turn22view2îˆ |
| Spectrogram pattern fishing | Public historical summary says Instar was checked without meaningful spectrogram findings. | Add spectrogram null controls before any future audio runs. | îˆ€citeîˆ‚turn23view2îˆ‚turn39search1îˆ |
| Braille dot readings | Even in early page-art discussion, participants noted how many different braille readings could be found. | Add as visual pareidolia negative control. | îˆ€citeîˆ‚turn38view3îˆ |
| Constellation matching | Orion/Capella/Crux/Eurion claims are numerous and contradictory. | Add as â€œresemblance-onlyâ€ negative-control class. | îˆ€citeîˆ‚turn35view0îˆ‚turn38view6îˆ |
| 13/31 as forced binary values | Topic pages explicitly show multiple alternative values. | Preserve the full ambiguity table in docs/tests. | îˆ€citeîˆ‚turn13view0îˆ‚turn13view1îˆ |
| AI-generated page â€œsolvesâ€ | The debunk shard records AI hallucinating even already-solved material. | Keep explicit warning in README/wiki/tutorials. | îˆ€citeîˆ‚turn24view2îˆ |
| â€œLP has only 16 authentic pagesâ€ myth | A 2025 general-solving claim on the site asserts this; it contradicts the projectâ€™s 58-page working corpus context and the broader public LP record. | Preserve as misinformation example. | îˆ€citeîˆ‚turn19view4îˆ‚turn30view0îˆ |
| PGP-absent â€œnew Cicadaâ€ claims | Debunk topic explicitly notes lack of signature as reason to discard. | Keep in source reliability docs. | îˆ€citeîˆ‚turn24view1îˆ‚turn43view0îˆ |
| Dictionary-ish prime/totient word hits | Debunk topic shows how easy nonsense hits are to obtain. | Add to scorer warning docs and negative controls. | îˆ€citeîˆ‚turn24view3îˆ |

## Recommended registry updates and bounded experiment backlog

The highest-value immediate work is **promotion**, not â€œsolvingâ€. The source registry should absorb the best public artefacts surfaced by the site. The visual observation registry should absorb only exact, image-tied claims: cuneiform candidate regions, three-dot delimiter handedness, five-dot motif coordinates, and any promoted page-art regions with precise page and crop references. The numeric observation registry should focus on exact-span GP/rune claims, the cuneiform-derived candidate tuples and derived residues, and raw Onion 7 square values before any transforms. The negative-control registry should explicitly preserve the siteâ€™s own best warnings: braille ambiguity, constellation pareidolia, OutGuess fake file types, spectrogram non-results, and AI hallucinations. îˆ€citeîˆ‚turn30view0îˆ‚turn43view0îˆ‚turn43view1îˆ‚turn43view2îˆ

The next bounded experiments should be small, explicit, and boring in the best possible way.

| Experiment ID | Hypothesis | Exact inputs | Candidate count | Controls | False-positive risk | Operator-policy status | Recommended stage | Evidence |
|---|---|---|---:|---|---|---|---|---|
| `exp_stage4b_cuneiform_reading_pack_v1` | Only explicitly documented cuneiform tuple readings deserve testing. | Archived tuples from the cuneiform topic; start with `[17,13],[55,1]` plus explicitly documented alternates only. | 32 | Random equally sized tuples; previously noisy full-value tests. | high | auto-runnable after implementation | Stage 4C | îˆ€citeîˆ‚turn14view0îˆ‚turn37view0îˆ‚turn14view3îˆ |
| `exp_stage4b_dot_ambiguity_audit_v1` | Dot/binary claims are mostly ambiguity, not forced values. | Promoted five-dot and three-dot motifs from exact page/image refs. | 140 | Synthetic dot masks and delimiter controls. | low | auto-runnable after implementation | Stage 4C | îˆ€citeîˆ‚turn13view0îˆ‚turn13view1îˆ‚turn26view2îˆ |
| `exp_stage4b_delimiter_handedness_v1` | Left/right three-dot delimiters correlate with reset or direction boundaries. | All exact three-dot delimiter instances across locked LP pages. | 16 model variants | Symmetric delimiters, shuffled-page controls. | medium | auto-runnable after implementation | Stage 4D | îˆ€citeîˆ‚turn26view2îˆ‚turn38view5îˆ |
| `exp_stage4b_onion7_raw_routes_v1` | Raw Interconnectedness squares may yield useful seed streams under tiny deterministic route families. | Three published raw squares only. | 96 | Route-permuted controls; random same-order magic squares. | medium | auto-runnable after implementation | Stage 4D | îˆ€citeîˆ‚turn23view4îˆ‚turn39search2îˆ‚turn39search5îˆ |
| `exp_stage4b_cookie_pack_v2` | A small set of newly promoted, exact historical strings may match the two SHA-256-like cookie values. | Explicit strings from source-backed HTML comments, file names, onion strings, and signed-message nearby text only. | 384 | Previous pack dedupe; random string negatives. | medium | auto-runnable if deduped | Stage 4E | îˆ€citeîˆ‚turn12view0îˆ‚turn12view1îˆ‚turn21view6îˆ‚turn42view3îˆ |
| `exp_stage4b_gp_rune_verifier_batch002` | New exact-span claims from the website can be verified or rejected cheaply. | Newly promoted exact page/span claims only. | 20 | Existing verifier goldens and nulls. | low | auto-runnable now if implementation exists | Stage 4D | îˆ€citeîˆ‚turn16view1îˆ‚turn43view1îˆ |
| `exp_stage4b_number_square_no_fudge_v1` | Prime-difference stories should only survive if they work under fixed, no-fudge transforms. | Raw 4Ã—4/5Ã—5/7Ã—7 values from historical source. | 128 | Random table controls; permutation controls. | medium | auto-runnable after implementation | Stage 4D | îˆ€citeîˆ‚turn14view1îˆ‚turn23view4îˆ |
| `exp_stage4b_visual_region_annotation_v1` | Better coordinates beat more filters. | Human-annotated cuneiform and dot regions only. | 24 regions | Double-review on a subset. | low | needs human review first | Stage 4C | îˆ€citeîˆ‚turn14view0îˆ‚turn25view3îˆ |
| `exp_stage4b_outguess_positive_negative_matrix_v1` | The harness should prove it can separate known stego positives from negatives before touching new LP targets. | Known OutGuess/OpenPuff positives and locally controlled negatives. | 12 | Historical positives plus synthetic negatives. | low | needs assets/tool | Stage 4F | îˆ€citeîˆ‚turn23view2îˆ‚turn39search2îˆ‚turn39search11îˆ |
| `exp_stage4b_mp3_regression_v1` | Deterministic hexdump/string scans should reproduce known Instar behaviour and avoid â€œaudio mysticismâ€. | `761.mp3`, Interconnectedness asset, one negative audio control. | 9 | Known-positive/known-negative strings. | low | needs assets | Stage 4F | îˆ€citeîˆ‚turn39search1îˆ‚turn39search15îˆ |
| `exp_stage4b_source_health_audit_v1` | Fragile public sources should be locked before they vanish. | Top-priority public links only. | 20 sources | Manual checksum confirmation on a subset. | low | auto-runnable as audit tooling | Stage 4B | îˆ€citeîˆ‚turn19view0îˆ‚turn19view2îˆ‚turn32view6îˆ‚turn32view9îˆ |
| `exp_stage4b_visual_negative_controls_v1` | Visual scoring needs pareidolia controls before any image-derived seed scoring. | Braille/constellation/binary candidate tables from promoted motifs. | 60 | Randomised motif orderings and polarity flips. | low | auto-runnable after implementation | Stage 4D | îˆ€citeîˆ‚turn38view3îˆ‚turn38view6îˆ‚turn13view0îˆ‚turn13view1îˆ |

The first five above are the ones worth running soonest. They are small, explicit, and each one either tightens the evidence surface or retires a class of bad ideas.

## Immediate Codex stages, deferrals, and site privacy

The next five stages should follow the repositoryâ€™s own current trajectory rather than improvising a new one. The repo already says Stage 4B is next, and that is the correct choice. îˆ€citeîˆ‚turn42view3îˆ

| Stage | Objective | Likely files/areas | Acceptance criteria | Stop condition | Evidence |
|---|---|---|---|---|---|
| `Stage 4B â€” website-derived source-lock triage and visual observation intake` | Promote high-value public sources and exact visual claims from the site into the registry. | `data/locks`, `data/observations/visual`, `docs/history`, `research-log`, source schemas. | Top source set locked; cuneiform/dot observations created with provenance. | Stop if claims lack exact page/image anchors. | îˆ€citeîˆ‚turn42view3îˆ‚turn30view0îˆ |
| `Stage 4C â€” cuneiform and dot annotation pack` | Add coordinate-based visual records for promoted cuneiform and dot motifs. | visual schemas, annotation docs, galleries, observation YAML/JSON. | Exact region records exist; ambiguity is encoded, not hidden. | Stop if annotation cannot reach inter-review agreement. | îˆ€citeîˆ‚turn14view0îˆ‚turn13view0îˆ‚turn13view1îˆ |
| `Stage 4D â€” bounded numeric verifier pack` | Implement the delimiter, GP/rune, and Onion7 no-fudge numeric verifiers. | experiment manifests, verifier code, tests, result synthesis. | All experiments are tiny, deterministic, and logged. | Stop on noisy/non-discriminative outputs. | îˆ€citeîˆ‚turn16view1îˆ‚turn23view4îˆ |
| `Stage 4E â€” cookie exact-candidate refresh` | Generate a deduped v2 cookie hash pack from newly locked exact strings only. | web/hash schemas, manifest queue, result store. | Candidate pack is explicit, deduped, and bounded. | Stop if strings are not source-backed. | îˆ€citeîˆ‚turn12view0îˆ‚turn12view1îˆ‚turn42view3îˆ |
| `Stage 4F â€” historical stego/audio fixture lock and regression extension` | Lock assets for known positives and extend the existing harness. | stego docs, test fixtures, harness code, lock metadata. | Known positives reproducible; negatives included. | Stop if assets/toolchain cannot be reproduced locally. | îˆ€citeîˆ‚turn42view3îˆ‚turn39search1îˆ‚turn39search2îˆ |

What should **not** run yet is equally important. Do not run broad dictionary VigenÃ¨re. Do not run unconstrained prime/totient/Legendre/Mersenne sweeps. Do not run hashcat or broad cookie cracking. Do not run open-ended OutGuess brute-force across LP pages. Do not run spectrogram fishing. Do not turn AI/OCR/ML image interpretation into â€œevidenceâ€. Do not expand any dot/binary or cuneiform search before exact visual annotation exists. The repositoryâ€™s current `README.md` still defers CUDA and broad campaigns, and that remains correct. îˆ€citeîˆ‚turn42view2îˆ‚turn42view3îˆ‚turn24view2îˆ

On site privacy, the answer is blunt: keep the research utility, reduce the blast radius. Because the site is a derived Discord corpus, and because it exposes attachment-reference material and a giant searchable index surface, the safe recommendation is **noindex immediately, then move future iterations behind access control**. If a public version is kept, it should be a trimmed reviewer edition with attachment-reference pages removed and an `X-Robots-Tag: noindex, nofollow, noarchive`. îˆ€citeîˆ‚turn30view0îˆ‚turn29view0îˆ

## Final deliverables

**Recommended next Codex prompt.**
**Stage 4B â€” website-derived source-lock triage and visual observation intake.**
That is not just a good idea; it is already the next planned stage in the repository `STATUS.md`, and the Stage 4A site gives more than enough material to justify it. îˆ€citeîˆ‚turn42view3îˆ

**Top twenty leads to act on.**

| Lead | Classification | Evidence strength | False-positive risk | Action | Evidence |
|---|---|---|---|---|---|
| rtkd original-files/transcript repository | public_source_to_lock | high | low | source-lock now | îˆ€citeîˆ‚turn19view0îˆ‚turn35view0îˆ |
| scream314 puzzle-history repository | public_source_to_lock | high | low | source-lock now | îˆ€citeîˆ‚turn19view2îˆ‚turn32view1îˆ |
| Uncovering solved-method page | public_source_to_lock | high | low | source-lock now | îˆ€citeîˆ‚turn39search0îˆ |
| Uncovering Instar emergence page | public_source_to_lock | high | low | source-lock now | îˆ€citeîˆ‚turn39search1îˆ‚turn39search15îˆ |
| Uncovering 2014/OpenPuff page | public_source_to_lock | high | low | source-lock now | îˆ€citeîˆ‚turn39search2îˆ‚turn39search5îˆ |
| Uncovering OutGuess page | public_source_to_lock | high | low | source-lock now | îˆ€citeîˆ‚turn39search11îˆ‚turn32view6îˆ |
| LP transliteration page noting cross-page words | public_source_to_lock | high | low | source-lock now | îˆ€citeîˆ‚turn39search12îˆ |
| Frequency-analysis page | public_source_to_lock | high | low | source-lock now | îˆ€citeîˆ‚turn39search14îˆ |
| Raw Interconnectedness magic squares | experiment_candidate | high | low | queue bounded experiment | îˆ€citeîˆ‚turn23view4îˆ‚turn39search2îˆ |
| Mirrored three-dot delimiters | observation_to_review | medium | medium | observation-review now | îˆ€citeîˆ‚turn26view2îˆ‚turn38view5îˆ |
| Cuneiform `[17,13]/[55,1]` tuple interpretation | observation_to_review | medium | high | observation-review now | îˆ€citeîˆ‚turn14view0îˆ‚turn37view0îˆ |
| Full cuneiform value `3,722,101` | experiment_candidate | low | high | queue tiny seed test later | îˆ€citeîˆ‚turn14view3îˆ‚turn37view0îˆ |
| Exact cookie keys `167` and `761` with 64-hex values | experiment_candidate | high | medium | queue exact-match pack | îˆ€citeîˆ‚turn12view0îˆ‚turn12view1îˆ |
| Exact-span GP/rune claims from website | experiment_candidate | medium | low | verifier queue now | îˆ€citeîˆ‚turn16view1îˆ‚turn43view1îˆ |
| OutGuess/OpenPuff historical positives | public_source_to_lock | high | low | source-lock now | îˆ€citeîˆ‚turn39search2îˆ‚turn39search11îˆ |
| Wayback OutGuess docs | public_source_to_lock | medium | low | source-lock now | îˆ€citeîˆ‚turn32view6îˆ |
| Translation spreadsheet workbook | public_source_to_lock | medium | medium | lock metadata and snapshot | îˆ€citeîˆ‚turn19view3îˆ‚turn32view7îˆ |
| Attachment-reference index privacy issue | unsafe_or_private | high | medium | quarantine from public web | îˆ€citeîˆ‚turn29view0îˆ |
| Twemoji/CDN link-noise in public-links index | duplicate_of_existing_work | high | low | filter out in Stage 4B | îˆ€citeîˆ‚turn31view2îˆ |
| Geometry/mirror overlay dumps without traceable public source | too_speculative | low | extreme | quarantine | îˆ€citeîˆ‚turn33view1îˆ |

**Top twenty images and visual items to review.**

| Item | Classification | Why review | Action | Evidence |
|---|---|---|---|---|
| Page 33â€“39 cuneiform candidate marks as a cluster | observation_to_review | Highest-value visual numeric lead, but still ambiguous. | human annotation first | îˆ€citeîˆ‚turn14view0îˆ‚turn34view0îˆ |
| Page 39 small dot cluster | observation_to_review | Reappears in cuneiform/page-art discussions. | annotate coordinates | îˆ€citeîˆ‚turn37view0îˆ‚turn28view5îˆ |
| Page 5 left/right three-dot delimiter variants | observation_to_review | Actual punctuation asymmetry. | delimiter inventory | îˆ€citeîˆ‚turn26view2îˆ |
| Page 56 three-dot delimiter variants | observation_to_review | Same reason as page 5; possible boundary clue. | delimiter inventory | îˆ€citeîˆ‚turn26view2îˆ‚turn28view7îˆ |
| Big five-dot motifs mentioned across pages 24, 40, and 56 | observation_to_review | Recurring motif family; needs exact image anchors. | annotate; do not decode yet | îˆ€citeîˆ‚turn25view3îˆ |
| Small five-dot motif on page 39 | observation_to_review | Central to the 13/31 ambiguity story. | annotate; ambiguity audit | îˆ€citeîˆ‚turn25view3îˆ‚turn13view0îˆ |
| Page 34/36â€“38 â€œnumbers/pointersâ€ regions | observation_to_review | Referred to explicitly in cuneiform channel. | annotate | îˆ€citeîˆ‚turn36view0îˆ |
| 39.jpg and related user overlays | observation_to_review | Discord references suggest active visual work around page 39. | review only if tied to public page image | îˆ€citeîˆ‚turn28view5îˆ |
| 56.jpg discussion images | observation_to_review | Relevant to delimiter and â€œAn Endâ€ contextual work. | review selected safe images | îˆ€citeîˆ‚turn28view7îˆ |
| 57.jpg discussion images | observation_to_review | Relevant to mayfly/stego claims and negative controls. | review selected safe images | îˆ€citeîˆ‚turn28view6îˆ |
| Mayfly overlay claims on 57.jpg | too_speculative | Strong claim, weak public proof. | quarantine until sourced | îˆ€citeîˆ‚turn26view8îˆ |
| â€œDots encode skip indicesâ€ mayfly claim | too_speculative | Classic high-drama, low-proof claim. | quarantine | îˆ€citeîˆ‚turn26view8îˆ |
| Constellation overlays for dots | debunk_or_false_positive | Repeated and contradictory. | negative control | îˆ€citeîˆ‚turn35view0îˆ‚turn38view6îˆ |
| Braille overlays for dots | debunk_or_false_positive | Many readings possible. | negative control | îˆ€citeîˆ‚turn38view3îˆ |
| Binary-clock analogies | too_speculative | Interesting, but weakly anchored. | keep as low-priority note | îˆ€citeîˆ‚turn38view0îˆ‚turn38view2îˆ |
| Page-art tree motifs | observation_to_review | Possible motif catalogue value, but no operational clue yet. | annotate, do not derive ciphers | îˆ€citeîˆ‚turn26view9îˆ |
| Wing/tree section images | observation_to_review | Recurrent section-art candidate; needs structured catalogue. | visual registry only | îˆ€citeîˆ‚turn30view0îˆ |
| Spiral/branch section motifs | observation_to_review | Worth cataloguing purely as section art and route-hypothesis context. | registry only | îˆ€citeîˆ‚turn33view8îˆ |
| Nebuchadnezzar / mirrored-hands comparisons | observation_to_review | Historical imagery context, not direct solve evidence. | source-lock and annotate | îˆ€citeîˆ‚turn20view4îˆ‚turn33view4îˆ |
| Low-bit / greyscale nested-image historical example | public_source_to_lock | Good historical positive/negative context for image pipeline tuning. | source-lock and document | îˆ€citeîˆ‚turn17view2îˆ |

**Top twenty public links to source-lock.**

| Source | Class | Action | Evidence |
|---|---|---|---|
| rtkd original files/transcripts repository | strong_community_technical | lock now | îˆ€citeîˆ‚turn19view0îˆ‚turn35view0îˆ |
| scream314 repository | strong_community_technical | lock now | îˆ€citeîˆ‚turn19view2îˆ‚turn32view1îˆ |
| Complete Cicada3301 Archive repository | secondary_archive | lock selected assets now | îˆ€citeîˆ‚turn18view8îˆ |
| Uncovering solved LP methods page | strong_community_technical | lock now | îˆ€citeîˆ‚turn39search0îˆ |
| Uncovering LP unsolved pages page | strong_community_technical | lock now | îˆ€citeîˆ‚turn39search6îˆ |
| Uncovering LP transliteration page | strong_community_technical | lock now | îˆ€citeîˆ‚turn39search12îˆ |
| Uncovering frequency-analysis page | strong_community_technical | lock now | îˆ€citeîˆ‚turn39search14îˆ |
| Uncovering Instar emergence page | strong_community_technical | lock now | îˆ€citeîˆ‚turn39search1îˆ‚turn39search15îˆ |
| Uncovering What Happened Part 1 (2014) page | strong_community_technical | lock now | îˆ€citeîˆ‚turn39search2îˆ‚turn39search5îˆ |
| Uncovering OutGuess page | strong_community_technical | lock now | îˆ€citeîˆ‚turn39search11îˆ |
| Wayback OutGuess site snapshot | reference_only_tooling | lock now | îˆ€citeîˆ‚turn32view6îˆ |
| Cygwin OutGuess package page | reference_only_tooling | lock now | îˆ€citeîˆ‚turn32view6îˆ |
| MP3Stego repository | reference_only_tooling | lock reference | îˆ€citeîˆ‚turn22view3îˆ |
| `rtkd/iddqd` 2013/02 asset tree | strong_community_technical | lock now | îˆ€citeîˆ‚turn20view8îˆ‚turn32view0îˆ |
| Wayback `infotomb` mirror for historical text | secondary_archive | lock metadata | îˆ€citeîˆ‚turn32view9îˆ |
| Google `tranlsations` workbook | secondary_archive | lock snapshot cautiously | îˆ€citeîˆ‚turn19view3îˆ‚turn32view7îˆ |
| Complete Archive `magicsquares.txt` | secondary_archive | lock now | îˆ€citeîˆ‚turn18view8îˆ‚turn23view4îˆ |
| Complete Archive `li676-224_server-status_orig.txt` | secondary_archive | lock later | îˆ€citeîˆ‚turn18view8îˆ |
| Uncovering 2012 split/alternate-path pages | negative_control_material | lock for fake-path documentation | îˆ€citeîˆ‚turn32view3îˆ |
| 3301archive / old number-square essays | speculative | reference-only | îˆ€citeîˆ‚turn32view8îˆ |

**Top twenty debunks and false positives to preserve.**

| Item | Why preserve it | Evidence |
|---|---|---|
| 13 as a forced dot value | Not forced; depends on orientation/anchor. | îˆ€citeîˆ‚turn13view0îˆ |
| 31 as a forced dot value | Same problem. | îˆ€citeîˆ‚turn13view1îˆ |
| Braille decodes of page-art dots | Too many plausible readings. | îˆ€citeîˆ‚turn38view3îˆ |
| Constellation matches for dots | Resemblance-driven, contradictory. | îˆ€citeîˆ‚turn35view0îˆ‚turn38view6îˆ |
| Eurion-style dot theory | Cute, not grounded. | îˆ€citeîˆ‚turn38view6îˆ |
| Cuneiform readout treated as fact | Visual reading still disputed. | îˆ€citeîˆ‚turn14view0îˆ |
| Page-33 pair-swapping/base-60 method yielding â€œTH,Eâ€ | The arithmetic itself was challenged in-channel. | îˆ€citeîˆ‚turn37view1îˆ‚turn36view6îˆ |
| â€œShift by -25 shows trigramsâ€ style cuneiform claims | Too under-specified and post-hoc. | îˆ€citeîˆ‚turn37view3îˆ |
| Broad OutGuess brute force on LP pages | Repeated fake file-type hits. | îˆ€citeîˆ‚turn23view3îˆ‚turn24view0îˆ |
| MP3Stego excitement as proof | Needs positive controls, not vibes. | îˆ€citeîˆ‚turn23view0îˆ |
| Spectrogram fishing on Instar | Historical checking reportedly found nothing meaningful. | îˆ€citeîˆ‚turn23view2îˆ‚turn39search1îˆ |
| AI-generated page solves | Hallucinates even solved pages. | îˆ€citeîˆ‚turn24view2îˆ |
| â€œLP only has 16 original pagesâ€ myth | Conflicts with public LP working corpus practice. | îˆ€citeîˆ‚turn19view4îˆ‚turn30view0îˆ |
| Unsourced TikTok / new-Cicada claims | No PGP, no trust. | îˆ€citeîˆ‚turn24view1îˆ‚turn43view0îˆ |
| Dictionary-looking prime/totient hits | Easy nonsense. | îˆ€citeîˆ‚turn24view3îˆ |
| 3301-minus-value prime games without fixed rules | Arithmetic massage trap. | îˆ€citeîˆ‚turn14view1îˆ‚turn15view0îˆ |
| Broad literature-key fishing | Already low-yield, weakly anchored. | îˆ€citeîˆ‚turn42view3îˆ‚turn20view2îˆ‚turn21view4îˆ |
| Geometry/mirror-sequence dumps without source lineage | Unsupported structure masquerading as method. | îˆ€citeîˆ‚turn33view1îˆ |
| Mayfly-dot skip-index theory | Big claim, tiny proof. | îˆ€citeîˆ‚turn26view8îˆ |
| Public attachment-reference indexing | Not a solve path; just a privacy footgun. | îˆ€citeîˆ‚turn29view0îˆ |

**Top ten bounded experiments to run next.**

| Rank | Experiment | Candidate count | Why this one next | Evidence |
|---:|---|---:|---|---|
| 1 | `exp_stage4b_gp_rune_verifier_batch002` | 20 | Fastest credibility gain: reject or confirm exact claims cheaply. | îˆ€citeîˆ‚turn16view1îˆ‚turn43view1îˆ |
| 2 | `exp_stage4b_dot_ambiguity_audit_v1` | 140 | Turns 13/31 mythology into measurable ambiguity. | îˆ€citeîˆ‚turn13view0îˆ‚turn13view1îˆ |
| 3 | `exp_stage4b_delimiter_handedness_v1` | 16 | Best visual clue tied to actual text structure. | îˆ€citeîˆ‚turn26view2îˆ‚turn38view5îˆ |
| 4 | `exp_stage4b_onion7_raw_routes_v1` | 96 | Uses a known historical positive artefact with no arithmetic fudge. | îˆ€citeîˆ‚turn23view4îˆ‚turn39search2îˆ |
| 5 | `exp_stage4b_cookie_pack_v2` | 384 | Still bounded, still exact-match, still sourceable. | îˆ€citeîˆ‚turn12view0îˆ‚turn12view1îˆ‚turn42view3îˆ |
| 6 | `exp_stage4b_cuneiform_reading_pack_v1` | 32 | Worth doing only after annotation starts. | îˆ€citeîˆ‚turn14view0îˆ‚turn14view3îˆ |
| 7 | `exp_stage4b_number_square_no_fudge_v1` | 128 | Good retirement test for prime-massage theories. | îˆ€citeîˆ‚turn14view1îˆ‚turn23view4îˆ |
| 8 | `exp_stage4b_visual_negative_controls_v1` | 60 | Needed before any image-derived scoring. | îˆ€citeîˆ‚turn38view3îˆ‚turn38view6îˆ |
| 9 | `exp_stage4b_outguess_positive_negative_matrix_v1` | 12 | Necessary harness extension, but tool/assets first. | îˆ€citeîˆ‚turn42view3îˆ‚turn39search11îˆ |
| 10 | `exp_stage4b_mp3_regression_v1` | 9 | Useful only after source-locking audio assets. | îˆ€citeîˆ‚turn39search1îˆ‚turn39search15îˆ |

**Recommended next Codex prompt title.**
**Stage 4B â€” website-derived source-lock triage and visual observation intake.** îˆ€citeîˆ‚turn42view3îˆ

**Whether the Stage 4A generated site should stay public, be noindexed, or be access-controlled.**
**Noindex immediately; access-control for future iterations.** The current site is thoughtfully redacted, but it is still a large derived Discord corpus, and the attachment-reference surface is too broad for casual indexing. Keep a trimmed public summary if desired; keep the full reviewer site private or semi-private. îˆ€citeîˆ‚turn30view0îˆ‚turn29view0îˆ

**What should remain ignored or deferred.**
Broader VigenÃ¨re key expansion, dictionary-scale key search, page-wide image-derived text experiments, unconstrained prime-family sweeps, cookie cracking beyond exact explicit packs, CUDA/GPU work, open-ended OutGuess fuzzing of LP pages, spectrogram fishing, and any AI-led visual interpretation should remain deferred. The repoâ€™s own current boundaries still make that the correct call. îˆ€citeîˆ‚turn42view2îˆ‚turn42view3îˆ
