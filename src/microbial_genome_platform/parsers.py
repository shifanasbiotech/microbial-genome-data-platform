from pathlib import Path

from Bio import SeqIO


def parse_fasta(fasta_path: str | Path) -> list[dict]:
    """
    Parse a FASTA file and return basic information for each sequence.

    Returns:
        A list of dictionaries containing:
        - id
        - description
        - length_bp
        - gc_percent
        - sequence
    """

    fasta_path = Path(fasta_path)

    if not fasta_path.exists():
        raise FileNotFoundError(f"FASTA file not found: {fasta_path}")

    records = []

    for record in SeqIO.parse(fasta_path, "fasta"):
        sequence = str(record.seq).upper()
        length_bp = len(sequence)

        if length_bp == 0:
            gc_percent = 0.0
        else:
            gc_count = sequence.count("G") + sequence.count("C")
            gc_percent = round((gc_count / length_bp) * 100, 3)

        records.append(
            {
                "sequence_id": record.id,
                "description": record.description,
                "length_bp": length_bp,
                "gc_percent": gc_percent,
                "sequence": sequence,
            }
        )

    if not records:
        raise ValueError(f"No FASTA sequences found in: {fasta_path}")

    return records


def parse_gff3(gff_path: str | Path) -> list[dict]:
    """
    Parse a GFF3 file and return genomic feature information.
    """

    gff_path = Path(gff_path)

    if not gff_path.exists():
        raise FileNotFoundError(f"GFF3 file not found: {gff_path}")

    features = []

    with gff_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):

            line = line.strip()

            # Ignore comments and blank lines
            if not line or line.startswith("#"):
                continue

            columns = line.split("\t")

            if len(columns) != 9:
                raise ValueError(
                    f"Invalid GFF3 format at line {line_number}: "
                    f"expected 9 columns, found {len(columns)}"
                )

            (
                seqid,
                source,
                feature_type,
                start,
                end,
                score,
                strand,
                phase,
                attributes,
            ) = columns

            features.append(
                {
                    "sequence_id": seqid,
                    "source": source,
                    "feature_type": feature_type,
                    "start": int(start),
                    "end": int(end),
                    "score": score,
                    "strand": strand,
                    "phase": phase,
                    "attributes": attributes,
                }
            )

    return features