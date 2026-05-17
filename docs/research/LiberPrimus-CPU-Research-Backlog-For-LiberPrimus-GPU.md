# Liber Primus CPU Research Backlog for LiberPrimus-GPU

> Stage 3E note: this document is a research input used to rank bounded CPU experiments. It is not a solution claim, does not activate a canonical corpus, does not finalize page boundaries, and does not authorize CUDA, broad search, generated-output commits, or solve claims.

## Executive summary

LiberPrimus-GPU already has the part that most Cicada projects never manage to build: a reproducible research spine. The public repository says the workbench now has a CPU transform registry, a solved-baseline manifest runner, JSONL and SQLite result stores, raw-data-free CI, a bounded CPU execution harness, and a standing local operator policy capped at 100,000 candidates, 600 seconds, and 250 MB of generated output. It also says Stage 3A through 3D have already been run on a reviewable unsolved slice: the 841-candidate Caesar/affine sweep and its rerank/reverse follow-up both stayed noisy; Stage 3C added positive, null, and negative calibration; Stage 3D ran a four-key Vigenère preview and the best key, `LIBER`, still calibrated as noisy. The same README is explicit that the canonical corpus is still inactive, page boundaries are still reviewable, and broad search, scoring, and CUDA campaigns have not started. citeturn42view4turn43view1turn43view4turn27view0

That means the next step should **not** be “more brute force, but bigger”. The next step should be a **ranked Stage 3E backlog** of tiny and small CPU experiments that are actually supported by evidence from solved Liber Primus pages and earlier Cicada rounds. The strongest next families are, in order: an evidence-grounded explicit-key Vigenère pack built from solved-page vocabulary and earlier Cicada key material; a p56-inspired prime-minus-one keystream sweep with bounded offsets, directions, and reset modes; and a compact reset/advance ablation pack that tests whether key or stream position should reset at line, clause, or separator boundaries. Those three families are the best fit because solved LP pages already demonstrate Atbash/reversed Gematria, Atbash-plus-shift, explicit-key Vigenère with skip behaviour, and a prime-minus-one stream; earlier Cicada rounds also repeatedly used books, phrases, primes, and multi-stage transformations rather than plain Caesar-style algebra alone. citeturn21view0turn24view5turn22view2turn22view5turn23view5turn28view7turn28view3turn29view2turn30view5turn40view0

The blunt version is this: **do not widen affine search, do not launch dictionary-scale key search, do not search arbitrary skip masks, and do not touch CUDA yet**. The repository’s own safety rules already say no generated output is a solve by itself, broad unsolved-page campaigns are not started, and future CUDA kernels must come only after CPU reference implementations, parity tests, and benchmarks exist. Starting GPU work now would mostly accelerate uncertainty. That is just a more expensive way of being wrong. citeturn42view4turn43view4

The evidence picture separates cleanly into five buckets.

| Bucket | Assessment |
|---|---|
| **Known facts** | Solved LP sections use direct translation, reversed Gematria/Atbash, Atbash followed by a shift of 3, explicit-key Vigenère with declared keys and published skip indices, and p56’s ordered `prime - 1` stream modulo 29. The current workbench reproduces 10 known solved baselines and has already shown that simple Caesar/affine and a four-key motif Vigenère preview on the current reviewable slice are noisy. citeturn21view0turn24view5turn22view2turn22view5turn23view5turn27view0turn43view4 |
| **Community claims worth testing** | Public community sources argue that cross-page continuation matters, that p56 may justify nearby prime-stream variants, and that earlier Cicada phrases such as *Parable*, *instar*, *divinity*, and *Patience is a virtue* may recur as keys or scoring motifs. These are reasonable as bounded experiments, not as proof. citeturn41view0turn23view5turn30view5turn29view4 |
| **Plausible hypotheses** | The unsolved corpus may use explicit keys from earlier rounds, prime-derived streams near the p56 pattern, separator-sensitive resets, or tiny route/order changes such as line reversal or boustrophedon reading. Earlier Cicada rounds used book codes, primes, XOR/bit inversion, magic squares, and multi-stage pipelines, so composition is historically normal. citeturn28view7turn28view3turn29view1turn29view4turn29view0turn40view0 |
| **Weak hypotheses** | Fibonacci/Lucas/Möbius/Legendre streams, arbitrary grid/spiral routes, and large external-book dependencies are not impossible, but direct evidence for them in unsolved LP pages is weak. A Reddit-style Fibonacci theory for 2016/2017 exists, but it is not a strong foundation for immediate search priority. citeturn39search4turn29view0turn29view2 |
| **Dead ends for now** | Re-running broad affine/Caesar on the same slice, broadening from four Vigenère keys to huge dictionaries, searching unconstrained F-skip masks, or building CUDA kernels before CPU parity. Those are exactly the traps the current evidence says to avoid. citeturn27view0turn42view4turn43view4 |

The single clearest recommendation after Stage 3D is therefore:

**Stage 3E should ingest a method backlog and queue the next three bounded CPU experiments:**
1. a solved-and-history evidence Vigenère key pack;
2. a p56-local prime-minus-one offset sweep;
3. a separator/reset ablation pack over the best-supported keys and streams. citeturn43view4turn22view2turn23view5turn40view0

## Source map

The source problem here is not a lack of material. It is an overabundance of mirrors, partial transcriptions, and community summaries with different counting conventions. The safest approach is to use a **tiered source model**.

### Primary and strongest community-technical sources

| Source | What it gives you | Assessment | Action |
|---|---|---|---|
| `scream314/cicada3301` | A long-running archive that includes `2012.md`, `2013.md`, `2014.md`, `2015.md`, `2016.md`, `2017.md`, `gematria_primus.md`, `pages_and_ciphers.md`, and a full `liber_primus.md`. The repo describes itself as a collection of raw assets, and its README points to the full Liber Primus plus year-by-year materials. citeturn19search10turn13search8 | **Strong archival reference** for puzzle history, solved-page groupings, and raw LP image/file naming. Not the original publisher, but one of the core community archives. | Mirror specific commit SHAs and raw file hashes for every file the workbench cites. |
| `rtkd/iddqd` | “Unmodified files, transcription and other assets”, including `liber-primus__images--full`, `liber-primus__images--unsolved`, `liber-primus__index`, `liber-primus__keys`, `liber-primus__transcription--master`, and `liber-primus__translation`. citeturn11search0 | **Best transcript/image baseline** available publicly. Still community-maintained, so it is not magically canonical, but it is the most practical anchor for reproducible corpus work. | Treat as the default corpus candidate source and lock tree hashes. |
| Public PGP-signed message archives | The archive material consistently points back to Cicada’s PGP key `7A35090F`; scream314’s 2016 page shows a good signature for the 2016 image payload, and the 2017 signed warning explicitly says “Beware false paths. Always verify PGP signature from 7A35090F.” citeturn40view0turn38view0turn14search2 | **Authenticity anchor**. Anything not tied back to this key is second-class at best. | Mirror signed message files and a verified copy of the public key first. |

