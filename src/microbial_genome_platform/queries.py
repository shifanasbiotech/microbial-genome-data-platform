from .database import GenomeDatabase


class GenomeQueries:
    """Read-only query interface for the microbial genome database."""

    def __init__(self, database_path: str = "results/microbial_genomes.sqlite"):
        self.db = GenomeDatabase(database_path)

    def list_genomes(self):
        return self.db.query(
            """
            SELECT
                genome_id,
                assembly_accession,
                organism_name,
                assembly_name,
                assembly_level,
                genome_size_bp,
                contig_count,
                total_features,
                source
            FROM genomes
            ORDER BY assembly_accession
            """
        )

    def get_genome(self, accession: str):
        return self.db.query(
            """
            SELECT
                genome_id,
                assembly_accession,
                organism_name,
                assembly_name,
                assembly_level,
                genome_size_bp,
                contig_count,
                total_features,
                source
            FROM genomes
            WHERE assembly_accession = ?
            """,
            (accession,),
        )

    def get_replicons(self, accession: str):
        return self.db.query(
            """
            SELECT
                r.sequence_id,
                r.length_bp,
                r.gc_percent
            FROM replicons r
            JOIN genomes g ON r.genome_id = g.genome_id
            WHERE g.assembly_accession = ?
            ORDER BY r.sequence_id
            """,
            (accession,),
        )

    def get_features(self, accession: str, feature_type: str | None = None):
        if feature_type:
            return self.db.query(
                """
                SELECT
                    f.sequence_id,
                    f.feature_type,
                    f.start,
                    f.end,
                    f.strand,
                    f.source,
                    f.attributes
                FROM features f
                JOIN genomes g ON f.genome_id = g.genome_id
                WHERE g.assembly_accession = ?
                  AND f.feature_type = ?
                ORDER BY f.sequence_id, f.start
                """,
                (accession, feature_type),
            )

        return self.db.query(
            """
            SELECT
                f.sequence_id,
                f.feature_type,
                f.start,
                f.end,
                f.strand,
                f.source,
                f.attributes
            FROM features f
            JOIN genomes g ON f.genome_id = g.genome_id
            WHERE g.assembly_accession = ?
            ORDER BY f.sequence_id, f.start
            """,
            (accession,),
        )

    def close(self):
        self.db.close()
