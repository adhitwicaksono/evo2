#!/usr/bin/env python3
"""
Validate plant CDS FASTA sequences before Evo 2 scoring or generation.

This script performs lightweight checks that are useful before interpreting
Evo 2 scores or generated continuations.

Checks include:
- sequence length
- invalid characters
- ambiguous bases
- length divisibility by 3
- start codon
- terminal stop codon
- internal stop codons
- longest homopolymer run
- simple low-complexity warning

This script does not require Evo 2, PyTorch, CUDA, or GPU access.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


VALID_DNA = set("ATGC")
AMBIGUOUS_DNA = set("NRYKMSWBDHV")
STOP_CODONS = {"TAA", "TAG", "TGA"}


def read_fasta(path: Path) -> Iterable[Tuple[str, str]]:
    """Read FASTA records as (header, sequence)."""
    header = None
    chunks: List[str] = []

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(chunks)
                header = line[1:].strip()
                chunks = []
            else:
                chunks.append(line)

        if header is not None:
            yield header, "".join(chunks)


def clean_sequence(seq: str) -> str:
    """Uppercase sequence, remove whitespace, and convert U to T."""
    return "".join(seq.split()).upper().replace("U", "T")


def longest_homopolymer(seq: str) -> int:
    """Return the length of the longest identical-base run."""
    if not seq:
        return 0

    max_run = 1
    current_run = 1

    for i in range(1, len(seq)):
        if seq[i] == seq[i - 1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1

    return max_run


def count_internal_stops(seq: str) -> int:
    """Count in-frame internal stop codons, excluding terminal codon."""
    count = 0
    usable_len = len(seq) - (len(seq) % 3)

    for i in range(0, max(usable_len - 3, 0), 3):
        codon = seq[i:i + 3]
        if codon in STOP_CODONS:
            count += 1

    return count


def validate_record(header: str, raw_seq: str) -> Dict[str, object]:
    """Validate one FASTA record."""
    seq = clean_sequence(raw_seq)

    chars = set(seq)
    invalid_chars = sorted(chars - VALID_DNA - AMBIGUOUS_DNA)
    ambiguous_chars = sorted(chars & AMBIGUOUS_DNA)

    length = len(seq)
    divisible_by_3 = length % 3 == 0
    starts_with_atg = seq.startswith("ATG") if length >= 3 else False
    terminal_codon = seq[-3:] if length >= 3 else ""
    has_terminal_stop = terminal_codon in STOP_CODONS
    internal_stop_count = count_internal_stops(seq) if divisible_by_3 else "NA"
    longest_run = longest_homopolymer(seq)

    low_complexity_warning = "yes" if longest_run >= 10 else "no"

    return {
        "sequence_id": header,
        "length": length,
        "divisible_by_3": divisible_by_3,
        "starts_with_ATG": starts_with_atg,
        "terminal_codon": terminal_codon,
        "has_terminal_stop": has_terminal_stop,
        "internal_stop_count": internal_stop_count,
        "ambiguous_bases": "".join(ambiguous_chars) if ambiguous_chars else "none",
        "invalid_characters": "".join(invalid_chars) if invalid_chars else "none",
        "longest_homopolymer": longest_run,
        "low_complexity_warning": low_complexity_warning,
    }


def write_report(rows: List[Dict[str, object]], output: Path) -> None:
    """Write validation report as CSV."""
    if not rows:
        raise ValueError("No FASTA records were found.")

    fieldnames = list(rows[0].keys())

    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate plant CDS FASTA sequences before Evo 2 analysis."
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=Path,
        help="Input CDS FASTA file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="Output CSV validation report.",
    )

    args = parser.parse_args()

    rows = []
    for header, seq in read_fasta(args.input):
        rows.append(validate_record(header, seq))

    write_report(rows, args.output)

    print(f"Validated {len(rows)} sequence(s).")
    print(f"Report written to: {args.output}")


if __name__ == "__main__":
    main()