### Strong secondary sources

| Source | What it gives you | Assessment | Action |
|---|---|---|---|
| Uncovering Cicada wiki | The wiki pages on solved-page methods, unsolved pages, transliteration, frequency analysis, and later messages are the best indexed community explanations. The solved-method page explicitly states it is using rtkd’s transcription. The unsolved-page transliteration page preserves line count and warns that words can continue across page boundaries. citeturn33search4turn41view0turn41view1 | **Very useful, but community-edited**. Good for method summaries, page notes, and image annotations. Not a canonical authority. | Mirror specific pages as frozen HTML/PDF snapshots, with retrieval date and URL. |
| `krisyotam/cicada3301` | A newer “definitive research archive” mirror that bundles puzzles, Liber Primus pages, enhanced images, community tools, signed messages, and timeline material. It claims 75 original page images, enhanced versions, and 22 signed messages. citeturn37view0 | **Convenience mirror, not authority**. Good for bulk preservation and source discovery, but claims should be checked against older archives. | Mirror selectively; use as a backup and index, not as source of truth. |

### Reference-only technical tools

| Source | Useful for | Why it is not authoritative |
|---|---|---|
| `rtkd/idkfa` | Crib finding, invert/reverse switches, mathematical key generators including `prime()` and `fib()`, and reset-by-chunk ideas such as line/page/segment. citeturn34view1 | It is a solver toolkit, not a transcript authority. Use it to inspire interfaces, not facts. |
| `relikd/LiberPrayground` | Frequency analysis, interrupt detection, Vigenère/Affine breaker ideas, rune-object modelling, and explicit punctuation notation. citeturn34view3 | It uses its own copied pages and utility layer. Good reference, not a locked corpus source. |
| `r4nd0mD3v3l0p3r/LiberPrimusSolver` | Manifest-like task pipelines, `splitBy` semantics, support for direct/Atbash/shift/Vigenère/Hill tasks, and the practical idea that chunk/reset policy should be configurable. citeturn35view0 | It is explicitly “an attempt” and uses its own task model. Useful as architectural inspiration only. |
| `lipeeeee/gematria` | Gematria sum/hash workflows and examples tying 761 and related phrases to earlier rounds. citeturn34view0 | Useful for GP-sum computations, not for corpus truth. |

### Historical convenience sources that should be treated carefully

Pastebins, gists, Dropbox links, spreadsheets, forum posts, and Reddit threads are useful mostly because they disappear. The Cicada-solvers gist explicitly lists the old Pastebin with “58 pages in runes, and rune prime values”, plus a Google sheet and Dropbox bundle. Those are useful things to mirror, but they should be treated as unstable transport rather than authoritative evidence. citeturn36search2turn36search0

### Rejected or low-trust material

Unsourced “decoded” posts and crib guesses are not evidence. The archived Reddit “page 43” speculation thread is a perfect example: it proposes a candidate word because it “fits pretty much everything”, but provides no reproducible transform, no locked transcript, and no control structure. Likewise, a Reddit Fibonacci theory about 2016/2017 sums might be interesting as a curiosity, but it is nowhere near strong enough to drive immediate search priority. These are useful only as negative controls or examples of crypto pareidolia. citeturn33search5turn39search4

### Disagreements that matter to experiment design

The first disagreement is **counting convention**. The Uncovering wiki prominently says there are “17 already solved pages”, while repositories like `pages_and_ciphers.md` group solved material by **ranges**, **split pages**, and even hidden/extra image names such as `107.jpg`, `167.jpg`, `229.jpg`, and `73.jpg - 56.jpg`. That means “how many solved pages exist?” is partly a bookkeeping question, not a cryptanalytic one. The workbench should therefore store at least: `semantic_section_id`, `published_page_id`, `archive_image_id`, `split_part`, and `source_range_label`. citeturn41view1turn15view2turn31view4

The second disagreement is **boundary handling**. The transliteration page warns explicitly that words can continue across pages, with a concrete example at the transition from `0.jpg` to `1.jpg`. The project is therefore right to keep page boundaries reviewable and the canonical corpus inactive for now. Any early experiment should either reuse the exact Stage 3A reviewable selector or make boundary assumptions explicit in the manifest. citeturn41view0turn42view4

The third disagreement is **transcription notation**. rtkd’s master transcription states `Word : -` and `Clause : .`, while the solved/unsolved community transcriptions also preserve `/`, `&`, and `%` tokens in context. That is enough to justify the repo’s separator grammar work: these characters cannot be hand-waved away as formatting junk. They are corpus features. citeturn9view0turn21view0turn23view5

## Historical carryover from earlier Cicada puzzles

Earlier Cicada rounds matter because Liber Primus did not appear in a vacuum. The recurring pattern across 2012–2017 is not “one cipher repeated forever”; it is **multi-stage puzzle construction with careful authenticity signalling, repeated use of external texts, prime-number motifs, steganographic packaging, and later numeric reinterpretation of already-seen phrases**. That is exactly why the next LP experiments should be **small, modular, and evidence-ranked** rather than monolithic. citeturn14search9turn28view7turn28view3turn29view1turn29view0turn40view0turn38view0

### What earlier rounds clearly established

| Round | Known mechanism | Evidence level | What it suggests for LP |
|---|---|---|---|
| 2012 | OutGuess steganography in images, a book code leading through *The Mabinogion*, coordinates that led to physical QR posters, later another book code using *Agrippa*, and strict PGP signing. citeturn14search9turn28view7turn28view8 | High | Cicada likes multi-stage packaging, authentic signed breadcrumbs, and external texts as structured keys. |
| 2013 | A riddle-led book code using *Liber AL vel Legis*; a bootable ISO that printed prime numbers up to 3301; the audio file `761.mp3` whose hexdump contained the *Parable* text; a `count` command tying phrases to Gematria sums such as `761`; and an engineering challenge requiring a Tor hidden service. citeturn28view1turn28view3turn30view5turn30view0 | High | Primes, Gematria sums, and specific phrases such as *instar*, *circumferences*, *divinity*, and *emerge* are not random community inventions; they were used by Cicada before LP page 57. |
| 2014 | A book cipher pointing to Emerson’s *Self-Reliance*; OAEP/RSA encryption; a growing hex string on an onion page tied to the comment “Patience is a virtue”; the observation that its Gematria sum is 761; bit-flip/XOR style extraction that exposed embedded JPEGs; magic-square submission; and later additional LP image files such as `107.jpg`, `167.jpg`, and `229.jpg`. citeturn29view2turn29view1turn29view4turn29view0turn35view0 | High | Multi-stage composition, numeric reinterpretation of phrases, magic-square themes, and hidden LP pages are all part of the ecosystem. |
| 2016 | The signed message says: “Liber Primus is the way. Its words are the map, their meaning is the road, and their numbers are the direction.” It also repeats the warning to verify the PGP key. citeturn40view0 | High | The text itself, its interpreted meaning, and its numbers are all fair game. Number-aware transforms are therefore not a community fantasy. |
| 2017 | The final signed warning: “Beware false paths. Always verify PGP signature from 7A35090F.” citeturn38view0 | High | Method claims without provenance and reproducibility are exactly the thing the project should reject. |

