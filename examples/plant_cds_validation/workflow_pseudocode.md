# Plant CDS Validation Workflow: Pseudocode

## Purpose

This document describes a recommended pseudocode workflow for evaluating plant coding sequences (CDS) with Evo 2.

The workflow is designed for plant bioinformaticians who want to use Evo 2 for:

- scoring native CDSs
- comparing original and perturbed sequences
- generating sequence continuation from real prefixes
- validating generated sequence before interpretation

This is a conceptual workflow, not a fully executable script.

---

## Workflow Overview

```text
Input plant CDS FASTA
        |
        v
Clean and validate sequences
        |
        v
Score original CDS
        |
        v
Create perturbed CDS
        |
        v
Score perturbed CDS
        |
        v
Generate continuation from real CDS prefix
        |
        v
Extract generated tail only
        |
        v
Validate generated sequence
        |
        v
Summarize interpretation
```

---

## Step 1: Load input CDS FASTA

Input:

```text
plant_cds.fasta
```

Example:

```text
>AT2G01290_RPI
ATGGCGCTTGCGTATGATCCTCTCTTCATTACATCGGACAAATC...
```

Pseudocode:

```text
read FASTA file
for each sequence:
    store sequence ID
    store sequence string
```

---

## Step 2: Clean and validate sequences

Recommended checks:

```text
for each sequence:
    convert sequence to uppercase
    remove whitespace
    replace U with T
    check for invalid characters
    warn if ambiguous bases are present
    check whether length is divisible by 3
    check whether sequence starts with ATG if expected
    check whether sequence ends with stop codon if expected
```

Recommended allowed characters for strict CDS scoring:

```text
A, T, G, C
```

Optional relaxed characters:

```text
N, R, Y, K, M, S, W, B, D, H, V
```

However, ambiguous bases should be reported because they may affect model scoring.

---

## Step 3: Score original CDS

Pseudocode:

```text
for each original CDS:
    score sequence with Evo 2
    calculate mean log-likelihood
    calculate mean negative log-likelihood
    optionally calculate per-position entropy
    save result to scores_original.csv
```

Recommended output:

```text
sequence_id,length,mean_log_likelihood,mean_NLL,sum_log_likelihood,sum_NLL
```

Interpretation:

> A lower NLL may indicate that the sequence is more predictable to Evo 2, but it does not prove biological function or annotation correctness.

---

## Step 4: Create perturbed CDS

Pseudocode:

```text
for each original CDS:
    create one or more controlled perturbations
```

Possible perturbations:

```text
single nucleotide insertion
single nucleotide substitution
synonymous codon substitution
non-synonymous codon substitution
frameshift-like edit
motif disruption
```

Recommended caution:

> Fully shuffled sequences may be too artificial and may behave similarly to random same-length sequences. Use biologically interpretable perturbations when possible.

---

## Step 5: Score perturbed CDS

Pseudocode:

```text
for each perturbed CDS:
    score sequence with Evo 2
    calculate mean log-likelihood
    calculate mean negative log-likelihood
    compare with original CDS score
    save result to scores_perturbed.csv
```

Suggested comparison:

```text
delta_NLL = perturbed_mean_NLL - original_mean_NLL
```

Interpretation:

| Result | Possible interpretation |
|---|---|
| Perturbed NLL > Original NLL | Perturbation may make sequence less model-plausible |
| Perturbed NLL ≈ Original NLL | Model may be insensitive to this edit |
| Perturbed NLL < Original NLL | Perturbed sequence is more model-predictable; biological interpretation requires caution |

---

## Step 6: Generate continuation from real prefix

For each CDS:

```text
prefix = first 500 bp of original CDS
native_tail = downstream sequence after first 500 bp
generated_tail = Evo 2 continuation from prefix
full_generated = prefix + generated_tail
```

Pseudocode:

```text
for each original CDS:
    extract first 500 bp as prefix
    generate N bp continuation using Evo 2
    save full generated sequence
    save generated tail only
```

Recommended output files:

```text
generated_full.fasta
generated_tail_only.fasta
native_tail.fasta
```

Important:

> Always save the generated tail separately. Full-sequence analysis may be dominated by the authentic prefix.

---

## Step 7: Validate generated continuation

Recommended validation checks:

```text
for each generated sequence:
    BLAST full generated sequence
    BLAST generated tail only
    compare generated tail with native downstream sequence
    translate full generated sequence
    check for premature stop codons
    check reading frame
    check amino acid similarity
    check low-complexity regions
    check homopolymer runs
```

Suggested low-complexity checks:

```text
longest homopolymer run
dinucleotide repeat count
trinucleotide repeat count
sequence entropy
simple repeat detection
```

---

## Step 8: Summarize results

Recommended summary table:

```text
species,gene,sequence_type,length,NLL,delta_NLL,tail_BLAST_result,ORF_preserved,low_complexity_warning,interpretation
```

Example interpretation categories:

| Category | Meaning |
|---|---|
| Coherent continuation | Tail BLAST supports correct gene family and ORF is preserved |
| Prefix-carried result | Full BLAST is strong but tail-only BLAST is weak |
| Low-complexity artifact | Generated sequence is repetitive despite low NLL |
| Frame-disrupted | Generated sequence introduces stop codons or frame problems |
| Ambiguous | Requires further validation |

---

## Step 9: Interpret cautiously

Recommended principle:

```text
Evo 2 score or generated output should be interpreted as computational evidence only.
It should not be treated as proof of biological function.
```

Best-practice interpretation:

```text
Evo 2 output → hypothesis
BLAST/alignment/ORF/repeat checks → validation
biological context → interpretation
```

Avoid:

```text
low NLL → functional sequence
generated sequence → real gene
species prompt → species-specific sequence
full BLAST hit → generated region is correct
```

---

## Minimal Pilot Design

A minimal plant CDS benchmark can use:

```text
Species:
- Arabidopsis thaliana
- Sapria himalayana

Genes:
- RPI
- EF-1α
- PGK

Sequence types:
- original CDS
- perturbed CDS
- prefix
- native tail
- generated full sequence
- generated tail only
```

This design produces:

```text
6 original CDSs
6 perturbed CDSs
6 prefix-conditioned generations
6 generated tails
```

This is small enough for manual inspection but structured enough to reveal model behavior.

---

## Final Recommendation

The recommended workflow is:

```text
score → perturb → compare → generate → isolate tail → validate → interpret
```

not:

```text
generate → trust
```

For plant bioinformatics, Evo 2 is best used as a guided sequence-scoring and continuation assistant whose outputs must be checked using conventional biological validation.
