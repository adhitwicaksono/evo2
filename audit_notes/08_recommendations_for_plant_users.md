# Recommendations for Plant Users of Evo 2

## Summary

Evo 2 is a powerful genomic foundation model with public code, checkpoints, and example workflows for sequence scoring, embeddings, and generation. From a plant-bioinformatics perspective, its most promising uses are not unconstrained sequence generation, but rather context-aware tasks such as scoring real sequences, comparing original and perturbed coding sequences, and continuing sequences from biologically meaningful prefixes.

This note summarizes practical recommendations for plant users, especially those working with coding sequences (CDS), complex plant genomes, long introns, repeat-rich regions, and non-model plants.

---

## 1. Recommended Use Cases for Plant Bioinformatics

### 1.1 Scoring real plant coding sequences

Evo 2 can be useful for scoring native plant CDSs or gene regions. This may help users compare whether a sequence appears more or less plausible under the model.

Potential applications:

- Comparing coding sequences from model and non-model plants.
- Evaluating manually curated gene models.
- Comparing original versus edited or perturbed sequences.
- Screening unusual CDS annotations in difficult genomes.
- Identifying sequences that may deserve closer manual inspection.

However, model score should not be interpreted as direct evidence of biological function.

Recommended interpretation:

> Lower negative log-likelihood (NLL) or higher likelihood may indicate that the sequence is more familiar or predictable to the model, but it does not prove that the sequence is functional, correctly annotated, or biologically valid.

---

### 1.2 Comparing original and perturbed sequences

For plant CDS analysis, Evo 2 may be useful for comparing an original coding sequence against a minimally edited version.

Possible perturbations include:

- Single nucleotide insertion.
- Single nucleotide substitution.
- Codon-preserving synonymous edits.
- Frameshift-like edits.
- Codon-level shuffling.
- Local motif disruption.

Recommended approach:

1. Score the original sequence.
2. Score the perturbed sequence.
3. Compare mean NLL or mean log-likelihood.
4. Inspect per-position entropy if available.
5. Validate the biological consequence separately.

Important caution:

> A small change in NLL does not necessarily mean the model understands the biological effect of the mutation. Evo 2 should be treated as a plausibility model, not a functional oracle.

---

### 1.3 Prefix-conditioned continuation

Prefix-conditioned continuation appears to be one of the most promising use cases for Evo 2.

In this workflow, a real sequence prefix is provided to the model, and Evo 2 generates the downstream continuation.

Recommended examples:

- First 500 bp of a plant CDS → generate downstream 200 bp.
- Partial transcript sequence → generate possible continuation.
- Conserved gene fragment → explore plausible downstream sequence space.

This is more biologically grounded than organism-only generation because the model is anchored by authentic sequence context.

Recommended validation:

1. Compare the full generated sequence against the expected sequence if available.
2. Extract the generated tail only.
3. BLAST the generated tail separately.
4. Translate the full generated sequence if it is expected to be coding.
5. Check for premature stop codons.
6. Check whether the reading frame is preserved.
7. Check low-complexity or repetitive sequence content.

Key recommendation:

> For prefix-conditioned generation, full-sequence BLAST can be misleading because the real prefix may dominate the result. The generated tail should be analyzed separately.

---

## 2. Use Cases That Require Caution

### 2.1 Unconstrained de novo generation

Generating DNA from minimal prompts or organism labels alone should be interpreted cautiously.

Potential issues:

- Low-complexity repeats.
- Homopolymer expansion.
- Taxonomically nonspecific hits.
- Weak or absent BLAST support.
- High model confidence despite poor biological meaning.
- Generated sequences that are statistically plausible but biologically uninformative.

Recommendation:

> Do not interpret organism-only generated sequences as functional, species-specific, or biologically meaningful without independent validation.

---

### 2.2 Species-tag prompting

Evo 2 supports generation using phylogenetic species tags. This is potentially useful, but plant users should treat this mode carefully.

Recommended checks:

- Confirm that the species tag is taxonomically correct.
- Check whether the taxon name is accepted or a synonym.
- Check whether the generated sequence has meaningful BLAST hits.
- Check whether the sequence is low-complexity.
- Compare generated sequences against related taxa.
- Avoid interpreting generated sequence as truly species-specific without evidence.

For rare, non-model, parasitic, or poorly represented plant lineages, species-tag generation may be especially uncertain.

---

### 2.3 Long plant genomic regions

Many plant genes contain long introns, repetitive elements, transposons, and complex regulatory regions. Long-context models may be useful for such regions, but practical interpretation is difficult.

Potential plant-specific challenges:

- Repeat-rich gene regions.
- Long introns.
- Transposable element insertions.
- Segmental duplications.
- Highly duplicated gene families.
- Organellar insertions.
- Pseudogenes.
- Annotation artifacts.

Recommendation:

> For long genomic regions, combine Evo 2 scoring with conventional genome annotation, repeat annotation, transcript evidence, homology search, and manual curation.

---

## 3. Suggested Validation Workflow for Plant CDS Generation

For plant CDS continuation or generation, we recommend the following validation workflow.

### Step 1: Define the biological task

Before using Evo 2, specify the task clearly:

- CDS scoring?
- Perturbation comparison?
- Prefix continuation?
- De novo generation?
- Annotation triage?
- Variant prioritization?

Avoid using the same interpretation for all modes.

---

### Step 2: Prepare clean input sequences

Recommended preprocessing:

- Use uppercase DNA sequence.
- Remove spaces and line breaks.
- Avoid RNA `U`; convert to `T`.
- Check for ambiguous bases such as `N`, `R`, `Y`, `K`, `M`, etc.
- Record whether the sequence is CDS, genomic DNA, promoter, intron, or unknown region.
- Use the biologically correct strand for known CDSs.

For known CDSs, forward-strand scoring is usually preferable to reverse-complement averaged scoring.

---

### Step 3: Score original sequence

Record:

- Sequence ID.
- Sequence length.
- Mean log-likelihood.
- Mean NLL.
- Summed log-likelihood or summed NLL if needed.
- Per-position entropy if available.

Recommended output format:

```text
sequence_id,length,mean_log_likelihood,mean_NLL,sum_log_likelihood,sum_NLL