### What is most relevant to bounded CPU experiments

The strongest historical carryovers are **explicit phrases that might become keys**, **number-theoretic motifs**, and **multi-stage but still classical transform chains**. The 2013/2014 material puts *Parable*, *instar*, *divinity*, *emerge*, and `761` on very firm footing. The 2012–2014 book-cipher history also makes a bounded external-text key pack reasonable: *Mabinogion*, *Agrippa*, *Liber AL vel Legis*, *Book of the Law*, and *Self-Reliance* are all historically attested, even if using them as LP keys is still only a hypothesis. citeturn30view5turn29view4turn28view7turn28view3turn29view2

What is **not** immediately relevant to the current workbench is the steganographic packaging layer itself. OutGuess, audio hiding, OAEP/RSA, and hidden-service tasks are historically real, but LiberPrimus-GPU is presently a bounded CPU text-search workbench with canonical corpus still inactive. The practical implication is to **record image/audio anomalies as metadata**, not to derail Stage 3E into image forensics. The pages with anti-aliased apostrophes or quotation marks should be tagged in corpus metadata for later image-aware work, but they should not be the next CPU search campaign. citeturn41view1turn29view0turn29view1

### Historical clues that justify small key packs

Three historical facts justify immediate bounded key experimentation instead of broad dictionary search.

First, Cicada repeatedly reused meaningful phrases rather than arbitrary random strings. *Patience is a virtue* appears in the 2012 message chain and again in 2014 onion material; its GP sum to 761 is repeatedly noted by community technical archives. Second, *Parable* and its body text appear in 2013 before becoming LP page 57. Third, earlier rounds repeatedly used named books as codebooks. Those patterns do **not** prove that unsolved LP pages use those strings as Vigenère keys, but they make such tests evidence-grounded and cheap. citeturn36search4turn29view4turn30view5turn28view7turn28view3turn29view2

## Liber Primus solved-method review

Liber Primus is described in the major archives as a two-part publication: LP1 is 17 pages long and LP2 is 58 pages long, for 75 pages total. Community inventories usually display LP2 pages `0.jpg` through `57.jpg` and note that pages `0.jpg` through `55.jpg` remain unsolved, while page 56 (*An End*) and page 57 (*Parable*) are solved. At the same time, LP1 solves are often grouped by semantic section or archive-specific file ranges instead of a flat page count, which is why solved-page totals vary depending on whether title pages, split pages, and hidden images are counted separately. citeturn13search8turn41view1turn15view2turn31view4

The solved-method page gives the community-standard modulo-29 mapping: 29 rune values from decimal 0 to 28, with associated prime values from 2 to 109. It also states that solved Vigenère-style pages are decrypted by subtracting key values modulo 29, and that some solved methods skip plaintext `F` positions, which do not advance the key or prime schedule. That is not a cosmetic quirk. It is a search-space bomb. A naive skip-mask search over long candidate slices explodes combinatorially, so the workbench should only test capped or heuristic skip policies unless a stronger clue justifies more. citeturn20view4turn33search4

### Solved inventory and what it actually tells us

| Solved item | Image/range convention | Method used | Formula or rule | Why it matters | Repo baseline status |
|---|---|---|---|---|---|
| **Liber Primus** title | `00.jpg` | Direct translation | Identity on rune values | Confirms cleartext pages exist. citeturn17view0 | Public README does not list individual fixture names; likely folded into direct-translation baselines as applicable. citeturn27view0 |
| **A Warning** | `01.jpg` | Atbash / reversed Gematria | `p_i = 28 - c_i` | Establishes reverse-Gematria/Atbash as a real LP method. citeturn21view0turn18view5 | Covered by Atbash-family bucket. citeturn27view0 |
| **Intus** | `02.jpg` | Direct translation | Identity | Confirms cleartext headings/titles. citeturn32view0 | Likely direct-translation bucket. citeturn27view0 |
| **Welcome** | `03.jpg–04.jpg` | Explicit-key Vigenère | Standard subtractive Vigenère over mod 29; key `DIVINITY`; skip indices published for plaintext `F`s. citeturn22view2turn33search4 | Strong evidence for explicit keys and skip-sensitive schedules. | Explicit-key Vigenère bucket. citeturn27view1 |
| **Some Wisdom** | `05.jpg` | Direct translation | Identity | Introduces primes, totient, encryption, and the number-word grid. citeturn21view2turn18view4 | Likely direct-translation bucket. citeturn27view0 |
| **Koan 1** | LP1 image set beginning `06.jpg` | Atbash then shift 3 | `p_i = (28 - c_i + 3) mod 29` | Shows the project must support two-stage transforms, not just single operators. citeturn24view5turn25view1 | Covered by Atbash-family bucket. citeturn27view0 |
| **The Loss of Divinity** | `10.jpg–13.jpg` | Direct translation | Identity | Reinforces the text’s vocabulary and orthography. citeturn18view3turn31view2 | Likely direct-translation bucket. citeturn27view0 |
| **Koan 2** | `14.jpg–15.jpg` and archive-linked hidden pages | Explicit-key Vigenère | Standard subtractive Vigenère; key `FIRFUMFERENFE`; skip indices published. citeturn20view1turn22view5 | Confirms a second explicit key and a second skip-driven solved method. | Explicit-key Vigenère bucket. citeturn27view2 |
| **An Instruction** | `16.jpg` plus archive-linked continuation | Direct translation | Identity | Adds another cleartext section and a 5×5 number grid. citeturn24view3turn25view3 | Likely direct-translation bucket. citeturn27view0 |
| **An End** | `56.jpg` | Ordered prime-minus-one stream | `p_i = (c_i - (prime_i - 1)) mod 29`; equivalently `phi(prime_i)` for primes. citeturn23view5turn23view0 | This is the single strongest piece of evidence for bounded prime-stream experimentation. | Implemented as p56 prime-minus-one / phi-prime baseline. citeturn27view1 |
| **Parable** | `57.jpg` | Direct translation | Identity | The same *Parable* text appears in 2013 material, which makes those phrases historically grounded motifs. citeturn17view6turn30view5 | Likely direct-translation bucket. citeturn27view0 |

### Why p56 matters more than almost any other clue

