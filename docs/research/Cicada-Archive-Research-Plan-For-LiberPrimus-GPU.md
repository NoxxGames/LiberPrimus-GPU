> Stage 3K note: This is a research input, not a solution claim. It contains source classifications and hypotheses requiring validation. Generated experiments must still use manifests and controls, and observations remain noncanonical until reviewed.
# Cicada Archive Research Plan for LiberPrimus-GPU

## Executive summary

The public `LiberPrimus-GPU` README now describes a project that already has ten solved-page baselines passing through the registry and manifest path, a CPU transform registry, JSONL/SQLite result-store foundations, CI consistency checks, a bounded CPU execution harness, and a public status in which the canonical corpus remains inactive, page boundaries remain reviewable, and CUDA work is explicitly deferred until CPU references and parity tests exist. The same README also records that the bounded Stage 3Aâ€“3I text campaigns have stayed conservative: simple Caesar/affine sweeps, calibration runs, small explicit-key VigenÃ¨re packs, p56-local prime-minus-one offset work, reset/advance ablations, and a historical motif key-pack all produced noisy leads rather than solve-grade evidence. In other words: the repository has already done the right thing on the text side, and the next high-value move is **not** â€œmore of the same, just fasterâ€ and definitely not â€œCUDA first.â€ It is **historical archive ingestion plus a deterministic observation registry** that can seed better bounded text experiments later. îˆ€citeîˆ‚turn23view0îˆ‚turn23view1îˆ‚turn23view2îˆ‚turn23view3îˆ‚turn23view4îˆ

That recommendation is evidence-grounded by Cicadaâ€™s earlier puzzle behaviour. Across 2012â€“2017, the documented puzzle chain repeatedly used OutGuess or other side-channel artefacts, book ciphers, prime-number clues, image dimensions, coordinates, Tor hidden services, timed web pages, cookies, audio files, and signed authenticity warnings. In 2012, `final.jpg` yielded an OutGuess book-code message, and the phone step explicitly tied the next stage to two prime image dimensions multiplied by `3301`; the same 2012 branch then used coordinates and more image steganography. In 2013, another image again required OutGuess, the book cipher keyed off *Liber AL vel Legis*, the live image printed primes up to `3301` with pauses at `1033` and `3301`, the ISO contained `761.mp3`, and the later onion-stage test page reportedly set the `167` and `761` cookies. Post-2014 material returned solvers to *Liber Primus*, with signed warnings to verify messages and avoid false paths. Those are exactly the kinds of historical artefacts a serious LP workbench should ingest before widening the text search space. îˆ€citeîˆ‚turn9view0îˆ‚turn10view0îˆ‚turn10view1îˆ‚turn10view2îˆ‚turn11view0îˆ‚turn12view0îˆ‚turn12view3îˆ‚turn13view1îˆ‚turn7view4îˆ‚turn6view5îˆ‚turn6view7îˆ

The blunt recommendation is therefore this. **Build Stage 3J as a historical archive and observation-registry stage.** Lock the archive sources, hash them, ingest deterministic metadata, and create reviewable records for web/onion artefacts, cookie hashes, image dimensions, outguessable carriers, audio metadata, and visual/numeric observations. Then run a small set of bounded CPU experiments derived from the strongest historical observations: cookie-hash literal packs, archive image metadata/outguess regression, and tiny numeric-seed packs driven by documented numbers like `167`, `761`, `1033`, `3301`, and the Onion 7 page-15 table. Only after that should the project consider broader archive-derived text campaigns. CUDA still belongs later, after those seed families have stable CPU definitions and parity tests. îˆ€citeîˆ‚turn23view1îˆ‚turn23view2îˆ‚turn12view0îˆ‚turn8view0îˆ‚turn13view1îˆ

The key risks are the usual Cicada traps, wearing a slightly more academic hat: crypto pareidolia from short strings and images, archive drift, post-hoc community mythology, leaked and modified materials, and silent mixing of â€œsigned/primaryâ€ with â€œinteresting but unverified.â€ The 2017 signed message explicitly warns, â€œBeware false paths,â€ and the 2015 Twitter message warns that any unsigned message should be considered fake. The project should take those warnings literally and encode them into policy, schemas, and CI. îˆ€citeîˆ‚turn6view5îˆ‚turn7view0îˆ

## Source map

For this project, the cleanest working split is:

