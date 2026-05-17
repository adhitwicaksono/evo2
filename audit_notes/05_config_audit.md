# Audit note: Evo 2 configuration files

## Summary
The 7B configuration files reveal that Evo 2 model variants share broadly similar architecture but differ in context length, positional scaling, and precision settings. These configs are useful for engineers, but several naming and documentation details may confuse biological users.

## Observations
- `evo2-7b-1m.yml` has `max_seqlen: 1048576`, confirming 1M context.
- `evo2-7b-1m.yml` uses interpolated rotary positional embeddings with `rotary_emb_scaling_factor: 128`.
- `evo2-7b-8k.yml` has `max_seqlen: 32768`, which is larger than the filename implies.
- Both `7b-1m` and `7b-8k` configs use the same internal `model_name: shc-evo2-7b-8k-2T-v2`, which may confuse users.
- `7b-1m` sets `use_fp8_input_projections: True`, although the model loader can fall back to bf16 for 7B models if Transformer Engine is unavailable.

## Strengths
- Configs expose architecture parameters clearly.
- Long-context capability is explicitly encoded.
- Precision settings are configurable.
- The 7B family appears accessible relative to 20B/40B models.

## Potential confusion
1. Config filename `7b-8k` does not match `max_seqlen: 32768`.
2. Internal `model_name` includes `8k` even in the 1M config.
3. FP8 setting in the 7B-1M config may appear contradictory to README claims unless users inspect model-loading fallback logic.
4. Users are not guided on which config/checkpoint is best for short CDSs, long genes, or whole genomic regions.

## Suggested improvements
- Add a public model-to-config mapping table.
- Explain `model_name` versus checkpoint name.
- Clarify training context versus inference `max_seqlen`.
- Add a short “Which model should I use?” guide.
- Add comments explaining 7B FP8 fallback behavior.