The p56 solve is unusual because it is not merely “number-themed”. It is mechanically specified: subtract the ordered prime numbers minus one, modulo 29. The same community write-up explicitly notes that `φ(p) = p - 1` for primes, which is why the repo records `phi_prime_stream` as an equivalent alias for prime inputs. That turns vague numerology into a concrete transform family. It does **not** prove that every unsolved page uses primes, but it does justify a **local neighbourhood search** around this exact mechanism: offsets, direction, resets, and nearby prime-derived streams such as raw `prime mod 29` or `prime-gap mod 29`. It does **not** justify a wild zoo of arbitrary integer sequences on day one. citeturn23view5turn23view0turn27view1

### What the current repo already covers, and what it does not

The public README says the workbench currently has 10 passing solved baselines: four direct-translation fixtures, three Atbash-family fixtures, two explicit-key Vigenère fixtures, and one p56 prime-minus-one fixture. It also says these are regression baselines and not solve claims, that the p56 hex block is preserved as a payload check, and that selected source locks already exist for `scream314/cicada3301` and `lipeeeee/gematria`. citeturn27view0turn27view1turn42view2

The gap is therefore not “can the repo reproduce known solves?” It can. The gap is **what bounded unsolved experiments to prioritise next** without collapsing into false positives. That is exactly where the backlog below is aimed.

## Method family analysis

The right way to prioritise method families here is by asking three questions at once: **is there historical or solved-page evidence for the family; can it be bounded under the current CPU policy; and does it have a plausible failure analysis rather than just producing noise faster?** The table below is the shortlist that survives those tests.

### Evidence-ranked families

| Method family | Evidence basis | Search size under a sensible bounded design | Fits current policy | Risk level | Recommendation |
|---|---|---:|---|---|---|
| **Explicit-key Vigenère packs** | Two solved LP sections use explicit keys (`DIVINITY`, `FIRFUMFERENFE`), and earlier puzzle rounds repeatedly used meaningful books and phrases. citeturn22view2turn22view5turn28view7turn28view3turn29view2turn30view5 | Tiny to small | Yes | Moderate false-positive risk if scoring is weak | **Highest priority**. |
| **Prime-minus-one local sweeps** | p56 is solved exactly this way; LP text also foregrounds primes and totients. citeturn23view5turn23view0turn18view4 | Tiny | Yes | Lower than broad sequence search | **Highest priority**. |
| **Prime-mod and prime-gap local sweeps** | Nearby to p56’s known method; historically consistent with prime obsession, but not directly solved elsewhere. citeturn23view5turn18view4turn30view5 | Tiny | Yes | Moderate | **High priority after prime-minus-one**. |
| **Reset/advance ablations** | Solved Vigenère pages depend on published skip indices; current corpus still has reviewable boundaries. citeturn33search4turn41view0turn42view4 | Tiny | Yes | Low | **High priority** because it tests semantics, not just keys. |
| **Capped F-skip search** | F-skip behaviour is real on solved pages, but unrestricted mask search blows up. citeturn33search4turn22view5 | Small if capped; large if free | Yes only with hard cap | High if not capped | **Priority only with explicit cap and stop rule**. |
| **Tiny line/order transpositions** | Earlier Cicada rounds used multi-stage transforms; LP pages preserve line structure and punctuation. citeturn29view0turn41view0 | Tiny to small | Yes | Moderate | **Try only after the first key/stream packs**. |
| **Cross-page continuation tests** | The transliteration page explicitly warns that words continue across page boundaries. citeturn41view0 | Tiny if limited to documented pairs | Yes | Moderate because boundaries are reviewable | **Do on documented continuations only**. |
| **Fibonacci / triangular / square streams** | Number-theoretic culture is strong, but direct LP evidence is weak beyond primes/totient. citeturn30view5turn39search4 | Small | Yes | High overfitting risk | **Later, after stronger families**. |
| **Magic-square / arbitrary route ciphers** | Magic squares were used in 2014, but not yet tied directly to unsolved LP page ordering. citeturn29view0 | Large quickly | Not sensibly | Very high | **Do not run yet**. |
| **Broad dictionary or beam search** | No strong evidence; current slice scoring is still fragile. citeturn27view0turn42view4 | Large | No | Very high | **Do not run yet**. |

### Exact transform assumptions worth keeping

For this project, the useful mod-29 families are small and explicit:

- **Atbash / reverse Gematria:** `p_i = 28 - c_i`. This is an established solved LP method. citeturn21view0
- **Atbash plus shift:** `p_i = (28 - c_i + 3) mod 29`. Also established. citeturn24view5
- **Explicit-key Vigenère:** `p_i = (c_i - k_{f(i)}) mod 29`, where `f(i)` depends on reset and advancement policy. This formula is a standard inference from the solved-method description, which explicitly says the Vigenère pages are reversed by subtracting key values modulo 29. citeturn33search4
- **p56 prime-minus-one:** `p_i = (c_i - ((prime_i - 1) mod 29)) mod 29`. Established. citeturn23view5
- **Prime-mod local variant:** `p_i = (c_i - (prime_i mod 29)) mod 29`. This is an inference worth testing because it is the nearest simpler relative of the solved p56 stream.
- **Prime-gap local variant:** `p_i = (c_i - ((prime_{i+1} - prime_i) mod 29)) mod 29`. This is only a hypothesis, but it stays close to the same number-theoretic family.

Everything beyond that should be treated as an explicit downgrade in evidence level.

### Weak hypotheses and dead ends

Some hypotheses are tempting precisely because they are mathematically fancy. That is not the same thing as being historically supported.

A **weak hypothesis** is any sequence family that currently depends more on cleverness than on evidence: Fibonacci/Lucas/Möbius/Legendre symbols, large OEIS digressions, or page-number algebra without a clue that actually points there. The Reddit Fibonacci discussion is a warning sign here: even if a pattern exists in one message set, it does not deserve automatic promotion into LP search priority. citeturn39search4

A **dead end for now** is anything that is either already tested and noisy, or structurally too unconstrained to teach you much if it fails. That includes repeating broad affine searches on the same slice, huge key dictionaries, unconstrained F-skip mask searches, arbitrary route ciphers, and premature CUDA work. The current repo state already says broad search/scoring/CUDA campaigns are not started and that the small Stage 3A–3D runs did not justify widening. citeturn43view4turn27view0

## Prioritised bounded experiment backlog

All candidate counts below assume **the exact same reviewable Stage 3A/3B/3D slice selector** unless noted otherwise. That is deliberate: until the canonical corpus activates, changing both the method family and the corpus slice at the same time is a good way to learn nothing.

Estimated runtimes below are **engineering inferences**, not published benchmarks. They assume the present CPU-only harness on an i9-9900K, the current Stage 3C-style scorer, ignored output files, and top-k result retention rather than dumping every candidate. The dry-run planner should verify actual counts before execution. The project’s standing policy already allows automatic local CPU runs only when the item stays within 100,000 candidates, 600 seconds, and 250 MB. citeturn43view1turn43view2turn43view3

