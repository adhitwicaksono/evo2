# Potential Pull Request Summary: Plant CDS Validation Guidance for Evo 2

## Purpose

This branch adds a plant-bioinformatics-oriented audit and example workflow for using Evo 2 on plant coding sequences (CDS). The goal is to improve biological interpretability and validation guidance for users who want to apply Evo 2 to plant genomics, especially CDS scoring, perturbation comparison, and prefix-conditioned sequence continuation.

This is intended as a constructive documentation and example contribution, not a change to core Evo 2 model behavior.

---

## Motivation

Evo 2 provides powerful infrastructure for genomic sequence modeling, scoring, embeddings, and generation. However, biological users may need additional guidance to interpret model scores and generated sequences responsibly.

In particular, plant users may face challenges such as:

- long introns
- repeat-rich gene regions
- complex gene models
- non-model species
- ambiguous annotations
- generated sequences with low-complexity or repetitive artifacts
- overinterpretation of low negative log-likelihood (NLL)

This branch proposes validation-oriented documentation to help users avoid treating Evo 2-generated sequences as biologically valid without independent checks.

---

## Main Additions

### Audit notes

Added audit notes covering:

- README usability
- scoring utilities
- model wrapper/API behavior
- generation tests
- configuration clarity
- utility functions and phylogenetic tags
- generation notebook behavior
- recommendations for plant users
- domain and family guardrails

### Plant CDS validation example

Added an example folder:

```text
examples/plant_cds_validation/
```

This folder provides a recommended workflow for:

- validating plant CDS FASTA files
- preparing perturbed CDS variants
- preparing prefixes and native tails
- interpreting Evo 2 scoring
- evaluating generated tails separately
- applying ORF, BLAST, HMMER, Pfam, Rfam, and low-complexity guardrails

### Helper scripts

Added lightweight helper scripts that do not require Evo 2, PyTorch, CUDA, or GPU access:

```text
validate_cds_fasta.py
prepare_cds_variants.py
```

These scripts support preflight validation and preparation of plant CDS sequences before Evo 2 scoring or generation.

### Guardrail documentation

Added guidance for combining Evo 2 with biological validation tools such as:

- ORF checks
- Pfam/HMMER
- custom plant-family HMMs
- BLASTp/DIAMOND
- Rfam/Infernal
- low-complexity screening
- generated-tail-only validation

---

## Key Recommendation

The recommended workflow is:

```text
score → perturb → compare → generate → isolate tail → validate → interpret
```

not:

```text
generate → trust
```

Evo 2 should be viewed as a sequence plausibility and continuation model whose outputs require conventional biological validation.

---

## Why This Matters for Plant Users

Plant genomes often contain large introns, high repeat content, duplicated gene families, transposable elements, and complex annotation challenges. These features can make direct interpretation of foundation-model scores or generated sequences difficult.

A plant-specific validation workflow can help users distinguish between:

- biologically coherent continuation
- prefix-carried similarity
- low-complexity artifacts
- functional-neighborhood drift
- unsupported generation
- possible annotation issues

---

## Suggested Future Improvements

Future Evo 2 documentation or examples could include:

1. FASTA-based scoring workflow with NLL and entropy output.
2. Plant CDS continuation notebook.
3. Generated-sequence validation checklist.
4. Tail-only BLAST guidance for prefix-conditioned generation.
5. ORF/frame validation examples.
6. Low-complexity and homopolymer detection examples.
7. Pfam/HMMER and Rfam/Infernal guardrail examples.
8. Clearer model-selection guide for biological users.
9. Safer species-tag prompting documentation.
10. Example workflow for non-model plant genomes.

---

## Scope

This branch does not modify core Evo 2 model code.

It focuses on:

- documentation
- audit notes
- plant-user recommendations
- lightweight helper scripts
- biological validation guidance

---

## Intended Tone

This contribution is intended to be constructive and supportive. Evo 2 is a powerful genomic foundation model, and the goal of this branch is to help biological users apply it more carefully and reproducibly.
