# Example Plant CDS Candidates for Evo 2 Validation

## Purpose

This document lists recommended plant coding sequences (CDS) that can be used for testing Evo 2 scoring, perturbation comparison, and prefix-conditioned continuation.

The goal is to use conserved, interpretable genes rather than arbitrary sequences. Conserved housekeeping or metabolic genes are useful because they are easier to compare across plant lineages and less likely to produce misleading results due to lineage-specific novelty.

---

## Recommended Gene Groups

| Group | Gene | Biological role | Why useful for Evo 2 testing |
|---|---|---|---|
| 1 | RPI / ribose-5-phosphate isomerase | Pentose phosphate pathway / plastid metabolism | Conserved metabolic gene; useful for CDS scoring and continuation |
| 2 | EF-1α / elongation factor 1-alpha | Translation elongation | Highly conserved; useful as a stable coding-sequence benchmark |
| 3 | PGK / phosphoglycerate kinase | Glycolysis / carbon metabolism | Conserved enzyme; useful for testing longer CDS continuation |

---

## Suggested Species Comparison

A simple plant-focused comparison can use:

| Species | Role in benchmark |
|---|---|
| *Arabidopsis thaliana* | Model plant reference |
| *Sapria himalayana* | Non-model parasitic plant with unusual genome biology |

This comparison is useful because *Arabidopsis thaliana* is expected to be well represented in public genomic datasets, while *Sapria himalayana* represents a more unusual plant lineage with complex genome features.

---

## Suggested Data Sources

| Species | Suggested source |
|---|---|
| *Arabidopsis thaliana* | TAIR10 CDS annotations |
| *Sapria himalayana* | Manually curated or BRAKER-annotated CDS based on available genome annotation |

For reproducibility, record:

- source database or annotation version
- gene ID
- transcript ID
- CDS length
- strand
- whether the sequence is manually curated
- whether introns were removed before scoring

---

## Recommended Sequence Types

For each gene, prepare the following:

| Sequence type | Description |
|---|---|
| Original CDS | Full coding sequence |
| Perturbed CDS | CDS with a controlled edit |
| Prefix | First 500 bp of original CDS |
| Native downstream region | True downstream sequence following the prefix |
| Evo 2 generated continuation | Model-generated continuation from prefix |
| Generated tail only | Generated region excluding the real prefix |

---

## Suggested Perturbation Types

Use biologically interpretable perturbations.

Recommended:

- single nucleotide insertion
- single nucleotide substitution
- synonymous codon substitution
- non-synonymous codon substitution
- frameshift-like mutation
- short motif disruption

Avoid relying only on fully shuffled sequences, because fully shuffled controls may behave similarly to random same-length sequences and may not represent biologically meaningful perturbation.

---

## Recommended Evaluation Questions

For each gene, ask:

1. Does Evo 2 assign lower NLL to the original sequence than to the perturbed sequence?
2. Is the effect of perturbation consistent across genes?
3. Does prefix-conditioned continuation preserve coding-sequence structure?
4. Does the generated tail show homology to the correct gene family?
5. Does the full generated sequence preserve the reading frame?
6. Does the generated sequence avoid low-complexity or repetitive collapse?
7. Are results different between model plant and non-model parasitic plant sequences?

---

## Suggested Result Table

| Species | Gene | Sequence type | Length | NLL | BLAST result | ORF preserved | Notes |
|---|---|---:|---:|---:|---|---|---|
| *Arabidopsis thaliana* | RPI | Original CDS | NA | NA | NA | NA | NA |
| *Arabidopsis thaliana* | RPI | Perturbed CDS | NA | NA | NA | NA | NA |
| *Sapria himalayana* | RPI | Original CDS | NA | NA | NA | NA | NA |
| *Sapria himalayana* | RPI | Perturbed CDS | NA | NA | NA | NA | NA |

---

## Notes on Interpretation

Conserved genes are useful for benchmarking because they provide clearer biological expectations. However, even for conserved genes, Evo 2 scores and generated outputs should not be interpreted as direct evidence of biological function.

Recommended interpretation:

> Evo 2 can help identify plausible, surprising, or suspicious sequence behavior, but its outputs require conventional validation using ORF checks, homology search, sequence alignment, and biological context.

---

## Minimal Example Set

A minimal pilot benchmark may include:

| Species | Genes |
|---|---|
| *Arabidopsis thaliana* | RPI, EF-1α, PGK |
| *Sapria himalayana* | RPI, EF-1α, PGK |

This produces six original CDSs. With one perturbation per CDS, this gives twelve scoring tests. With one prefix-conditioned continuation per CDS, this gives six generation tests.

This is small enough for manual inspection but structured enough to reveal whether Evo 2 behaves consistently across plant coding sequences.