### Backlog table

| Experiment ID | Short name | Hypothesis | Exact parameters | Candidate count estimate | Runtime estimate | Policy status | Required controls | Run? |
|---|---|---|---|---:|---|---|---|---|
| `stage3e_vig_lp_evidence_pack_v1` | LP evidence key pack | Unsolved slice may use explicit keys drawn from solved LP vocabulary. | Keys=`[DIVINITY,FIRFUMFERENFE,PARABLE,INSTAR,EMERGE,WITHIN,WELCOME,PILGRIM,TOTIENT,PRIMES,SACRED,ENCRYPTED]`; reset=`[none,line]`; advance=`[runes_only,token_break_preserving]` | **48** | ~5–20 s | Auto-runnable now if key-pack Vigenère exists | Solved Vigenère positives; Stage 3C nulls; shuffled same-slice negatives | **Run now** |
| `stage3e_prime_minus_one_offsets_v1` | p56 local prime sweep | Unsigned pages may use the same family as p56 with a different offset, direction, or reset mode. | stream=`prime_minus_one`; offset=`0..63`; direction=`[forward,reverse]`; reset=`[none,line]` | **256** | ~10–30 s | Auto-runnable now if stream sweep exists | p56 positive; Stage 3C nulls; shuffled-rune negatives | **Run now** |
| `stage3e_vig_history_key_pack_v1` | Historical motif key pack | Earlier Cicada book and phrase material may reappear as compact keys. | Keys=`[PATIENCEISAVIRTUE,THEINSTAREMERGENCE,SELFRELIANCE,BOOKOFTHELAW,MABINOGION,AGRIPPA,EMERSON,CROWLEY,BLAKE,PATIENCE,VIRTUE,SELF,RELIANCE,LAW]`; reset=`[none,line]`; advance=`[runes_only,token_break_preserving]` | **56** | ~5–20 s | Auto-runnable now if key-pack Vigenère exists | Stage 1C solved positives; nulls; same-length random-text negatives | **Run now** |
| `stage3e_reset_advance_ablation_v1` | Reset/advance ablation | Current noisy results may be mostly boundary semantics, not wrong keys. | Base transforms=`[DIVINITY,FIRFUMFERENFE,PATIENCEISAVIRTUE,THEINSTAREMERGENCE,prime_minus_one@0,prime_minus_one@1,prime_mod29@0,prime_gap@0]`; reset=`[none,word,clause,line]`; advance=`[runes_only,token_break_preserving]` | **64** | ~10–30 s | Auto-runnable now if reset hooks exist | Same transforms over shuffled negatives; solved-page regression spot-checks | **Run now** |
| `stage3e_prime_mod_gap_pack_v1` | Prime neighbour streams | Nearby prime-derived streams may outperform p56’s exact form on different pages. | family=`[prime_mod29,prime_gap_mod29]`; offset=`0..31`; direction=`[forward,reverse]`; reset=`[none,line]` | **256** | ~10–30 s | Auto-runnable now if family registry exists | Nulls and p56 negative control check | **Run now** |
| `stage3f_f_skip_capped_v1` | Capped F-skip search | Some promising keys may fail only because of a small number of skipped plaintext `F`s. | Key set=`[DIVINITY,FIRFUMFERENFE,PATIENCEISAVIRTUE,THEINSTAREMERGENCE]`; candidate F positions capped to first 12; allow skip-mask Hamming weight `0..2`; reset=`[none,line]` | **632** upper bound | ~20–60 s | Needs implementation first, still policy-safe | Reproduce known skip-aware solved pages; compare against non-skip version; stop if slice has >12 F candidates | **Run later** |
| `stage3f_titles_pack_v1` | Section-title keys | LP titles may be reused as short keys or key seeds. | Keys=`[AWARNING,WELCOME,SOMEWISDOM,KOAN,ANINSTRUCTION,ANEND,PARABLE,INTUS]`; reset=`[none,line]`; advance=`[runes_only,token_break_preserving]` | **32** | ~5–15 s | Needs implementation first | Nulls; solved positive spot-checks | **Run later** |
| `stage3f_line_order_pack_v1` | Tiny order variants | A small route change may be required before a supported key/stream works. | Pretransform=`[identity,reverse_each_line,reverse_line_order,boustrophedon_lines]`; base transforms=`[top 4 key pack items + top 4 prime items]` | **32** | ~10–30 s | Needs implementation first | Order-shuffled negatives; solved-page sanity checks on cleartext pages | **Run later** |
| `stage3f_page01_continuation_v1` | Documented continuation pair | The `0.jpg→1.jpg` continuation note may affect early LP2 search results. | Selector variants=`[0-alone,0+1-with-boundary-token,0+1-concatenated-no-boundary-token]`; transforms=`[top 8 from first five experiments]` | **24** | ~10–30 s | Needs implementation first; still bounded | Compare all three selectors against same nulls | **Run later** |
| `stage3g_simple_sequence_pack_v1` | Other small integer sequences | Nearby non-prime numeric motifs may be worth a cheap falsification pass. | family=`[fibonacci_mod29,triangular_mod29,square_mod29]`; offset=`0..31`; direction=`[forward,reverse]`; reset=`[none,line]` | **384** | ~15–45 s | Needs implementation first | Strong nulls and family-wise multiple-testing correction | **Run later** |
| `stage3g_prime_position_mix_v1` | Prime-plus-position overlay | 2016’s “numbers are the direction” may point to index-mixed prime streams. | family=`[(prime_minus_one + i) mod29,(prime_minus_one - i) mod29]`; offset=`0..15`; direction=`[forward,reverse]`; reset=`[none,line]` | **128** | ~10–30 s | Needs implementation first | Nulls; compare against plain prime-minus-one | **Run later** |
| `stage3g_atbash_then_prime_v1` | Two-stage reverse-plus-stream | Some unsolved pages may combine a reverse family with a number stream. | pretransform=`[identity,atbash,atbash_plus_3]`; stream=`prime_minus_one`; offset=`0..7`; reset=`[none,line]` | **48** | ~10–30 s | Needs implementation first | Known solved Atbash/Atbash+3 fixtures; nulls | **Run later** |
| `stage3g_separator_reset_grid_v1` | Separator-sensitive semantics | `/`, `&`, and `%` may act as reset or block markers. | Selected transforms=`[top 6 from 3E]`; reset policy=`[word,clause,line,separator_block]` | **24** | ~10–20 s | Needs implementation first | Negative controls where separators are randomised | **Run later** |
| `stage3g_score_cluster_rerank_v1` | Result clustering and rerank | Noise may look strong only because variants collapse onto the same pseudo-plaintext family. | Import top 500 from experiments 3E–3F; cluster by normalised plaintext, transform-chain similarity, and score vector; rerank by cluster robustness | **500 rescored items** | ~5–20 s | Needs implementation first | Must preserve original rankings and emit cluster audit files | **Run later** |
| `stage3g_negative_control_extension_v1` | Family-specific negatives | Every new family needs fresh negatives or the scorer will flatter nonsense. | Negative corpora=`[same-length shuffle, rune-frequency-preserving shuffle, wrong-mapping transform, separator-randomised slice]`; representative transform subset size=`25` | **100** | ~5–15 s | Auto-runnable now if control harness exists | Positive solved controls + nulls + negatives | **Run now** |