| Source class | What belongs here | How to treat it |
|---|---|---|
| **Primary or near-primary signed record** | Signed Cicada messages preserved on Uncovering Cicada; archive PDFs and docs for 2012â€“2017; signed post-2014 messages; the Necrome refutation; the April 2017 message. îˆ€citeîˆ‚turn9view6îˆ‚turn6view5îˆ‚turn16view8îˆ‚turn24view0îˆ | Mirror first. Prefer as chronology and authenticity anchors. |
| **Strong community technical source** | `rtkd/iddqd`, which explicitly presents itself as â€œunmodified files, transcription and other assets,â€ including full/unsolved LP images, transcription sets, keys, and translations; `scream314/cicada3301`, whose `pages_and_ciphers.md` is a long technical index of pages and methods. îˆ€citeîˆ‚turn21search0îˆ‚turn22view0îˆ | Treat as source-locked working references. Useful for reproducible ingestion and regression. |
| **Secondary archive** | `cicada-solvers/The-Complete-Cicada3301-Archive`, which is a public fork containing year folders for 2012, 2013, 2014, 2015, 2016, 2017, `EXTRA WIKI PAGES`, and `assets`; `krisyotam/cicada3301`, a public aggregate archive updated in 2026. îˆ€citeîˆ‚turn16view0îˆ‚turn16view1îˆ‚turn16view2îˆ‚turn16view3îˆ‚turn16view4îˆ‚turn17view0îˆ‚turn18view0îˆ‚turn21search8îˆ | Very useful for mirroring and convenience, but always record provenance and hash before trusting content. |
| **Reference-only tooling** | `rtkd/idkfa`, `relikd/LiberPrayground`, `lipeeeee/gematria`. These are useful as tool ideas, not as historical authority. îˆ€citeîˆ‚turn21search1îˆ‚turn21search2îˆ‚turn21search3îˆ | Borrow ideas. Do not treat outputs as evidence. |
| **Archived claims requiring caution** | 2013 part-2 question page and cookies, because the test page and follow-on email were leaked rather than preserved as a signed official export; â€œThe Leaked Emailâ€ page, whose leaked version was modified and initially disputed, though Uncovering now documents a later rediscovered PGP-signed variant; â€œPossible hints never used.â€ îˆ€citeîˆ‚turn12view0îˆ‚turn12view3îˆ‚turn37view2îˆ‚turn34search0îˆ | Use only as archived claims or negative controls until independently source-locked. |
| **Speculation-heavy community pages** | â€œOnion 7: numbers on page 15â€ for derived spiral/Fibonacci interpretations; â€œSymbols/Drawing/Art of Liber Primusâ€; various debate notes in `EXTRA WIKI PAGES`. Those pages themselves contain caveats such as â€œnot verified or cleaned up,â€ â€œdoes not confirm anything,â€ and â€œwe donâ€™t know yet.â€ îˆ€citeîˆ‚turn8view0îˆ‚turn35view0îˆ‚turn16view3îˆ | Excellent seed registries. Terrible things to trust blindly. |

The archive repository is especially valuable because it is already organised in the way an ingestion pipeline wants to see it. The 2012 folder contains `additional docs`, `additional media`, `MIDI puzzle`, websites, and PDF/DOCX â€œwhat happenedâ€ writeups; the 2013 folder contains `additional docs`, `additional files`, `additional images`, and the 2013 PDFs; the 2014 folder contains `Liber Primus`, `Websites`, `additional docs`, `additional images`, and 2014 PDFs; the 2015, 2016, and 2017 folders likewise carry PDFs plus â€œextra docsâ€ or â€œadditional imagesâ€; and the `assets` tree contains year buckets with raw puzzle media. The 2012 assets directory even includes image files beside matching `.out` files, which makes it an unusually strong positive-control set for stego regression tests. îˆ€citeîˆ‚turn16view0îˆ‚turn16view1îˆ‚turn16view2îˆ‚turn17view0îˆ‚turn18view0îˆ‚turn16view4îˆ‚turn16view5îˆ‚turn16view6îˆ

The highest-priority mirroring targets are therefore straightforward. First: `rtkd/iddqd`; second: `scream314/cicada3301` technical markdown; third: the archive repositoryâ€™s `2014/Liber Primus`, `2014/Websites`, `2014/additional images`, `2013/additional images`, `2013/additional files`, and `assets/2012` directories; fourth: Uncovering Cicadaâ€™s pages for 2012, 2013, 2014/Post-2014, 2015, 2016, 2017, Onion 7, and the LP symbols page. Anything more weakly sourced than that should be retained as a reference-only pointer until the project has URL, fetch date, hash, and provenance notes locked. îˆ€citeîˆ‚turn20view4îˆ‚turn20view3îˆ‚turn19view0îˆ‚turn20view0îˆ‚turn20view1îˆ‚turn16view5îˆ‚turn8view4îˆ‚turn11view0îˆ‚turn11view1îˆ‚turn5view2îˆ‚turn5view3îˆ‚turn5view4îˆ‚turn8view0îˆ‚turn35view0îˆ

## Historical techniques and artefacts

A serious LP workbench should model historical Cicada techniques as a set of **documented mechanism families**, not as a single mythologised aesthetic.

