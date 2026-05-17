# Domain and Family Guardrails for Evo 2 Plant CDS Workflows

## Purpose

Evo 2 can score and generate DNA sequences, but model plausibility alone is not the same as biological validity. A generated sequence may receive a favorable score because it is predictable, repetitive, or locally sequence-like, even if it does not encode a coherent protein or RNA family.

This document describes how to add biological guardrails around Evo 2 outputs using domain, family, ORF, homology, and complexity checks.

The goal is not to replace Evo 2, but to combine it with established biological validation tools.

Recommended principle:

```text
Evo 2 proposes or scores.
Domain and homology tools constrain.
Biological interpretation decides.
```

---

## 1. Why Evo 2 Needs Guardrails

Evo 2 can be useful for:

- sequence plausibility scoring
- original-versus-perturbed sequence comparison
- prefix-conditioned continuation
- exploratory sequence generation

However, Evo 2 output should not be treated as automatically functional.

Potential failure modes include:

- low-complexity sequence generation
- homopolymer or simple-repeat expansion
- biologically nonspecific sequence
- strong model score without meaningful homology
- coding-frame disruption
- premature stop codons
- generated tails that are only supported because the real prefix dominates full-sequence similarity searches

Therefore, generated sequences should be validated using independent biological evidence.

---

## 2. Recommended Guardrail Layers

For plant protein-coding sequences, use multiple validation layers.

| Layer | Question | Example tools |
|---|---|---|
| Evo 2 score | Does the DNA look plausible to the model? | Evo 2 scoring |
| ORF check | Does it preserve a coding frame? | Biopython, EMBOSS, custom script |
| Protein domain check | Does the translated protein match expected domains? | HMMER + Pfam |
| Protein homology check | Does it resemble real proteins? | BLASTp, DIAMOND |
| Gene-family check | Does it remain in the expected plant gene family? | custom HMM, hmmsearch |
| RNA family check | Does it match known RNA families? | Rfam + Infernal |
| Low-complexity check | Is the sequence repetitive or trivial? | SEG, dustmasker, custom scripts |
| Tail-only check | Is the generated region itself biologically meaningful? | BLAST/HMMER on generated tail |

---

## 3. Protein-Coding Gene Guardrails

For CDS generation or continuation, the most important guardrails are:

1. ORF preservation
2. protein translation
3. Pfam/HMMER domain search
4. BLASTp or DIAMOND homology search
5. low-complexity filtering

Suggested workflow:

```text
Evo 2 generated CDS
        |
        v
clean DNA sequence
        |
        v
check ORF and stop codons
        |
        v
translate to protein
        |
        v
scan translated protein against Pfam or custom HMMs
        |
        v
run BLASTp or DIAMOND
        |
        v
interpret with Evo 2 score + biological evidence
```

---

## 4. ORF and Frame Validation

Before domain analysis, check whether the generated sequence still behaves like a CDS.

Recommended checks:

- sequence length divisible by 3
- correct reading frame
- expected start codon if full CDS
- expected terminal stop codon if full CDS
- no premature internal stop codons
- no frameshift introduced by generation
- translated protein has reasonable length

Example interpretation:

| Observation | Interpretation |
|---|---|
| ORF preserved, no internal stops | Suitable for protein-level validation |
| ORF disrupted by frameshift | Not reliable as CDS continuation |
| Many premature stops | Likely poor coding continuation |
| Tail alone lacks frame context | Validate full prefix + tail together |

---

## 5. Pfam/HMMER Guardrail

Pfam/HMMER is useful for testing whether a translated generated CDS matches known protein families or domains.

Recommended use:

```text
generated DNA → translate protein → hmmscan against Pfam-A.hmm
```

Example command:

```bash
hmmscan \
  --cpu 8 \
  --domtblout pfam.domtblout \
  Pfam-A.hmm \
  generated_proteins.faa
```

Important output fields to inspect:

