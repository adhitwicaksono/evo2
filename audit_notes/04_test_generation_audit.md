# Audit note: test_evo2_generation.py

## Summary
The generation test verifies whether Evo 2 can greedily continue known sequences from a prefix and recover the downstream target with an expected percentage identity. This is useful as a regression test for continuation behavior, but it does not test Evo 2 scoring, entropy calculation, FASTA usability, biological interpretation, or generated-sequence validation.

## Strengths
- Tests prefix-conditioned continuation rather than unconstrained generation.
- Uses expected model-specific identity scores.
- Uses fixed random seeds.
- Uses greedy generation with top_k=1.
- Provides a simple installation verification command.

## Limitations
1. Does not test scoring / NLL / entropy functions.
2. Prints "Test Failed" but does not exit with a nonzero status.
3. Assumes CUDA-specific behavior without graceful CPU/no-GPU handling.
4. Only covers a subset of documented checkpoints.
5. Uses direct position-by-position identity without alignment.
6. Does not check low-complexity collapse, ORF preservation, BLAST identity, or biological validity.
7. Does not provide plant-focused validation examples.

## Suggested improvements
- Add `sys.exit(1)` on failed validation.
- Add CUDA availability checks.
- Add tests for scoring and entropy utilities.
- Add FASTA-based test input.
- Add a prefix-conditioned CDS continuation example.
- Add generated-sequence sanity checks or link to a validation notebook.
