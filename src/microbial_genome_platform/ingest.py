from pathlib import Path
import json
import re

from .parsers import parse_fasta, parse_gff3
from .database import GenomeDatabase
from .qc import genome_qc


def accession_from_path(path: Path) -> str:
    """Extract assembly accession from a dataset directory."""
    match = re.search(r"(GC[AF]_\d+\.\d+)", str(path))
    if not match:
        raise ValueError(f"Unable to determine accession from {path}")
    return match.group(1)


def locate_files(dataset_root: str):
    """Locate downloaded FASTA/GFF3 files recursively."""
    root = Path(dataset_root)

    fasta_files = sorted(root.rglob("*_genomic.fna"))
    gff_files = sorted(root.rglob("*.gff"))

    return fasta_files, gff_files


def ingest_dataset(dataset_root: str, database_path: str):
    """Ingest all available NCBI genome packages."""
    fasta_files, gff_files = locate_files(dataset_root)

    gff_by_accession = {
        accession_from_path(path): path
        for path in gff_files
    }

    db = GenomeDatabase(database_path)
    summaries = []

    for fasta_path in fasta_files:
        accession = accession_from_path(fasta_path)

        if accession not in gff_by_accession:
            continue

        gff_path = gff_by_accession[accession]

        sequences = parse_fasta(fasta_path)
        features = parse_gff3(gff_path)

        qc = genome_qc(sequences, features)

        genome_id = db.insert_genome(
            accession=accession,
            organism_name=accession,
            assembly_name=accession,
            assembly_level="NCBI RefSeq",
            genome_size_bp=qc["total_sequence_bp"],
            contig_count=qc["sequence_count"],
            total_features=qc["feature_count"],
        )

        db.insert_replicons(genome_id, sequences)
        db.insert_features(genome_id, features)

        summaries.append({
            "assembly_accession": accession,
            **qc,
        })

    db.close()

    return summaries


def save_qc_report(summaries, output_path):
    """Write machine-readable QC results."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w") as handle:
        json.dump(summaries, handle, indent=2)