| Field | Meaning |
|---|---|
| domain accession | Pfam domain ID |
| domain name | family/domain label |
| E-value | statistical significance |
| bit score | strength of match |
| domain coordinates | domain position in query |
| coverage | how much of the expected domain is covered |

Suggested interpretation:

| Result | Interpretation |
|---|---|
| Expected domain found with strong E-value | Supports coherent protein-family identity |
| Related domain found but not exact expected family | Possible functional-neighborhood drift |
| No domain found | Generated protein may be too short, novel-like, or invalid |
| Multiple unexpected domains | Possible chimeric or nonspecific generation |
| Domain found only in real prefix region | Tail may not be biologically supported |

---

## 6. Downloading and Preparing Pfam HMMs

For local HMMER analysis, download the Pfam HMM library and prepare it with `hmmpress`.

Example:

```bash
mkdir -p databases/pfam
cd databases/pfam

wget https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.hmm.gz
gunzip Pfam-A.hmm.gz

hmmpress Pfam-A.hmm
```

This creates indexed files required by `hmmscan`:

```text
Pfam-A.hmm.h3f
Pfam-A.hmm.h3i
Pfam-A.hmm.h3m
Pfam-A.hmm.h3p
```

Do not commit these database files to the repository.

Recommended `.gitignore` entries:

```text
databases/
*.h3f
*.h3i
*.h3m
*.h3p
*.hmm
*.hmm.gz
```

---

## 7. Custom Plant-Family HMM Guardrail

Pfam can detect broad protein domains, but it may not always be specific enough to determine whether a generated sequence remains in the expected plant gene family.

For plant CDS continuation, a custom HMM can be more informative.

Example workflow:

```text
collect homologous plant proteins
        |
        v
align with MAFFT
        |
        v
build custom HMM with hmmbuild
        |
        v
search generated proteins with hmmsearch
```

Example commands:

```bash
mafft --auto plant_RPI_homologs.faa > plant_RPI_homologs.aln.faa

hmmbuild plant_RPI.hmm plant_RPI_homologs.aln.faa

hmmsearch \
  --tblout plant_RPI_hmmsearch.tbl \
  plant_RPI.hmm \
  generated_proteins.faa
```

Suggested use cases:

| Gene | Custom HMM use |
|---|---|
| RPI | test whether generated continuation remains RPI-like |
| EF-1α | test whether generated sequence stays in EF-1α family versus broader GTPase-like neighborhood |
| PGK | test whether generated continuation remains PGK-like |
| CAMTA | test whether domains remain in correct order |
| NLRs | test domain architecture, but interpret carefully |

---

## 8. BLASTp or DIAMOND Guardrail

HMMER is sensitive for domain/family detection, while BLASTp or DIAMOND is useful for nearest-neighbor similarity.

Recommended use:

```bash
diamond blastp \
  --query generated_proteins.faa \
  --db plant_proteins.dmnd \
  --out generated_vs_plants.tsv \
  --outfmt 6 qseqid sseqid pident length evalue bitscore stitle \
  --threads 8
```

Suggested interpretation:

| BLAST/DIAMOND result | Interpretation |
|---|---|
| best hits are expected plant homologs | supports gene-family coherence |
| hits are broad but not specific | possible functional-neighborhood drift |
| hits are cross-kingdom/nonspecific | weak biological specificity |
| no hits | sequence may be too short, invalid, or novel-like |
| only full sequence hits due to prefix | inspect generated tail separately |

---

## 9. Rfam/Infernal Guardrail for RNA or Noncoding Sequences

For RNA families or structured noncoding RNA, use Rfam and Infernal rather than Pfam/HMMER.

Rfam uses covariance models that account for both sequence conservation and RNA secondary structure.

Suggested workflow:

```text
generated DNA/RNA-like sequence
        |
        v
search against Rfam covariance models
        |
        v
inspect RNA family, E-value, and coverage
```

Example:

```bash
cmscan \
  --cpu 8 \
  --tblout rfam.tblout \
  Rfam.cm \
  generated_noncoding_sequences.fasta
```

Preparing Rfam covariance models:

```bash
mkdir -p databases/rfam
cd databases/rfam

wget https://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/Rfam.cm.gz
gunzip Rfam.cm.gz

cmpress Rfam.cm
```

Do not commit Rfam database files to the repository.

---

## 10. Tail-Only Validation for Prefix-Conditioned Generation

For prefix-conditioned generation, always separate:

```text
real prefix
generated tail
full output = real prefix + generated tail
```

Why this matters:

> Full-sequence BLAST or HMMER results may be dominated by the real prefix. The generated tail must be evaluated separately to determine whether the generated region itself is biologically meaningful.

Recommended files:

```text
generated_full.fasta
generated_tail_only.fasta
native_tail.fasta
```

Recommended checks:

| Check | Full output | Tail only |
|---|---|---|
| Evo 2 score | useful | useful if supported |
| BLASTn | may be prefix-dominated | more informative for tail |
| BLASTp | useful after translation | useful if tail is in frame |
| HMMER/Pfam | useful for domain architecture | useful if tail covers domain region |
| ORF check | essential | tail alone may need frame context |

---

## 11. Low-Complexity and Repeat Guardrail

Low NLL or high model confidence may reflect repetitive predictability rather than biological coherence.

Check for:

- long homopolymers
- dinucleotide repeats
- trinucleotide repeats
- low sequence entropy
- simple AT-rich or GC-rich collapse
- repeated short motifs

Suggested warning rules:

| Pattern | Warning |
|---|---|
| homopolymer length >= 10 | possible low-complexity artifact |
| repeated motif dominates sequence | possible generation collapse |
| strong NLL but no BLAST/HMM support | likely statistical predictability, not biology |
| tail-only sequence has no meaningful hits | continuation may not be biologically anchored |

---

## 12. Candidate Ranking Framework

A generated CDS candidate can be ranked using multiple evidence layers.

Suggested table:

| Evidence | Good sign | Bad sign |
|---|---|---|
| Evo 2 NLL | lower than weak baseline | low only because repetitive |
| ORF | preserved | frameshift/stops |
| Pfam/HMMER | expected domain found | no or wrong domain |
| custom HMM | expected family support | family drift |
| BLASTp/DIAMOND | plant homologs | nonspecific/cross-kingdom hits |
| low-complexity | no warning | strong warning |
| tail-only analysis | tail has support | full result carried by prefix |

Suggested interpretation labels:

| Label | Meaning |
|---|---|
| high-confidence coherent continuation | multiple evidence layers agree |
| plausible but needs review | some evidence supports, some uncertain |
| functional-neighborhood drift | biologically coherent but wrong exact family |
| low-complexity artifact | model score likely driven by trivial predictability |
| unsupported generation | no clear biological evidence |

---

## 13. Recommended Minimal Guardrail Workflow

For plant CDS continuation:

```text
1. Score original CDS with Evo 2.
2. Generate continuation from real prefix.
3. Extract generated tail.
4. Translate full prefix + generated tail.
5. Check ORF and stop codons.
6. Run Pfam/HMMER on translated protein.
7. Run BLASTp/DIAMOND against plant proteins.
8. BLAST generated DNA tail if appropriate.
9. Check low-complexity and homopolymers.
10. Interpret only after combining all evidence.
```

---

## 14. Final Recommendation

Evo 2 should not be used alone for biological claims.

Recommended responsible workflow:

```text
Evo 2 score/generate
        |
        v
ORF and frame validation
        |
        v
Pfam/HMMER or Rfam/Infernal
        |
        v
BLAST/DIAMOND
        |
        v
low-complexity screening
        |
        v
biological interpretation
```

For plant bioinformatics, the most useful approach is not unconstrained generation, but constrained and validated sequence exploration.