### Why this order

The order is evidence-first, not novelty-first. The first five items either come directly from solved LP methods or from very close neighbouring hypotheses. They are also tiny enough that, if the implementation hooks already exist, they fit easily inside the standing CPU operator policy. By contrast, the later items either need new transform hooks, depend on more fragile modelling assumptions, or are deliberately secondary falsification passes. citeturn43view1turn43view2turn43view3turn22view2turn23view5

### Top five immediate experiments

#### Stage 3E Vigenère evidence key pack

**Manifest idea**

```yaml
experiment_id: stage3e_vig_lp_evidence_pack_v1
selector: reuse_exact_stage3a_reviewable_slice
family: vigenere_explicit_key
keys:
  - DIVINITY
  - FIRFUMFERENFE
  - PARABLE
  - INSTAR
  - EMERGE
  - WITHIN
  - WELCOME
  - PILGRIM
  - TOTIENT
  - PRIMES
  - SACRED
  - ENCRYPTED
reset_modes: [none, line]
advance_modes: [runes_only, token_break_preserving]
candidate_count: 48
score_profile: stage3c_composite
top_k: 50
```

This is the best first run because every key in the list is grounded either in solved LP plaintext or in LP’s explicit number-theory vocabulary. The final two keys, `SACRED` and `ENCRYPTED`, come straight from *Some Wisdom*, which is direct LP plaintext about primes and totients. `DIVINITY` and `FIRFUMFERENFE` are already known solved keys, and *Parable* / *instar* / *within* / *emerge* are historically reinforced by the 2013 audio material. citeturn22view2turn22view5turn21view2turn30view5

Use the existing Stage 3C composite scorer, but add one **mandatory audit output**: a sidecar JSONL that records per-candidate separator statistics and whether high scores are coming from lexical hits, low-entropy collapse, or actual multi-feature agreement. Stop immediately if the top candidates land inside the existing noisy band defined by Stage 3C’s null and negative controls. citeturn27view0turn43view4

#### Stage 3E p56 local prime-minus-one offset sweep

**Manifest idea**

```yaml
experiment_id: stage3e_prime_minus_one_offsets_v1
selector: reuse_exact_stage3a_reviewable_slice
family: prime_minus_one_stream
offsets: [0, 1, 2, ..., 63]
directions: [forward, reverse]
reset_modes: [none, line]
candidate_count: 256
score_profile: stage3c_composite
top_k: 50
```

This is the strongest non-Vigenère next step because it stays as close as possible to the one unsolved-LP-adjacent page whose solving method is mechanically known. The point is not “primes everywhere”; the point is “test the immediate neighbourhood of the only proven prime keystream first, on a bounded slice”. citeturn23view5turn23view0turn27view1

Controls must include: the p56 positive control; the same slice with rune-order shuffle; and at least one wrong-family negative such as a simple Caesar or affine baseline imported from the existing noisy Stage 3A/3B output. If the score distribution overlaps heavily with the nulls, stop and do not widen offsets. citeturn27view0turn43view4

#### Stage 3E historical motif key pack

**Manifest idea**

```yaml
experiment_id: stage3e_vig_history_key_pack_v1
selector: reuse_exact_stage3a_reviewable_slice
family: vigenere_explicit_key
keys:
  - PATIENCEISAVIRTUE
  - THEINSTAREMERGENCE
  - SELFRELIANCE
  - BOOKOFTHELAW
  - MABINOGION
  - AGRIPPA
  - EMERSON
  - CROWLEY
  - BLAKE
  - PATIENCE
  - VIRTUE
  - SELF
  - RELIANCE
  - LAW
reset_modes: [none, line]
advance_modes: [runes_only, token_break_preserving]
candidate_count: 56
score_profile: stage3c_composite
top_k: 50
```

This is a historically justified extension of Stage 3D’s tiny four-key preview. The earlier puzzle chain repeatedly used meaningful books and phrases rather than anonymous random keys, and *Patience is a virtue* plus *The Instar Emergence* are especially strong because they are tied directly to Gematria/761 material. citeturn29view4turn30view5turn28view7turn28view3turn29view2

The false-positive risk is higher than in the LP evidence pack, because some keys here are historically real but not directly LP-local. That means the manual-review threshold must be stricter: no candidate should be considered interesting unless it beats nulls on at least two independent score components and produces multi-line structure rather than a few reassuring words sprinkled over rubbish.

#### Stage 3E reset and advance ablation grid

**Manifest idea**

```yaml
experiment_id: stage3e_reset_advance_ablation_v1
selector: reuse_exact_stage3a_reviewable_slice
base_transforms:
  - vigenere:DIVINITY
  - vigenere:FIRFUMFERENFE
  - vigenere:PATIENCEISAVIRTUE
  - vigenere:THEINSTAREMERGENCE
  - prime_minus_one:offset=0
  - prime_minus_one:offset=1
  - prime_mod29:offset=0
  - prime_gap_mod29:offset=0
reset_modes: [none, word, clause, line]
advance_modes: [runes_only, token_break_preserving]
candidate_count: 64
score_profile: stage3c_composite
top_k: 50
```

This is cheap and disproportionately valuable. The solved pages prove that boundary semantics matter: key advancement can skip over plaintext `F`s, and the public transcriptions preserve several separator classes. If Stage 3A–3D were noisy because the family was right but the state machine was wrong, this experiment catches that without widening the key space. citeturn33search4turn41view0

The control that matters here is **semantic ablation**: rerun the same transforms with separators stripped or randomised. If separator-aware candidates do not meaningfully outperform separator-randomised negatives, abandon the family variation and move on.

#### Stage 3E family-specific negative-control extension

**Manifest idea**

```yaml
experiment_id: stage3e_negative_control_extension_v1
selector: reuse_exact_stage3a_reviewable_slice
negative_corpora:
  - rune_shuffle_same_length
  - rune_freq_preserving_shuffle
  - wrong_mapping_variant
  - separator_randomised_variant
transform_subset_size: 25
candidate_count: 100
score_profile: stage3c_composite
emit_full_score_vectors: true
```

