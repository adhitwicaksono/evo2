# Evo 2 Plant-CDS Audit Notes

## Purpose

This folder contains audit notes written from a plant-bioinformatics user perspective. The goal is not to criticize Evo 2, but to identify practical opportunities to make the repository easier, safer, and more useful for biological users, especially plant scientists working with coding sequences, long genes, repeat-rich genomes, and non-model species.

The audit focuses on:

- usability for plant bioinformaticians
- sequence scoring workflows
- generation and continuation behavior
- biological validation needs
- documentation clarity
- reproducibility and model-selection guidance

---

## Audit Scope

The current audit covers the following parts of the repository:

| File | Focus |
|---|---|
| `01_readme_audit.md` | README clarity, installation guidance, biological interpretation gaps |
| `02_scoring_py_audit.md` | sequence scoring utilities, NLL/log-likelihood usability, FASTA workflow needs |
| `03_models_py_audit.md` | main Evo2 API, model loading, generation interface, biological guardrails |
| `04_test_generation_audit.md` | generation test behavior, regression testing, missing scoring tests |
| `05_config_audit.md` | model config clarity, context length, FP8 settings, naming confusion |
| `06_utils_audit.md` | model-name mapping and GBIF phylotag helper robustness |
| `07_generation_notebook_audit.md` | generation notebook workflow, alignment analysis, missing validation layers |
| `08_recommendations_for_plant_users.md` | practical recommendations for plant CDS users |

---

## Main Finding

Evo 2 provides strong infrastructure for genomic foundation model inference, including public checkpoints, scoring utilities, generation functions, and example notebooks. However, the repository is currently more accessible to machine-learning users than to biological users.

From a plant-bioinformatics perspective, the main opportunity is to add clearer biological validation workflows.

In particular:

> Evo 2 should be treated as a sequence scoring and context-aware continuation model, not as an autonomous generator of biologically validated genes.

---

## Key Strengths Identified

- Public repository and public model checkpoints.
- Clear Python API through the `Evo2` class.
- Useful internal scoring utilities.
- Generation support from sequence prompts.
- Long-context model configurations.
- Example generation notebook.
- Prefix-conditioned continuation tests.
- Hugging Face model integration.

---

## Key Improvement Opportunities

### 1. FASTA-based scoring workflow

A user-facing FASTA scoring workflow would help biological users score real sequences without writing custom Python code.

Suggested output:

| Output | Description |
|---|---|
| sequence ID | FASTA header |
| length | sequence length |
| mean log-likelihood | model score |
| mean NLL | positive negative log-likelihood |
| summed NLL | total sequence NLL |
| per-position entropy | optional positional uncertainty |

---

### 2. Plant CDS continuation example

A plant-focused notebook or example folder would help users evaluate Evo 2 on real coding sequences.

Suggested workflow:

1. Load plant CDS FASTA.
2. Score original CDS.
3. Create controlled perturbation.
4. Score perturbed CDS.
5. Generate continuation from real prefix.
6. Extract generated tail only.
7. BLAST generated tail.
8. Translate ORF.
9. Check stop codons and reading frame.
10. Interpret cautiously.

---

### 3. Generated-sequence validation checklist

Generated sequences should be validated before biological interpretation.

Recommended checks:

- low-complexity content
- homopolymer runs
- BLAST full output
- BLAST generated tail only
- ORF preservation
- premature stop codons
- reading-frame consistency
- gene-family specificity
- taxonomic specificity

---

### 4. Clearer model-selection guidance

The repository would benefit from a practical guide explaining which model/checkpoint to use for different biological tasks.

Example:

| Task | Suggested model type |
|---|---|
| short CDS scoring | smaller/base or 7B model |
| long plant gene region | 7B long-context model |
| whole genomic fragment | long-context model or hosted inference |
| fast local testing | smallest available checkpoint |
| serious benchmarking | compare multiple checkpoints |

---

### 5. Safer species-tag generation

Species-tag prompting is useful but should be handled carefully.

Recommended improvements:

- validate GBIF match confidence
- check accepted taxon names
- handle failed requests safely
- avoid returning malformed tags
- validate generated sequences with BLAST and complexity checks

---

## Plant-CDS Perspective

For plant users, Evo 2 may be especially useful for:

- scoring conserved coding sequences
- comparing model and non-model plant CDSs
- testing sensitivity to frameshift-like perturbations
- evaluating manually curated gene models
- continuing partial coding sequences from authentic prefixes
- exploring sequence plausibility in unusual plant genomes

However, plant genomes pose special challenges:

- long introns
- transposable elements
- repeat-rich regions
- duplicated gene families
- pseudogenes
- organellar insertions
- annotation artifacts
- uneven representation in training data

Therefore, Evo 2 outputs should be interpreted alongside conventional genomic evidence.

---

## Recommended Interpretation Principle

The safest workflow is:

```text
score → perturb → compare → generate → isolate tail → validate → interpret
```

not:

```text
generate → trust
```

---

## Relationship to Example Workflow

The companion example folder is:

```text
examples/plant_cds_validation/
```

It contains a practical plant-CDS validation workflow, example gene candidates, and pseudocode for responsible Evo 2 use in plant bioinformatics.

---

## Final Note

This audit is intended as a constructive contribution. The goal is to help bridge the gap between powerful genomic foundation models and careful biological interpretation, especially for plant scientists working outside the most heavily represented model systems.
