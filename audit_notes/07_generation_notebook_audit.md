# Audit note: generation notebook

## Summary
The Evo 2 generation notebook provides a useful demonstration of prefix-conditioned sequence generation and alignment-based comparison against target sequences. It is more user-friendly than the raw API, but it remains a demonstration notebook rather than a full biological validation workflow.

## Strengths
- Clear educational structure.
- Uses Evo2 7B as default.
- Demonstrates sequence continuation from real prefixes.
- Compares generated sequence against downstream target sequence.
- Includes alignment-based evaluation.
- Demonstrates phylogenetic species-tag prompting.

## Limitations
1. Generation parameters are not fully explained; `top_k` and `top_p` are not explicitly shown in the generation cell.
2. Printed generation scores are not biologically interpreted.
3. Alignment similarity metric should be defined more carefully.
4. `pairwise2` should be replaced with `Bio.Align.PairwiseAligner`.
5. Huge raw alignments make the notebook hard to read.
6. Species-tag generation lacks BLAST, low-complexity, and taxonomic validation.
7. No plant-specific CDS example is included.
8. No ORF preservation, stop-codon, codon-frame, or generated-tail-only validation is performed.

## Suggested improvements
- Add explicit generation parameter block.
- Explain score sign convention and NLL/log-likelihood interpretation.
- Add summary metrics table.
- Add generated-tail-only analysis.
- Add low-complexity and homopolymer checks.
- Add BLAST guidance.
- Add plant CDS continuation example.
- Replace `pairwise2` with `PairwiseAligner`.
