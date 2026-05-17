# Audit note: evo2/utils.py

## Summary
`utils.py` defines the public model names, Hugging Face checkpoint mapping, configuration mapping, and a helper function to generate phylogenetic tags from GBIF. The file is simple and readable, but several details could be improved for robustness and biological usability.

## Strengths
- Public model names are clearly listed.
- Hugging Face repositories are explicitly mapped.
- Config files are explicitly mapped.
- The GBIF phylotag helper is useful in principle for generation prompts.

## Limitations
1. `MODEL_NAMES` and test-supported model names are inconsistent.
2. Model metadata is split across multiple dictionaries rather than one source of truth.
3. `evo2_7b_microviridae` uses a different Hugging Face namespace and could use documentation.
4. Config naming may confuse users, especially `evo2_7b_base` mapping to an `8k` config with a larger `max_seqlen`.
5. `make_phylotag_from_gbif()` is annotated as returning `dict` but returns a string.
6. `make_phylotag_from_gbif()` may crash if GBIF lookup fails because `phylo_tag` may be undefined.
7. GBIF requests have no timeout or exception handling.
8. Missing taxonomy fields may produce tags containing `None`.
9. GBIF match confidence and synonym/accepted-name status are not checked.

## Suggested improvements
- Replace separate mapping dictionaries with one `MODEL_METADATA` dictionary.
- Derive `MODEL_NAMES`, `HF_MODEL_NAME_MAP`, and `CONFIG_MAP` from metadata.
- Update tests to use `MODEL_NAMES` directly.
- Improve GBIF phylotag generation with timeout, error handling, confidence checking, and `Optional[str]` return type.
- Document how phylogenetic tags should be used and validated.
