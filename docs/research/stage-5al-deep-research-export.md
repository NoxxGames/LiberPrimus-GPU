# Stage 5AL Deep Research Export

Stage 5AL creates a private Deep Research export manifest at
`data/source-harvester/stage5al-deep-research-export.yaml` and ignored helper files under
`research-inputs/stage5al/`.

The export tells Deep Research what to consume:

- Stage 5AI curated bundle metadata
- Stage 5AJ UsefulFilesAndIdeas metadata
- Stage 5AK community-facts claim metadata
- Stage 5AL publication gates and data contract

The export also records what not to analyze yet: raw third-party files, private message
bodies, generated extract bodies, OCR/image/stego/audio workflows, CUDA, benchmarks, scored
experiments, and solve claims.

Recommended next prompt: Stage 5AM - Deep Research source inventory and reliability prompt.