| Historical branch | Verified or strongly documented mechanism | Why it matters for LP-GPU |
|---|---|---|
| **2012** | `final.jpg` required OutGuess; its hidden message explicitly introduced a book code. The resulting phone call said the original image had three associated primes, naming `3301` and implying the other two were the prime image dimensions `509` and `503`; multiplying them produced `845145127.com`. The coordinate page then used another stego-bearing image and a signed coordinate list. îˆ€citeîˆ‚turn9view0îˆ‚turn10view0îˆ‚turn10view1îˆ‚turn10view2îˆ | This is strong historical evidence for treating **image dimensions, hidden payload extraction, prime arithmetic, and resource naming** as legitimate experiment seeds. |
| **2013 early chain** | Another image again required OutGuess. The extracted riddle pointed to *Liber AL vel Legis* as a book-cipher source. The Dropbox ISO then booted while printing primes up to `3301`, with pauses at `1033` and `3301`. îˆ€citeîˆ‚turn11view0îˆ | This supports **external-text dependency**, **prime-sequence motifs**, and **number reuse across media**. |
| **2013 audio branch** | The ISO contained `761.mp3`; Uncovering records its ID3 title as â€œThe Instar Emergence,â€ notes a hidden hexdump message, and records the community observation that the track length is `167` seconds while the filename is `761`. îˆ€citeîˆ‚turn13view1îˆ‚turn13view2îˆ | This justifies **audio metadata extraction**, **exact duration capture**, **filename numerics**, and **manual reviewable spectrogram work**. |
| **2013 onion/test branch** | The leaked late-stage test page reportedly set two cookies: `167=<64-hex>` and `761=<64-hex>`. The follow-on email reportedly required candidates to build a TCP server, expose it as a Tor hidden service, and implement commands including `BASE29`, with `3301 -> 3QO` shown explicitly in the example protocol. îˆ€citeîˆ‚turn12view0îˆ‚turn12view3îˆ‚turn12view4îˆ | This is one of the strongest reasons to add **cookie/hash analysis**, **hidden-service artefact modelling**, and **base-29 numerical representation packs**. |
| **2014 to post-2014** | The post-2014 LP path records a signed message saying â€œLiber Primus is the way â€¦ their numbers are the direction.â€ The same page also records that the later image was `563 x 569`, both prime, that the background â€œblocksâ€ were JPEG compression noise rather than a QR code, and that OutGuess recovers the same signed text. îˆ€citeîˆ‚turn7view4îˆ‚turn7view5îˆ | This legitimises **prime-dimension observations** and **negative controls against visual over-reading**. |
| **2015 and 2017 authenticity rules** | The 2015 Twitter message says any unsigned message should be considered fake; the 2017 signed message warns solvers to â€œBeware false pathsâ€ and to verify PGP signatures against key `7A35090F`. îˆ€citeîˆ‚turn7view0îˆ‚turn6view5îˆ | This should become a **project policy rule**, not a footnote. |
| **Community-only visual numerics** | The LP symbols page claims cuneiform-like marks, five-dot motifs, roots/Fibonacci, mayflies, oak trees, and other symbols, but it also explicitly says â€œit does not confirm anythingâ€ and â€œwe donâ€™t know yet.â€ Onion 7â€™s page-15 number article records a 4Ã—4 number table and community prime/Fibonacci spiral derivations, while also flagging some related snippets as â€œnot verified or cleaned up.â€ îˆ€citeîˆ‚turn35view0îˆ‚turn8view0îˆ | These are **seed registries**, not evidence. Encode them, then test them conservatively. |

The practical carryover is fairly sharp. **Strong historical carryover** includes stego extraction, exact filenames, image dimensions, prime-number recurrences, base-29/base-Gematria numerics, external-text dependence, and signed-message verification. **Medium-strength carryover** includes cookies, form/page artefacts, resource names, and audio metadata. **Weak carryover** includes magic squares, constellation readings, Kabbalistic trees, and other symbolic/numerological interpretations that currently rely on community pattern-matching rather than signed or source-locked material. The archive itself already contains folders named `godel escher bach`, `the growing string`, `Self-Reliance and Other Essays`, `Magicsquare.jpg`, and â€œ5x5 Magic Squares based on numbers from onion5 portrait.jpg,â€ which is exactly why the registry must keep â€œarchived existenceâ€ separate from â€œcredible clue.â€ îˆ€citeîˆ‚turn20view2îˆ‚turn19view0îˆ

One source-reliability subtlety matters a lot. â€œThe Leaked Emailâ€ is not a clean binary case of true or false. Uncovering documents that the first widely circulated version was a supposedly leaked and modified pastebin and that it was controversial because it was not initially PGP-verified; the same page also documents a later rediscovered 2024 version signed seconds after the already-known one. So the correct treatment is neither â€œignore itâ€ nor â€œtreat every leaked paraphrase as ground truth,â€ but rather â€œmirror the signed variant, retain the modified leak as provenance context, and never use unauthenticated wording as an experiment seed when a signed wording exists.â€ îˆ€citeîˆ‚turn37view2îˆ

## Onion acquisition and cookie analysis

The currently documented cookie observations come from the leaked 2013 onion-stage test page: after a timed question set, the page reportedly set `167=6941f707ff39d259ff71657a79cb6b54c184d2f0455810109c1a960860bde0e6` and `761=7bc1e7805ccfa518920f0d94fc4e8f7dbd83287a03b337b89109cd2287befae5`. Uncovering also records the community note that `167` and `761` relate to the `761.mp3` branch and the `167`-second track length. Historically important? Yes. Primary? No. This is an **archived claim from a leaked stage**, not a first-party HTTP capture. Treat it as a high-interest but non-canonical web artefact. îˆ€citeîˆ‚turn12view0îˆ

On format alone, those cookie values are **64-character hexadecimal strings**. That does **not** uniquely identify an algorithm, but it is consistent with 256-bit digest families such as SHA-256 and SHA-512/256. NISTâ€™s approved hash list explicitly includes both SHA-256 and SHA-512/256 as 256-bit outputs. So the safe engineering move is: start with SHA-256 sanity packs because they are the simplest and most common 256-bit candidate, but store the algorithm field explicitly and be prepared to expand later if the small packs are exhausted. îˆ€citeîˆ‚turn12view0îˆ‚turn33search3îˆ‚turn33search4îˆ

I also recommend a very small local sanity check before anything glamorous. In my own bounded check, a manually curated pack of obvious literals and trivial whitespace/case variants drawn from the historical record produced **no exact SHA-256 match** for either cookie value. That is not evidence of anything beyond â€œthe answer is probably not embarrassingly literal,â€ but it is enough to justify keeping the first preimage stage tiny and structured rather than jumping to dictionary-scale or GPU-scale attacks. The right first packs are therefore: direct historical literals; base-29 and numeric renderings of historically important numbers; and short concatenation packs built only from source-locked tokens. Anything broader should wait. îˆ€citeîˆ‚turn12view0îˆ‚turn13view1îˆ‚turn10view0îˆ‚turn11view0îˆ

