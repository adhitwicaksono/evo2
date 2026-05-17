# Audit note: evo2/scoring.py

## Summary
`scoring.py` contains useful internal utilities for sequence likelihood scoring, reverse-complement scoring, positional entropy, and entropy-derived perplexity. The core logic needed for CDS scoring and perturbation comparison is already present. However, these functions are currently exposed as Python utilities rather than as a biologist-friendly FASTA scoring workflow.

## Strengths
- Provides batch preparation and padding.
- Converts logits to per-position log probabilities.
- Supports mean or summed log-likelihood scoring.
- Supports reverse-complement averaged scoring.
- Provides per-position entropy calculation.
- Can support our plant CDS scoring workflow with a lightweight wrapper.

## Main limitations
1. No command-line FASTA scoring interface.
2. Scores are log-likelihoods, while web interface reports positive NLL; documentation should clarify sign convention.
3. No CSV/TSV output for summary or per-position scores.
4. No obvious input validation for ambiguous bases, lowercase, RNA U, or invalid characters.
5. Reverse-complement averaging may be inappropriate for known CDS unless explicitly requested.
6. No biological interpretation warning: low NLL can reflect low-complexity predictability rather than biological validity.

## Suggested improvement
Add a `score_fasta.py` script or notebook that accepts FASTA input and outputs:
- sequence ID
- length
- mean log-likelihood
- mean NLL
- summed log-likelihood
- summed NLL
- optional per-position entropy
- optional per-position NLL

This would make Evo 2 scoring much more usable for plant bioinformatics workflows.
