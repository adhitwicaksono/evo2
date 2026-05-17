# Audit note: evo2/models.py

## Summary
`models.py` provides the main `Evo2` class, including model loading, forward inference, sequence scoring, embedding extraction, generation, and checkpoint handling. The API is clean for Python/ML users, but still lacks several features that would make Evo 2 easier and safer for biological users, especially plant bioinformaticians.

## Strengths
- Simple `Evo2(model_name)` entry point.
- Supports Hugging Face checkpoint download.
- Supports local checkpoint loading.
- Handles checkpoint shard merging.
- Provides 7B fallback when Transformer Engine is unavailable.
- Exposes sequence scoring through `score_sequences()`.
- Exposes generation through `generate()`.
- Supports embedding extraction by layer hooks.

## Main limitations
1. No FASTA-based scoring or generation interface.
2. No explicit sequence validation for ambiguous bases, lowercase, RNA `U`, or invalid characters.
3. No user-facing entropy method in the `Evo2` class, despite entropy utilities existing in `scoring.py`.
4. No clear generation reproducibility/seed option documented.
5. No biological validation helpers for generated sequences.
6. Reverse-complement averaging is implemented but biological use cases are not explained.
7. Checkpoint download/merge/cache behavior could be documented more clearly.

## Suggested improvements
- Add `score_fasta.py` and `generate_fasta.py` example scripts.
- Add sequence validation utilities.
- Add an `Evo2.positional_entropies()` or `score_sequences_with_entropy()` wrapper.
- Add seed/reproducibility guidance for generation.
- Add generated-sequence sanity-check notebook.
- Add documentation explaining when to use forward-only versus reverse-complement scoring.