For acquisition architecture, the safest design is **archive-first and Tor-second**. Build the schemas and CLI now, but initially ingest only already archived material from GitHub and public mirrors. When live acquisition is eventually needed, use a local Tor daemon with SOCKS5 and a localhost-only control port; Stem is the obvious Python control library for driving that control port, and Torâ€™s own specifications make clear that circuit/stream isolation matters because streams that share a circuit leak linkability. On the browser side, use Playwright with one fresh `BrowserContext` per capture job so cookies and cache do not bleed across jobs, and close the context explicitly so screenshots and artefacts flush deterministically. Tor Browser itself remains useful for **manual** spot checks, but I would not make it the primary acquisition engine. That is an inference from the official browser/privacy model, not an explicit Tor statement. îˆ€citeîˆ‚turn36view4îˆ‚turn36view5îˆ‚turn36view6îˆ‚turn36view0îˆ‚turn36view1îˆ‚turn36view2îˆ

The operational policy should be strict enough to survive future embarrassment. No plugins or extra browser add-ons; Tor Browserâ€™s own support pages strongly discourage them because they weaken privacy and increase trackability. No arbitrary downloads from unvetted onions. No personal accounts. No broad crawling. No capture without an explicit allowlist. Every capture gets raw HTML, browser-rendered DOM snapshot, response headers, cookies, linked-resource manifest, screenshot, and SHA-256 hashes for each stored artefact. Use â€œnew identityâ€ or fresh isolated sessions between jobs so cookies and history do not leak across captures. îˆ€citeîˆ‚turn36view8îˆ‚turn36view7îˆ‚turn27search1îˆ

A practical schema set for this module should be small and boring:

```json
{
  "onion_page_record": {
    "record_id": "hist-2013-p7amjopgric7dfdi-v1",
    "url": "http://p7amjopgric7dfdi.onion/",
    "capture_mode": "archive_import",
    "provenance_class": "archived_claim",
    "html_sha256": "â€¦",
    "dom_sha256": "â€¦",
    "screenshot_sha256": "â€¦",
    "header_set_sha256": "â€¦",
    "cookie_names": ["167", "761"],
    "resource_count": 0,
    "signed_status": "unsigned_page"
  }
}
```

```json
{
  "cookie_hash_record": {
    "record_id": "cookie-2013-167-v1",
    "page_record_id": "hist-2013-p7amjopgric7dfdi-v1",
    "cookie_name": "167",
    "cookie_name_int": 167,
    "cookie_value": "6941f707ff39d259ff71657a79cb6b54c184d2f0455810109c1a960860bde0e6",
    "value_format": "hex64",
    "candidate_algorithm_status": "unknown_256bit_hex",
    "evidence_class": "archived_claim"
  }
}
```

The conclusion here is simple. **A Tor-backed acquisition module is worth designing now, but not worth deploying as a live-capture crawler yet.** What is worth building immediately is the archive-import path, the schema, the hashing, the resource manifest, and the experiment harness for tiny cookie preimage packs.

## Image and audio observation registry

The historical archive already contains enough material to justify a proper deterministic image/audio pipeline. The 2013 archiveâ€™s `additional images` folder includes `761 extra metadata.png` and `A draft spectral anlysis.png`; the 2014 `additional images` folder includes `Onion_4_adress_runes.jpg`, `Onion_4_adress_runes.png`, `Magicsquare.jpg`, `spectogram.jpg`, `OutguessfromLiberPrimusPage6.jpg`, and `Runes-warning.jpg`; the 2014 `Websites` folder contains archived onion-site materials; and the 2014 `Liber Primus` folder includes enhanced rune images, stacked pages, full image sets, and text/numerical transcript files. Those are precisely the artefacts from which a reproducible observation registry can be built. îˆ€citeîˆ‚turn20view0îˆ‚turn19view0îˆ‚turn20view3îˆ‚turn20view4îˆ

The first five observations I would encode are these:

| Observation | Status | Why encode it first | How it should be used |
|---|---|---|---|
| **Prime image dimensions tied to puzzle progression**: 2012 `509Ã—503` with `3301`; post-2014 image `563Ã—569`, both prime. îˆ€citeîˆ‚turn10view0îˆ‚turn7view5îˆ | **Verified fact / strong archive** | Historically documented, objective, and already known to have been meaningful at least once. | Seed tiny numeric offset packs; never use alone as solve evidence. |
| **`761.mp3` plus `167`-second duration motif**. îˆ€citeîˆ‚turn13view1îˆ | **Archived claim with strong technical value** | Objective metadata and exact duration are deterministic to measure. | Encode as a numeric-clue cluster for cross-media correlation. |
| **2013 cookie pair `167`/`761` and their 64-hex values**. îˆ€citeîˆ‚turn12view0îˆ | **Archived claim** | Strongest web-specific observation currently documented. | Use only for tiny preimage packs and web artefact modelling. |
| **Onion 7 page-15 raw 4Ã—4 number table**. îˆ€citeîˆ‚turn8view0îˆ | **Archived claim grounded in a specific image/page** | Concrete numeric material with documented community transforms. | Use raw values and derived residues in bounded seed packs. |
| **LP visual-symbol candidates**: cuneiform-like numerals and five-dot motifs. The symbols page itself warns these do not confirm anything. îˆ€citeîˆ‚turn35view0îˆ | **Weak hypothesis / registry-only** | Important enough to encode; weak enough to quarantine. | Encode with low confidence and require human review before any text experiment uses them. |

For the cuneiform-like pattern, the community symbols page explicitly asserts the reading `17 13 55 1`, and further asserts the pairwise base-60 interpretations `1033` and `3301`. That page is not primary evidence, but the arithmetic is easy to verify once the reading is assumed: `17Ã—60+13 = 1033`, `55Ã—60+1 = 3301`, while the full four-digit sexagesimal number is `3,722,101`; all three are prime, and their residues mod 29 are `18`, `24`, and `9`, respectively. That makes them **excellent bounded seed values** and **terrible grounds for a solve claim**. The correct project status for such an observation is therefore: archived symbol reading, weak confidence, seed-only. îˆ€citeîˆ‚turn35view0îˆ

