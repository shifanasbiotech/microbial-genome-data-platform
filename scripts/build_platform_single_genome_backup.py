#!/usr/bin/env python3

from pathlib import Path
import csv

from src.microbial_genome_platform.ingest import (
    ingest_dataset,
    save_qc_report,
)
from src.microbial_genome_platform.database import GenomeDatabase


DATASET = "data/raw/ecoli_k12/ncbi_dataset"
DATABASE = "results/microbial_genomes.sqlite"


def main():
    print("\n=== MICROBIAL GENOME DATA PLATFORM ===\n")

    summaries = ingest_dataset(DATASET, DATABASE)

    save_qc_report(
        summaries,
        "results/qc/genome_qc.json",
    )

    db = GenomeDatabase(DATABASE)

    genome_summary = db.query(
        """
        SELECT
            assembly_accession,
            genome_size_bp,
            contig_count,
            total_features
        FROM genomes
        ORDER BY genome_size_bp DESC
        """
    )

    feature_summary = db.query(
        """
        SELECT
            feature_type,
            COUNT(*) AS feature_count
        FROM features
        GROUP BY feature_type
        ORDER BY feature_count DESC
        """
    )

    db.close()

    with open(
        "results/queries/genome_summary.tsv",
        "w",
        newline="",
    ) as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow([
            "assembly_accession",
            "genome_size_bp",
            "contig_count",
            "total_features",
        ])
        writer.writerows(genome_summary)

    with open(
        "results/queries/feature_summary.tsv",
        "w",
        newline="",
    ) as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["feature_type", "feature_count"])
        writer.writerows(feature_summary)

    print(f"Genomes loaded: {len(summaries)}")
    print(f"Database: {DATABASE}")
    print(f"Genome summary: {len(genome_summary)} records")
    print(f"Feature types: {len(feature_summary)}")
    print("\nPlatform build complete.")


if __name__ == "__main__":
    main()
