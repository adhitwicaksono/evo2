#!/usr/bin/env python3
"""
Prepare plant CDS sequences for Evo 2 scoring and continuation experiments.

This script creates:
- cleaned original CDS FASTA
- perturbed CDS FASTA with a +1 nucleotide insertion
- prefix FASTA for continuation
- native tail FASTA for comparison
- CSV manifest describing all generated records

It does not require Evo 2, PyTorch, CUDA, or GPU access.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


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
    """Uppercase sequence, remove whitespace, and convert RNA U to DNA T."""
    return "".join(seq.split()).upper().replace("U", "T")


def write_fasta(records: List[Tuple[str, str]], path: Path, line_width: int = 80) -> None:
    """Write FASTA records."""
    with path.open("w", encoding="utf-8") as handle:
        for header, seq in records:
            handle.write(f">{header}\n")
            for i in range(0, len(seq), line_width):
                handle.write(seq[i:i + line_width] + "\n")


def insert_base(seq: str, base: str, position_1based: int) -> str:
    """
    Insert base before the nucleotide at position_1based.

    Example:
    seq = ATGC
    insert G at position 3 -> ATGGC
    """
    if position_1based < 1 or position_1based > len(seq) + 1:
        raise ValueError(
            f"Insertion position {position_1based} is outside sequence length {len(seq)}"
        )

    idx = position_1based - 1
    return seq[:idx] + base + seq[idx:]


def safe_id(header: str) -> str:
    """Make a simple sequence ID from FASTA header."""
    return header.split()[0].replace("|", "_").replace(":", "_")


def prepare_records(
    fasta_path: Path,
    prefix_length: int,
    insert_base_char: str,
) -> Tuple[
    List[Tuple[str, str]],
    List[Tuple[str, str]],
    List[Tuple[str, str]],
    List[Tuple[str, str]],
    List[Dict[str, object]],
]:
    """Prepare original, perturbed, prefix, native-tail records and manifest."""
    original_records = []
    perturbed_records = []
    prefix_records = []
    tail_records = []
    manifest_rows = []

    insert_base_char = insert_base_char.upper()
    if insert_base_char not in {"A", "T", "G", "C"}:
        raise ValueError("--insert-base must be one of A, T, G, or C")

    for header, raw_seq in read_fasta(fasta_path):
        seq_id = safe_id(header)
        seq = clean_sequence(raw_seq)

        if not seq:
            continue

        # Default perturbation: insert one base near the CDS midpoint.
        insertion_position = (len(seq) // 2) + 1
        perturbed_seq = insert_base(seq, insert_base_char, insertion_position)

        prefix = seq[:prefix_length]
        native_tail = seq[prefix_length:]

        original_id = f"{seq_id}|original_cds"
        perturbed_id = f"{seq_id}|perturbed_plus1{insert_base_char}_pos{insertion_position}"
        prefix_id = f"{seq_id}|prefix_{prefix_length}bp"
        tail_id = f"{seq_id}|native_tail_after_{prefix_length}bp"

        original_records.append((original_id, seq))
        perturbed_records.append((perturbed_id, perturbed_seq))
        prefix_records.append((prefix_id, prefix))
        tail_records.append((tail_id, native_tail))

        manifest_rows.append(
            {
                "sequence_id": seq_id,
                "original_header": header,
                "original_length": len(seq),
                "perturbed_length": len(perturbed_seq),
                "inserted_base": insert_base_char,
                "insertion_position_1based": insertion_position,
                "prefix_length": len(prefix),
                "native_tail_length": len(native_tail),
                "prefix_is_full_sequence": len(seq) <= prefix_length,
            }
        )

    return original_records, perturbed_records, prefix_records, tail_records, manifest_rows


def write_manifest(rows: List[Dict[str, object]], path: Path) -> None:
    """Write manifest CSV."""
    if not rows:
        raise ValueError("No FASTA records were found.")

    fieldnames = list(rows[0].keys())

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare plant CDS variants for Evo 2 validation workflows."
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
        "--outdir",
        required=True,
        type=Path,
        help="Output directory.",
    )
    parser.add_argument(
        "--prefix-length",
        type=int,
        default=500,
        help="Prefix length for continuation experiments. Default: 500.",
    )
    parser.add_argument(
        "--insert-base",
        default="G",
        help="Base to insert for +1 perturbation. Default: G.",
    )

    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    (
        original_records,
        perturbed_records,
        prefix_records,
        tail_records,
        manifest_rows,
    ) = prepare_records(
        fasta_path=args.input,
        prefix_length=args.prefix_length,
        insert_base_char=args.insert_base,
    )

    write_fasta(original_records, args.outdir / "original_clean.fasta")
    write_fasta(perturbed_records, args.outdir / "perturbed_cds.fasta")
    write_fasta(prefix_records, args.outdir / "prefixes.fasta")
    write_fasta(tail_records, args.outdir / "native_tails.fasta")
    write_manifest(manifest_rows, args.outdir / "variant_manifest.csv")

    print(f"Prepared {len(original_records)} sequence(s).")
    print(f"Output directory: {args.outdir}")


if __name__ == "__main__":
    main()