The five-dot pattern is an even better example of why the registry must be explicit about uncertainty. If one models a five-dot motif as a simple 5-bit row with exactly three filled and two unfilled positions, the forward values are `{7, 11, 13, 14, 19, 21, 22, 25, 26, 28}`. So `13` is a possible reading, but only one of ten, and `31` does **not** arise from that strict three-filled/two-empty model at all. That makes simple â€œ13/31â€ internet lore exactly the sort of thing that should be recorded as a **rejected simplification** or at best a **weak hypothesis**, not directly translated into a text campaign.

The deterministic pipeline should stay old-school. For images: file hashing, ExifTool metadata extraction, ImageMagick `identify` for dimensions/corruption/format, channel separation, threshold grids, bit-plane extraction, edge maps, connected-component counts, symmetry deltas, JPEG quantisation tables, perceptual hashes, and OutGuess where the format permits. ExifTool is explicitly built to read and write metadata across a wide variety of files; ImageMagick `identify` reports file format, width, height, colours, bytes, and corruption; and OutGuess is designed to extract hidden data from redundant bits in JPEG/PPM/PNM carriers. îˆ€citeîˆ‚turn36view9îˆ‚turn36view10îˆ‚turn36view11îˆ

For audio: `ffprobe` for stream/container metadata and tags, fixed-parameter spectrogram generation with FFmpeg, framehash or framemd5 outputs for regression, exact-duration and bitrate capture, polarity/reversal tests, and null controls such as reversed or phase-scrambled copies. FFmpegâ€™s tooling is well suited to deterministic metadata and frame-level hash output, and the `showspectrumpic` family exists precisely to convert audio into a single spectrum image; but spectrograms are also an almost perfect false-positive machine if one lets parameter search wander. The project should therefore treat any detected â€œline sequencesâ€ as observations requiring matched null controls, not as decipherment evidence. îˆ€citeîˆ‚turn36view12îˆ‚turn36view13îˆ‚turn36view14îˆ

Third-party AI image analysis is **not worth using now**. A local model may eventually be useful for segmentation assistance or clustering, but every AI-generated label should be stored only as a reviewable hypothesis attached to a deterministic crop and should never become a seed without a human-approved observation record. Right now, the opportunity cost is obvious: the project still has higher-value tasks that are deterministic, auditable, and much harder to fool.

## Ranked bounded experiment backlog

Below is the backlog I would actually queue for Codex. The first five are deliberately small enough to sit comfortably inside the current standing operator policy if the implementation exists.

| Priority | Experiment ID | Hypothesis | Inputs | Exact bounded parameters | Candidate count | Runtime estimate on i9-9900K | Policy status | False-positive risk | Recommended stage |
|---|---|---|---|---|---:|---:|---|---|---|
| 1 | `hist_cookie_literal_pack_v1` | Cookie preimages may be direct historical literals. | Two cookie hashes; curated literal list from signed messages, onion addresses, filenames, and numbers. | 40 literals Ã— 12 byte-exact variants (`raw`, lower, upper, `LF`, `CRLF`, trailing/leading space, etc.). | **480** | **< 1 s** | **Auto-runnable now** | Low if every tested byte string is logged exactly. | Stage 3J/3L |
| 2 | `archive_image_manifest_v1` | Deterministic file facts should be source-locked before any image-derived seed test. | 40 archived images from 2012/2013/2014/2017. | 8 fixed extractors per file: SHA-256, ExifTool, identify, channel split stats, JPEG quant tables, pHash, OutGuess eligibility, dimensions-prime flag. | **320 file-ops** | **< 2 min** | **Auto-runnable now** | Very low. | Stage 3J/3K |
| 3 | `outguess_regression_v1` | The local stego toolchain is trustworthy only if it reproduces known positives and stays quiet on negatives. | 2012 assets with `.out` pairs; selected documented positives; clean JPEG negatives. | 8 positives + 10 negatives, one deterministic extraction recipe each. | **18** | **< 2 min** | **Auto-runnable now** | Low. | Stage 3K |
| 4 | `onion7_numeric_seed_pack_v1` | Onion 7 page-15 numbers may provide better small seed packs than arbitrary numerology. | 16 raw page-15 numbers; derived `|3301âˆ’x|` primes/order values where documented. | 48 seeds Ã— 2 directions on one existing bounded adapter. | **96** | **< 30 s** | **Auto-runnable now** | Medium; controlled by explicit registry provenance. | Stage 3M |
| 5 | `hist_cookie_base29_numeric_pack_v1` | Cookie preimages may be numeric clue values rendered in decimal/hex/base29 forms. | Historical numbers `{167,761,1033,3301,509,503,563,569,845145127,1231507051321}`. | 10 numbers Ã— 6 renders + 12 curated ordered pairs Ã— 4 separators, then Ã— 4 whitespace variants. | **432** | **< 1 s** | **Auto-runnable now** | Low. | Stage 3L |
| 6 | `trailingspace_regression_v1` | Exact whitespace has historical precedent and must not be lost by ingestors. | 2012/2014/2015 text artefacts and mirrors. | 15 artefacts, byte-exact diff plus trailing-space scan. | **15** | **< 10 s** | **Auto-runnable now** | Low. | Stage 3J |
| 7 | `prime_dimension_seed_pack_v1` | Historically documented prime dimensions may be legitimate numeric seeds. | `509,503,563,569,845145127`. | 5 seeds Ã— 2 directions Ã— 2 existing transform adapters Ã— 4 reset/advance combos. | **80** | **< 30 s** | **Auto-runnable after small implementation** | Medium-low. | Stage 3M |
| 8 | `sexagesimal_seed_pack_v1` | If the LP cuneiform reading is right, its pairwise/whole-number residues may be useful offsets. | Seed set `{17,13,55,1,1033,3301,3722101,18,24,9,7,16}`. | 12 seeds Ã— 2 directions Ã— 2 reset modes Ã— 2 advance modes. | **96** | **< 30 s** | **Needs human review** | Medium-high because source is weak. | Stage 3M |
| 9 | `dot_binary_seed_pack_v1` | Five-dot motifs justify only a tiny ambiguity-aware seed pack. | Forward/reverse values from strict 5-bit three-filled model. | 10 seeds Ã— 2 directions Ã— 2 reset modes Ã— 2 fill conventions. | **80** | **< 30 s** | **Needs human review** | High if registry confidence is ignored. | Stage 3M |
| 10 | `html_resource_capture_import_v1` | Archived onion/web captures may still contain stable forms, comments, resource names, and cookie metadata. | 12 archived HTML/site captures from archive directories. | Deterministic parser over HTML, comments, forms, scripts, resource URLs, hashes. | **12 capture jobs** | **< 1 min** | **Auto-runnable after implementation** | Low. | Stage 3N |
| 11 | `jpeg_quant_cluster_v1` | Quantisation tables and DCT-level stats may identify historically modified carrier images. | 30 historical JPEGs + 30 matched nulls. | One deterministic stat pack per file. | **60** | **< 5 min** | **Auto-runnable after implementation** | Medium. | Stage 3K |
| 12 | `spectrogram_761_repro_v1` | Spectrogram work is only useful if fixed parameters and null controls suppress pareidolia. | `761.mp3` plus 8 null variants. | 9 files Ã— 6 fixed spectrogram parameter sets. | **54** | **< 5 min** | **Auto-runnable after asset lock** | Medium-high. | Stage 3K |
| 13 | `symmetry_direction_ablation_v1` | Page-art asymmetry may correlate with direction/reset choices. | Small set of LP pages carrying tree/root/dot motifs. | 8 pages Ã— 4 direction/reset templates. | **32** | **< 1 min** | **Needs human review** | High. | Stage 3M |
| 14 | `magic_square_note_registry_v1` | Magic-square references exist in archives but should remain quarantined first. | `Magicsquare.jpg`, 5Ã—5 note file, related docs. | Registry-only extraction and provenance graph; no text search yet. | **6 artefacts** | **< 1 min** | **Run later** | Medium-high. | Stage 3J |
| 15 | `tor_allowlist_probe_v0` | A live-capture module should be tested only against a mock or explicitly approved allowlist target. | Local mock onion or controlled test target. | Single capture pipeline smoke test. | **1** | **< 2 min** | **Needs approval** | Operational rather than analytical. | Stage 3N |