This is not glamorous, which is exactly why it should happen. Stage 3C already added nulls and negatives, but the next families are not affine families. Each new search family needs its own false-positive calibration. Otherwise you are just letting a scorer flatter whatever structure you hand it. citeturn27view0turn43view4

The output should be a compact signed-off report, not just score rows: distribution summaries, percentile cut-offs, and a note on whether any score component is spuriously overactive on garbage.

## Codex engineering roadmap and GPU future

### Prompt-ready engineering stages

| Stage | Objective | Likely areas affected | Tests required | Outputs | Acceptance criteria | Stop conditions | Need more Deep Research? |
|---|---|---|---|---|---|---|---|
| **Stage 3E** | Ingest the evidence-ranked backlog and add the top three queue items plus one control item. | `experiments/`, CPU transform registry, manifest validation, docs, tests | Manifest schema tests, count determinism tests, dry-run planner tests | New manifests, updated backlog docs, dry-run reports | Dry-run counts match table; all items remain within policy; docs explain evidence basis | Any manifest causes selector widening or boundary finalisation | No |
| **Stage 3F** | Implement explicit-key pack execution and run the LP evidence pack plus historical pack. | CPU Vigenère transform layer, CLI wiring, result-store import path | Solved-page regression tests for `DIVINITY` and `FIRFUMFERENFE`; deterministic output ordering; negative-control import tests | JSONL/SQLite results, summary markdown | Both packs execute reproducibly and emit score breakdowns; no solve claim | Top candidates stay noisy and controls fail to discriminate | No |
| **Stage 3G** | Implement prime-minus-one offset sweep and prime-mod/gap family registry. | CPU stream transform layer, manifest schema, scorer integration | p56 parity test; offset schedule tests; wrong-family negative tests | Result sets and family comparison table | p56 remains exact; family items run with deterministic counts; null separation measurable | p56 parity fails or offset schedule nondeterministic | No |
| **Stage 3H** | Add reset/advance ablation and separator-aware state handling. | Separator grammar usage, transform-state machine, docs | Boundary/reset unit tests; separator-preservation tests; solved-page no-regression tests | New result entries, boundary audit output | Reset semantics are explicit and tested; output records show state-policy metadata | Reset policies cause solved baselines to drift unexpectedly | No |
| **Stage 4A** | Add capped F-skip search as a bounded optional transform wrapper. | Transform combinator layer, manifest constraints, scorer | Reproduce known skip-aware solved pages; cap enforcement tests; combinatorial bound tests | Bounded skip-search runs | Cap is enforced, counts are predictable, skip metadata is stored | Candidate count exceeds cap or control separation collapses | No |
| **Stage 4B** | Add clustering/rerank and family-specific negative-control dashboards. | Result analysis/report layer | Result-store integrity tests; cluster determinism tests | Markdown/HTML comparison reports | Engineers can see when high scorers collapse into the same garbage family | Clusterer hides provenance or rewrites rankings silently | No |
| **Stage 5A** | Plan CPU/GPU parity only after the CPU family interfaces stabilise. | CUDA scaffold, CPU reference library, benchmark harness | CPU/GPU parity tests, deterministic test vectors, benchmark smoke | Design note and parity fixtures only | No CUDA kernel is written without a locked CPU reference and benchmark target | CPU interfaces still changing weekly | Probably not |

The repository’s own architecture summary already says the CPU side owns corpus management, manifests, hypothesis generation, provenance, and manual review, while the GPU side should accelerate only large regular transform-and-score batches after CPU references, parity tests, and benchmarks exist. That is exactly right. Follow it. citeturn42view4turn43view4

### Recommended next Codex stage

The clear next stage is:

**Stage 3E — method backlog ingestion and queue update.**

That stage should do four things and only four things:

1. add the evidence-ranked backlog document to the repo;
2. implement manifest support for the top three bounded families if missing;
3. add four queue items: LP evidence key pack, historical motif key pack, p56 local prime sweep, and family-specific negative controls;
4. run only those items that already fit the current operator policy. citeturn43view4turn43view1

If Codex tries to widen scope beyond that, it is wandering.

### GPU/CUDA future analysis

For this project, future GPU value is obvious in principle and premature in practice. The repo already states that CUDA is scaffold/smoke only, and that future CUDA kernels need CPU references, parity tests, and benchmarks before optimisation. That should remain a hard rule. citeturn42view2turn43view4

On the user’s RTX 4060 Ti class hardware, the eventual GPU-suitable work is the boring, regular, batch-heavy part:

| Keep on CPU | Move to GPU later |
|---|---|
| Corpus parsing and locking | Massive transform-and-score batches |
| Boundary and selector logic | Key/offset sweeps over fixed candidate families |
| Manifest expansion | Fast n-gram / rune-gram scoring over thousands of candidates |
| SQLite/JSONL writes | Batch null-control sweeps |
| Branch-heavy skip-mask logic | Top-k reductions if the batch size becomes large enough |
| Manual review and report generation | Repeated candidate scoring over fixed corpora |

The main practical constraint on an 8 GB or 16 GB 4060 Ti is simple: **do not store every plaintext candidate in VRAM**. Store rune arrays as compact indices, score in batches, return only top-k scores and parameter tuples, and reconstruct plaintext on CPU. But that is future work. Right now the highest-value experiments are all well inside CPU policy limits, so a GPU port would save very little wall-clock time while making debugging harder. The GPU can wait its turn; it is not a sacred relic. It is just later. citeturn42view4turn43view4

## Anti-false-positive protocol, open questions, and final recommendations

### Anti-false-positive protocol

The project should formalise a solve-claim firewall that is stricter than most community work. That firewall should be built around the warnings already present in Cicada’s material: *A Warning* says to believe nothing from the book except what you know to be true and to test the knowledge; the 2017 signed message says to beware false paths and verify PGP. That is not subtle. citeturn18view5turn38view0

A candidate from an unsolved page should therefore be treated as **noise by default** unless all of the following are true:

- it is reproducible from a pinned corpus hash, manifest hash, Git commit, and logged transform chain;
- it survives rerun on the same slice with identical outputs;
- it beats the current null and negative controls on at least two independent score components, not just one blended score;
- it remains meaningfully above family-specific negatives after multiple-testing correction within that manifest;
- it produces multi-line coherence, separator plausibility, and non-trivial lexical structure rather than one or two comforting words;
- it is not a known solved phrase being re-injected by the key choice;
- it survives at least one transcript/boundary perturbation test if the relevant boundary is still reviewable;
- it can be independently reimplemented by a second path in the codebase, or at minimum by a tiny standalone verifier.

Anything less is an interesting candidate, not a solve.

### What would convince us we found a real solve

The strict validation standard should be:

