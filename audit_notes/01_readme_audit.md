# README audit: Evo 2

## Summary
The README is technically solid and provides clear access routes for local inference, Docker, hosted API, NIM, checkpoints, and example notebooks. However, it is written primarily for users already familiar with large GPU-based foundation models. For biological users, especially plant bioinformaticians, the documentation lacks practical interpretation guidance.

## Strengths
- Clear description of Evo 2 and its training dataset.
- Multiple access routes: local install, light 7B install, Docker, hosted API, NIM.
- Checkpoint table is useful.
- Example notebooks are provided.
- Training and finetuning routes are linked.

## Main gaps
1. Forward/scoring example exposes logits but not a ready-to-use NLL/per-base scoring workflow.
2. Generation example lacks biological validation guidance.
3. No explicit warning that low NLL can reflect low-complexity or repetitive predictability.
4. No plant-focused example notebook.
5. No guidance to BLAST generated tails separately from real prefixes.
6. Hardware requirements are listed, but practical VRAM/runtime expectations are missing.
7. Dataset section does not summarize plant/eukaryotic representation.

## Suggested improvements
- Add FASTA-based scoring example with NLL, entropy, and CSV output.
- Add generated-sequence validation checklist.
- Add plant CDS continuation notebook.
- Add low-complexity/repeat warning.
- Add hardware realism table.
- Add OpenGenome2 taxonomic composition summary.
