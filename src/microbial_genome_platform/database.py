import sqlite3
from pathlib import Path

from .schema import SCHEMA


class GenomeDatabase:
    """SQLite-backed genomic resource database."""

    def __init__(self, path: str = "results/microbial_genomes.sqlite"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript(SCHEMA)

    def insert_genome(
        self,
        accession,
        organism_name,
        assembly_name,
        assembly_level,
        genome_size_bp,
        contig_count,
        total_features,
    ):
        cursor = self.connection.execute(
            """
            INSERT OR REPLACE INTO genomes (
                assembly_accession,
                organism_name,
                assembly_name,
                assembly_level,
                genome_size_bp,
                contig_count,
                total_features
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                accession,
                organism_name,
                assembly_name,
                assembly_level,
                genome_size_bp,
                contig_count,
                total_features,
            ),
        )

        self.connection.commit()

        row = self.connection.execute(
            "SELECT genome_id FROM genomes WHERE assembly_accession = ?",
            (accession,),
        ).fetchone()

        return row[0]

    def insert_replicons(self, genome_id, records):
        self.connection.executemany(
            """
            INSERT OR REPLACE INTO replicons (
                genome_id,
                sequence_id,
                length_bp,
                gc_percent
            )
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    genome_id,
                    r["sequence_id"],
                    r["length_bp"],
                    r["gc_percent"],
                )
                for r in records
            ],
        )

        self.connection.commit()

    def insert_features(self, genome_id, records):
        self.connection.executemany(
            """
            INSERT INTO features (
                genome_id,
                sequence_id,
                feature_type,
                start,
                end,
                strand,
                source,
                attributes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    genome_id,
                    r["sequence_id"],
                    r["feature_type"],
                    r["start"],
                    r["end"],
                    r["strand"],
                    r["source"],
                    r["attributes"],
                )
                for r in records
            ],
        )

        self.connection.commit()

    def query(self, sql, parameters=()):
        return self.connection.execute(sql, parameters).fetchall()

    def close(self):
        self.connection.close()