The **top five immediate experiments** deserve exact manifest ideas.

**`hist_cookie_literal_pack_v1`** should declare the two cookie targets, algorithm `sha256`, UTF-8 encoding, and a source-locked literal file consisting only of signed-message phrases, historically named resources, onion addresses, exact filenames, and the small number set already mentioned. The scorer is binary exact match only. Controls are standard SHA-256 test vectors plus 100 random literals of comparable length to ensure the harness is not silently normalising input. Stop condition: zero matches or one exact match; no near-match narrative. Output: one JSONL row per tested byte string plus a tiny summary.

**`archive_image_manifest_v1`** should not be framed as a solve experiment at all. It is a corpus-facts experiment: hash, file type, dimensions, prime-dimension flag, detectable metadata, compression parameters, and OutGuess eligibility. The output should go to a persistent `historical_artefact_manifest.jsonl`, not a terminal dump. Stop condition: all files processed or any parser inconsistency that requires a fixture update. Controls: corrupted test images, duplicate files, and known PNG/JPEG type cases.

**`outguess_regression_v1`** should use the 2012 assets with `.out` pairs as positive controls and a matched negative set as false-positive guards. Success means the extracted payload hash matches the archived `.out` file hash for positives, and no payload is spuriously â€œdecodedâ€ from negatives. Stop condition: any regression mismatch. This is exactly the kind of boring test that saves months of bad folklore later. îˆ€citeîˆ‚turn16view5îˆ

**`onion7_numeric_seed_pack_v1`** should use the raw 4Ã—4 table from the Onion 7 page plus its directly documented prime/order transforms, convert those values to residues mod 29, and run them only through already-existing bounded adapters. The line between archive fact and community transform must be encoded in the manifest: raw table values are archived facts from the community-preserved image transcription, whereas prime/order/spiral meaning is community analysis. Controls: the same adapters run over equal-sized random seed sets and shuffled table values. Stop condition: if calibrated rank is indistinguishable from nulls, reject the family and move on. îˆ€citeîˆ‚turn8view0îˆ

**`hist_cookie_base29_numeric_pack_v1`** is worth running early because 2013 explicitly used a `BASE29` command in the hidden-service programming task. That does not prove the cookies are base-29 preimages, but it makes a tiny base-29 numeric render pack historically justified rather than whimsical. Controls: the same candidate templates applied to unrelated integers. Stop condition: no exact match. îˆ€citeîˆ‚turn12view3îˆ

## Recommended implementation blueprint

The clear next stage is:

**Recommended next Codex stage:** **Stage 3J â€” historical archive ingestion and visual/web observation registry.** The public repo already hints that a reviewable visual numeric observation registry is the right next deferred item; this research makes that the correct choice, not the optional one. îˆ€citeîˆ‚turn23view1îˆ

