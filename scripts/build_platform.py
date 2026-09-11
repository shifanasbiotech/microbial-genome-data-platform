#!/usr/bin/env python3

from pathlib import Path
import csv
import shutil

from src.microbial_genome_platform.ingest import ingest_dataset
from src.microbial_genome_platform.database import GenomeDatabase

DATASET_ROOT = Path("data/raw/multi_genome/ncbi_dataset/data")
DATABASE = "results/microbial_genomes.sqlite"


def main():
    print("\n=== MICROBIAL GENOME DATA PLATFORM ===\n")

    assemblies = sorted(
        p for p in DATASET_ROOT.iterdir()
        if p.is_dir() and p.name.startswith("GCF_")
    )

    if not assemblies:
        raise RuntimeError(f"No genome assemblies found in {DATASET_ROOT}")

    print(f"Assemblies discovered: {len(assemblies)}")
    for assembly in assemblies:
        print(f"  - {assembly.name}")

    db_path = Path(DATABASE)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        db_path.unlink()

    all_summaries = []

    for assembly in assemblies:
        print(f"\n--- Ingesting {assembly.name} ---")
        summary = ingest_dataset(str(assembly), DATABASE)
        all_summaries.append(summary)

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

    Path("results/queries").mkdir(parents=True, exist_ok=True)

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

    print("\n=== BUILD SUMMARY ===")
    print(f"Genomes loaded: {len(genome_summary)}")
    print(f"Database: {DATABASE}")
    print(f"Genome summary: {len(genome_summary)} records")
    print(f"Feature types: {len(feature_summary)}")

    print("\nLoaded assemblies:")
    for row in genome_summary:
        print(f"  {row[0]}")

    print("\nPlatform build complete.")


if __name__ == "__main__":
    main()