1. **Mechanical reproducibility**: an independent script reproduces the plaintext exactly from pinned rune data.  
2. **Control separation**: the candidate family clears current null and negative controls by a large margin, not by noise-level drift.  
3. **Local robustness**: if page boundaries or separators are part of the method, adjacent plausible corpus variants do not destroy the result immediately.  
4. **Semantic coherence**: the text reads as sustained Cicada-style prose across more than a toy fragment.  
5. **Non-circularity**: the result is not simply the key or crib echoed back through scoring bias.  
6. **Provenance completeness**: the result store includes source hashes, manifest, software revision, and review notes.  
7. **Preferably, downstream confirmation**: the output either continues a known thematic arc cleanly, aligns with other pages, or yields an externally checkable clue.  

That is the standard because Cicada’s own published material repeatedly warns against false paths and unverifiable claims. citeturn18view5turn38view0turn40view0

### Open questions checklist

| Open question | Why it matters | Who should answer |
|---|---|---|
| What is the exact selector ID and page set used for the Stage 3A/3B/3D reviewable slice? | It determines the exact manifests for the first five runs. | Human maintainer |
| Does the current CPU transform API already support explicit reset/advance policies, or must Stage 3E add them first? | It changes which backlog items are runnable immediately. | Codex plus maintainer |
| How many candidate `F` positions appear in the current reviewable slice under the project’s present tokenisation? | It determines whether capped F-skip search is viable under policy. | Codex after corpus inspection |
| What exact score components are in the Stage 3C composite scorer, and which of them misfire on current negatives? | It determines whether the next leads are signal or cosmetic noise. | Human maintainer plus result audit |
| Are page-local image anomalies already captured as metadata fields in the candidate corpus, or only in docs? | It affects later image-aware experiments and separator semantics. | Maintainer |
| Which source hashes are already locked locally for rtkd, scream314, and Pastebin-derived mirrors? | It affects reproducibility and whether new manifests need source-lock work first. | Maintainer |

### Recommended next Codex stage

**Stage 3E: ingest the method backlog and queue the top three bounded experiments plus one family-specific negative-control pack.** Do not widen the corpus slice, do not activate canonical corpus, and do not add CUDA work in the same stage. The repo’s public status already points in exactly this direction. citeturn43view4

### Top three bounded experiments to run next

- **`stage3e_vig_lp_evidence_pack_v1` — 48 candidates.**  
  Best blend of low cost and strong evidence. It directly extends solved LP methods and vocabulary. citeturn22view2turn22view5turn21view2

- **`stage3e_prime_minus_one_offsets_v1` — 256 candidates.**  
  Best number-theoretic follow-up because it stays nearest to the only proven prime keystream. citeturn23view5turn23view0

- **`stage3e_vig_history_key_pack_v1` — 56 candidates.**  
  Best historically grounded cheap extension of Stage 3D’s four-key preview, using earlier Cicada books and phrases instead of expanding into a dictionary swamp. citeturn28view7turn28view3turn29view2turn29view4turn30view5

### Do not run yet

- Broad dictionary or wordlist Vigenère search.
- Any unconstrained F-skip mask search.
- Arbitrary magic-square, spiral, or grid-route sweeps without a page-specific clue.
- Broad OEIS sequence campaigns.
- CUDA kernels for unsolved-page search.
- “Page 43 says egalitarianism”-style crib-driven campaigns.
- Any experiment that changes both method family and corpus slice at the same time. citeturn27view0turn42view4turn33search5turn29view0

### Sources that should be mirrored or locked next

- `rtkd/iddqd` repository tree and raw file hashes, because it is the most practical public transcript/image anchor. citeturn11search0
- `scream314/cicada3301` raw files for `liber_primus.md`, `pages_and_ciphers.md`, `2012.md`, `2013.md`, `2014.md`, `2016.md`, and `2017.md`, because they are the workhorse archival references for methods and history. citeturn19search10turn13search8
- Uncovering wiki pages for solved methods, unsolved pages, transliteration, and the 2017 signed message, because they are useful but mutable. citeturn33search4turn41view0turn41view1turn38view0
- The old Pastebin/Dropbox/spreadsheet convenience links listed in the Cicada-solvers gist, because those are exactly the sort of things that evaporate. citeturn36search2
- The verified public PGP key and signed message corpus tied to `7A35090F`, because authenticity gates everything else. citeturn14search2turn38view0turn40view0

### Questions for the user

- What exact reviewable slice selector did Stage 3A/3B/3D use, by manifest or queue ID?
- Does the current code already expose configurable reset/advance semantics for CPU transforms?
- Are you willing for Stage 3E to add one family-specific negative-control run alongside the three candidate-generating runs, even though it produces no “exciting” plaintexts?
- Do you want the historical Vigenère key pack limited strictly to earlier **Cicada-attested** phrases/books, or should it also include a second-tier pack of **LP-solved plaintext** motifs in the same stage?

### Appendices

#### Candidate method formulas

| Family | Definition |
|---|---|
| Atbash | `p_i = 28 - c_i` |
| Atbash plus 3 | `p_i = (28 - c_i + 3) mod 29` |
| Explicit-key Vigenère | `p_i = (c_i - k_{f(i)}) mod 29` |
| Prime-minus-one | `p_i = (c_i - ((prime_i - 1) mod 29)) mod 29` |
| Prime-mod | `p_i = (c_i - (prime_i mod 29)) mod 29` |
| Prime-gap | `p_i = (c_i - ((prime_{i+1}-prime_i) mod 29)) mod 29` |
| Fibonacci | `p_i = (c_i - (Fib_i mod 29)) mod 29` |
| Positional overlay | `p_i = (c_i - ((stream_i ± i) mod 29)) mod 29` |

#### Search-space calculations

For the first five recommended experiments:

- LP evidence key pack: `12 keys × 2 reset modes × 2 advance modes = 48`.
- Historical motif key pack: `14 keys × 2 reset modes × 2 advance modes = 56`.
- Prime-minus-one local sweep: `64 offsets × 2 directions × 2 resets = 256`.
- Reset/advance ablation: `8 base transforms × 4 resets × 2 advance modes = 64`.
- Prime-mod/gap pack: `2 families × 32 offsets × 2 directions × 2 resets = 256`.

These are all comfortably under the project’s current automatic CPU limits. citeturn43view1turn43view2turn43view3

#### Glossary

- **GP / Gematria Primus**: the 29-rune alphabet discovered in the Cicada puzzle chain, mapped to decimal values `0..28` and prime values `2..109`. citeturn20view4
- **Reviewable slice**: a corpus selector whose boundaries are deliberately not yet canonicalised. citeturn42view4
- **Skip-`F` rule**: a solved-page behaviour where plaintext `F` positions are exempted from key/stream advancement. citeturn33search4
- **False path**: Cicada’s own term in the 2017 signed warning; the correct engineering translation is “do not trust unsupported output”. citeturn38view0
- **Family-specific negative control**: a control corpus or transform designed to test whether a particular search family produces high scores on garbage.
