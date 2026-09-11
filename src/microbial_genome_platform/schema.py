SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS genomes (
    genome_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assembly_accession TEXT UNIQUE NOT NULL,
    organism_name TEXT,
    assembly_name TEXT,
    assembly_level TEXT,
    genome_size_bp INTEGER,
    contig_count INTEGER,
    total_features INTEGER,
    source TEXT DEFAULT 'NCBI RefSeq'
);

CREATE TABLE IF NOT EXISTS replicons (
    replicon_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genome_id INTEGER NOT NULL,
    sequence_id TEXT NOT NULL,
    length_bp INTEGER NOT NULL,
    gc_percent REAL,
    FOREIGN KEY (genome_id) REFERENCES genomes(genome_id),
    UNIQUE(genome_id, sequence_id)
);

CREATE TABLE IF NOT EXISTS features (
    feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genome_id INTEGER NOT NULL,
    sequence_id TEXT NOT NULL,
    feature_type TEXT NOT NULL,
    start INTEGER NOT NULL,
    end INTEGER NOT NULL,
    strand TEXT,
    source TEXT,
    attributes TEXT,
    FOREIGN KEY (genome_id) REFERENCES genomes(genome_id)
);

CREATE INDEX IF NOT EXISTS idx_genomes_accession
    ON genomes(assembly_accession);

CREATE INDEX IF NOT EXISTS idx_features_genome
    ON features(genome_id);

CREATE INDEX IF NOT EXISTS idx_features_type
    ON features(feature_type);

CREATE INDEX IF NOT EXISTS idx_features_sequence
    ON features(sequence_id);
"""
