# Plant CDS Validation Workflow for Evo 2

## Purpose

This example outlines a practical validation workflow for using Evo 2 on plant coding sequences (CDS). The goal is to help plant bioinformaticians use Evo 2 for sequence scoring, perturbation comparison, and prefix-conditioned continuation while avoiding overinterpretation of generated sequences.

Evo 2 should be treated as a sequence plausibility and continuation model, not as an autonomous generator of biologically validated genes.

---

## Recommended Workflow

### 1. Prepare input CDS sequences

Use clean DNA CDS sequences in FASTA format.

Recommended preprocessing:

- Use uppercase DNA letters.
- Remove spaces and line breaks inside sequences.
- Convert RNA `U` to DNA `T`.
- Check for ambiguous bases such as `N`, `R`, `Y`, `K`, or `M`.
- Confirm that the sequence is on the correct coding strand.
- Confirm that the CDS starts and ends as expected.

Example:

```text
>AT2G01290_RPI
ATGGCGCTTGCGTATGATCCTCTCTTCATTACATCGGACAAATC...
```

---

### 2. Score the original sequence

Score the original CDS using Evo 2.

Recommended outputs:

- sequence ID
- sequence length
- mean log-likelihood
- mean negative log-likelihood (NLL)
- summed log-likelihood
- summed NLL
- optional per-position entropy

Important interpretation:

> A lower NLL may indicate that the sequence is more predictable to Evo 2, but it does not prove biological function or correct annotation.

---

### 3. Score a perturbed sequence

Create biologically interpretable perturbations.

Possible perturbations:

- single nucleotide insertion
- single nucleotide substitution
- synonymous codon substitution
- non-synonymous codon substitution
- codon-level motif disruption
- frameshift-like mutation

Avoid relying only on fully shuffled sequences, because fully shuffled controls may behave similarly to random same-length sequences.

---

### 4. Generate continuation from a real prefix

For prefix-conditioned continuation:

1. Take the first part of a real CDS, for example 500 bp.
2. Ask Evo 2 to generate a downstream continuation, for example 200 bp.
3. Store both the full generated sequence and the generated tail only.

Example:

```text
>gene_prefix
[first 500 bp of real CDS]

>gene_full_generated
[prefix + generated continuation]

>gene_generated_tail
[generated continuation only]
```

---

### 5. Validate the generated tail

The generated tail should be evaluated separately from the full output.

Recommended checks:

- BLAST the full generated sequence.
- BLAST the generated tail only.
- Compare the generated tail against the true downstream CDS if available.
- Translate the full generated sequence.
- Check for premature stop codons.
- Check reading-frame preservation.
- Check amino acid similarity.
- Check low-complexity or repetitive content.
- Check long homopolymer runs.

Important caution:

> Full-sequence BLAST can be misleading when the first part of the sequence is a real biological prefix. The authentic prefix may dominate the BLAST result. Tail-only BLAST is more informative for evaluating the generated portion.

---

## Suggested Interpretation Table

| Observation | Suggested interpretation |
|---|---|
| Low NLL + good BLAST + ORF preserved | Potentially coherent continuation |
| Low NLL + repetitive sequence | Predictable but not necessarily meaningful |
| Good full-sequence BLAST + poor tail-only BLAST | Result may be carried by the real prefix |
| Poor BLAST + ORF preserved | Possibly nonspecific; requires caution |
| Frameshift or premature stop codon | Not reliable as coding continuation |
| Strong plant/gene-family tail BLAST | More promising, but still requires validation |

---

## Recommended Plant Example Genes

The following conserved plant genes are useful for pilot testing:

| Gene group | Example use |
|---|---|
| RPI / ribose-5-phosphate isomerase | conserved metabolic enzyme |
| EF-1α / elongation factor 1-alpha | conserved translation-related gene |
| PGK / phosphoglycerate kinase | conserved glycolytic enzyme |

These genes are useful because they are interpretable, conserved, and comparable across plant lineages.

---

## Suggested Output Files

A complete plant CDS validation run could produce:

```text
scores_original.csv
scores_perturbed.csv
generated_full.fasta
generated_tail_only.fasta
blast_full_results.tsv
blast_tail_results.tsv
orf_validation.tsv
low_complexity_report.tsv
summary_interpretation.md
```

---

## Minimal Validation Checklist

Before interpreting an Evo 2-generated plant sequence:

```text
[ ] Original sequence is clean and correctly oriented
[ ] Original CDS score recorded
[ ] Perturbed CDS score recorded
[ ] Generation parameters recorded
[ ] Full generated sequence saved
[ ] Generated tail saved separately
[ ] Full sequence BLAST performed
[ ] Tail-only BLAST performed
[ ] ORF translated
[ ] Premature stop codons checked
[ ] Reading frame checked
[ ] Low-complexity/repeats checked
[ ] NLL interpreted cautiously
```

---

## Main Recommendation

The safest workflow is not:

```text
prompt → generate → trust
```

but:

```text
prompt → generate/score → validate → compare → interpret cautiously
```

For plant bioinformatics, Evo 2 is most useful as a guided sequence scoring and continuation assistant. Its outputs should be treated as hypotheses that require conventional biological validation.