A prompt-ready engineering roadmap looks like this:

| Stage | Objective | Likely files | Tests required | Acceptance criteria |
|---|---|---|---|---|
| **Stage 3J** | Lock and hash the historical sources; add source-reliability records; create archive manifests. | `data/external/historical/â€¦`, `python/libreprimus/history/source_lock.py`, `docs/history/source-map.md`, `tests/unit/test_source_lock.py` | Deterministic hash tests, schema validation, duplicate URL handling. | Every mirrored artefact has URL, fetch date, SHA-256, provenance class, licence note, and review status. |
| **Stage 3K** | Add deterministic image/audio/web analysis CLIs and registries. | `python/libreprimus/history/image_audio.py`, `python/libreprimus/history/web_extract.py`, `schemas/*.json`, `tests/integration/test_history_extract.py` | Fixture-based Exif/identify/outguess regressions; ffprobe parsing tests; HTML parser tests. | Known fixtures reproduce expected metadata and no uncontrolled fields are omitted. |
| **Stage 3L** | Implement bounded cookie-hash experiment adapters and result-store import. | `python/libreprimus/experiments/hashpacks.py`, `experiments/manifests/historical/*.yaml`, `tests/unit/test_hashpacks.py` | Exact byte-string logging; SHA-256 vector tests; manifest determinism tests. | `hist_cookie_literal_pack_v1` and `hist_cookie_base29_numeric_pack_v1` run under policy and produce auditable JSONL/SQLite records. |
| **Stage 3M** | Bridge historical numeric observations into existing bounded text experiment adapters. | `python/libreprimus/observations/seed_bridge.py`, `experiments/manifests/historical-seeds/*.yaml` | Seed-count determinism; null-control parity; mod-29 mapping tests. | `onion7_numeric_seed_pack_v1` and `prime_dimension_seed_pack_v1` dry-run and execute within policy. |
| **Stage 3N** | Add archived HTML/resource import and a dormant Tor capture stub behind policy gates. | `tools/tor_acquisition/`, `python/libreprimus/history/tor_capture.py`, `tests/mock/test_tor_capture.py` | Local mock SOCKS/control-port tests only; no live historical fetch in CI. | The project can ingest archived web captures now and can later support live allowlist capture without redesign. |
| **Stage 5A** | Plan CUDA parity only after CPU definitions stabilise. | `docs/cuda/history-derived-workloads.md`, future `cuda/` parity fixtures | CPU/GPU parity vectors only. | No GPU code merged until archive-derived workloads have stable CPU references. |

The repository layout changes should be equally dull and explicit:

```text
data/
  external/
    historical/
      manifests/
      locks/
      mirrors/
      licences/
  observations/
    web/
    visual/
    audio/
docs/
  history/
  forensics/
  source-reliability/
experiments/
  manifests/
    historical/
    historical-seeds/
  results/
    historical/
python/
  libreprimus/
    history/
    observations/
tools/
  tor_acquisition/
```

The minimal schema set I would add immediately is:

```json
{
  "visual_numeric_observation": {
    "observation_id": "lp-symbols-cuneiform-34-v1",
    "source_id": "uncovering-symbols-page",
    "artefact_ref": "LP page 34",
    "status": "weak_hypothesis",
    "kind": "sexagesimal_cuneiform_candidate",
    "description": "Community-read cuneiform-like mark",
    "candidate_readings": [17, 13, 55, 1],
    "derived_values": {
      "pairwise_base60": [1033, 3301],
      "full_base60": 3722101,
      "mod29": [18, 24, 9]
    },
    "human_review_required": true
  }
}
```

```json
{
  "image_analysis_record": {
    "record_id": "img-2014-onion4-address-runes-jpg-v1",
    "source_id": "archive-2014-additional-images",
    "sha256": "â€¦",
    "format": "jpeg",
    "width": 0,
    "height": 0,
    "prime_dimensions": false,
    "metadata": {},
    "outguess_supported": true,
    "quant_table_fingerprint": "â€¦",
    "phash": "â€¦"
  }
}
```

```json
{
  "audio_analysis_record": {
    "record_id": "aud-2013-761mp3-v1",
    "source_id": "archive-2013-additional-files",
    "sha256": "â€¦",
    "duration_seconds": 167.0,
    "tags": {
      "title": "The Instar Emergence",
      "artist": "3301"
    },
    "spectrogram_runs": [],
    "framehash_sha256": "â€¦"
  }
}
```

The anti-false-positive protocol should be written down as hard rules:

1. **No archive-derived clue becomes a text seed until it exists as a typed observation record with provenance and confidence.**
2. **No community claim outranks a signed source.**
3. **No image/audio interpretation is accepted without matched null controls.**
4. **No cookie preimage result counts unless the exact byte string, encoding, and algorithm are logged.**
5. **No live Tor capture occurs in CI or by default.**
6. **No solve claim is permitted from image/audio/web analysis alone.**
7. **Every archive-derived text experiment must preserve the repoâ€™s current guardrails: canonical corpus inactive, page boundaries reviewable, no silent raw-data modification, no output commits.** îˆ€citeîˆ‚turn23view2îˆ‚turn6view5îˆ‚turn7view0îˆ

The GPU answer is short. **Do not recommend CUDA yet.** The repo already states that the CPU side owns corpus management, manifests, branching search, provenance, and manual review, and that GPU acceleration should wait for stable CPU references and parity tests. That is still correct. If archive-derived workloads later stabilise, the GPU worth having on an RTX 4060 Ti is for large regular batches only: hash tests over millions of strings, batch transform-and-score kernels, or large seed sweeps. It is not for Tor acquisition, HTML parsing, metadata extraction, OutGuess orchestration, or observation review. îˆ€citeîˆ‚turn23view0îˆ‚turn23view4îˆ

