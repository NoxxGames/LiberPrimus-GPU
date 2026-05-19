# Confidence Labels

Stage 4I confidence labels are a closed set:

- `positive_control_like`
- `plausible_lead`
- `weak_lead`
- `noisy`
- `inconclusive`
- `garbage`
- `negative_control_like`
- `scoring_not_available`
- `calibration_not_available`

Legacy labels are mapped through `data/scoring/scorer-compatibility-map-v0.yaml`. In particular, legacy `lead` maps to `plausible_lead`; `weak_lead`, `noisy`, and `garbage` keep their meanings.

No label can mean `solved` or `plaintext_verified`.
