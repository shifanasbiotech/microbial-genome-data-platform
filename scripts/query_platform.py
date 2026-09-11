#!/usr/bin/env python3

import argparse

from src.microbial_genome_platform.database import GenomeDatabase


def main():
    parser = argparse.ArgumentParser(
        description="Query the microbial genome database."
    )

    parser.add_argument(
        "--feature",
        help="Return features of a specific GFF3 type."
    )

    parser.add_argument(
        "--assembly",
        help="Return records for a specific assembly accession."
    )

    args = parser.parse_args()

    db = GenomeDatabase("results/microbial_genomes.sqlite")

    if args.feature:
        rows = db.query(
            """
            SELECT
                g.assembly_accession,
                f.sequence_id,
                f.feature_type,
                f.start,
                f.end,
                f.strand
            FROM features f
            JOIN genomes g
              ON f.genome_id = g.genome_id
            WHERE f.feature_type = ?
            LIMIT 50
            """,
            (args.feature,),
        )

    elif args.assembly:
        rows = db.query(
            """
            SELECT
                assembly_accession,
                organism_name,
                genome_size_bp,
                contig_count,
                total_features
            FROM genomes
            WHERE assembly_accession = ?
            """,
            (args.assembly,),
        )

    else:
        rows = db.query(
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

    db.close()

    for row in rows:
        print("\t".join(map(str, row)))


if __name__ == "__main__":
    main()