**Top 5 archive/image/onion tasks to implement**

| Task | Why first |
|---|---|
| Historical source-lock manifest generator | Everything else depends on stable provenance. |
| Observation registry schemas and validators | You need typed evidence before seed tests. |
| Deterministic image/audio extractor CLI | Highest-value new capability with low ambiguity. |
| Cookie-hash bounded experiment runner | Small, cheap, historically grounded. |
| Archived HTML/resource importer | Lets the project treat web/onion artefacts as data rather than lore. |

**Top 5 visual/numeric observations to encode first**

| Observation | Confidence |
|---|---|
| 2012 prime dimensions `509Ã—503` with multiplier `3301` | High |
| 2016 image dimensions `563Ã—569` and Oak-tree/OutGuess context | High |
| 2013 `761.mp3` / `167`-second duration cluster | Medium-high |
| 2013 `167`/`761` cookie names and 64-hex values | Medium |
| Onion 7 page-15 raw 4Ã—4 number table | Medium |

**Whether a Tor-backed acquisition tool is worth building now**

Yes, **as a dormant, archive-first, allowlist-only module**. No, **as a live historical onion crawler**.

**Whether third-party AI image analysis is worth using now**

No. Deterministic-first is the right move. Local AI may later assist annotation, but AI output should remain hypothesis-only.

**What not to run yet**

- Unbounded hashcat-style cookie attacks.
- Large OCR or CV-driven reading of LP page art.
- Live crawling of arbitrary onion space.
- Spectrogram parameter fishing until a â€œmeaningful lineâ€ appears.
- Magic-square, constellation, or Kabbalah seeded text campaigns before the registry exists.
- Any CUDA port of archive-derived workloads before CPU parity vectors exist.

**Sources that should be mirrored or locked next**

1. `rtkd/iddqd` for unmodified files and LP transcription/image sets. îˆ€citeîˆ‚turn21search0îˆ  
2. `scream314/cicada3301/pages_and_ciphers.md` and `gematria_primus.md` as technical reference texts. îˆ€citeîˆ‚turn22view0îˆ‚turn22view1îˆ  
3. `cicada-solvers/The-Complete-Cicada3301-Archive/2014/Liber Primus`. îˆ€citeîˆ‚turn20view4îˆ  
4. `â€¦/2014/Websites` and `â€¦/2014/additional images`. îˆ€citeîˆ‚turn20view3îˆ‚turn19view0îˆ  
5. `â€¦/2013/additional images` and `â€¦/2013/additional files`. îˆ€citeîˆ‚turn20view0îˆ‚turn20view1îˆ  
6. `â€¦/assets/2012` for stego regression positives. îˆ€citeîˆ‚turn16view5îˆ  
7. Uncovering pages for 2012, both 2013 parts, post-2014, 2015, 2016, 2017, Onion 7, symbols page, leaked email, and possible hints. îˆ€citeîˆ‚turn8view4îˆ‚turn11view0îˆ‚turn11view1îˆ‚turn5view2îˆ‚turn5view3îˆ‚turn5view4îˆ‚turn8view0îˆ‚turn35view0îˆ‚turn37view2îˆ‚turn34search0îˆ

**Questions for the user**

| Question | Why it materially matters |
|---|---|
| Are you willing to store mirrored binaries in the repo, or should the project commit only URL/hash manifests plus fetch scripts? | This affects layout, CI, and licensing strategy. |
| Do you want live Tor capture to exist at all in the near term, or should Stage 3N stop at archived HTML ingestion plus a mock capture harness? | This changes the acquisition architecture and risk model. |
| Can `761.mp3`, ISO materials, and archive screenshots be fetched locally under your project policy, or must they remain external references only? | This determines which of the top five immediate tasks can actually execute. |
| Do you want weak LP art hypotheses like cuneiform/dot patterns encoded in the first registry pass, or postponed until the stronger historical observations are done? | This changes the first seed packs and review burden. |

**Recommended next Codex stage**

Build **Stage 3J: historical archive ingestion and visual/web observation registry**.

**Top 3 bounded experiments to run next**

1. **`hist_cookie_literal_pack_v1` â€” 480 candidates.**  
   Fastest historically grounded web experiment; extremely low operational risk.

2. **`archive_image_manifest_v1` â€” 320 file-ops.**  
   Gives the project a trustworthy image fact base instead of folklore.

3. **`onion7_numeric_seed_pack_v1` â€” 96 candidates.**  
   First archive-derived bridge back into bounded text experimentation, with explicit provenance separation.

**Do not run yet**

- GPU hash-preimage attacks.
- Broad live Tor acquisition.
- LP art-driven large text campaigns.
- Open-ended spectrogram mining.
- AI-first image interpretation.

**Appendix formula crib**

| Family | Definition |
|---|---|
| Pairwise sexagesimal | `v = 60a + b` |
| Full sexagesimal | `v = Î£ d_i Â· 60^(n-i-1)` |
| Binary-dot reading | `v = Î£ b_i Â· 2^(n-i-1)` |
| Simple hash test | `digest = H(bytes(candidate))` |
| Mod-29 seed bridge | `seed = v mod 29` |
| Onion 7 prime delta | `p_i = |3301 - x_i|` where the historical derivation is documented |

That is the practical answer to â€œwhat should Codex implement next?â€: **stop pretending the remaining value is in wider blind text search, and start treating Cicadaâ€™s historical web, image, audio, and numeric artefacts as first-class, source-locked data.**
