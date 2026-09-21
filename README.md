# 🧬 Microbial Genome Data Platform

A reproducible bioinformatics data platform for ingesting, validating, storing, and querying microbial genome assemblies and genome annotations from NCBI RefSeq.

The project combines Python-based biological data processing, FASTA/GFF3 parsing, genome quality-control checks, relational database design, multi-genome ingestion, command-line querying, automated testing, and reproducible project organization.

---

## Overview

Microbial genome resources contain large volumes of sequence and annotation data that need to be processed consistently before they can be used for downstream analysis.

This project implements a lightweight microbial genome data platform that converts publicly available NCBI RefSeq genome datasets into a structured, queryable relational database.

The workflow progresses from:

**NCBI RefSeq data acquisition → genome discovery → FASTA/GFF3 parsing → validation → quality control → relational database ingestion → multi-genome integration → query interface → structured analysis outputs**

The project demonstrates practical skills in:

- Microbial genome data processing
- Prokaryotic genome analysis
- FASTA and GFF3 parsing
- Genome and annotation quality control
- Relational database design
- Multi-genome data ingestion
- Python-based bioinformatics software development
- Command-line interface development
- Automated testing
- Linux/WSL computational environments
- Git/GitHub-based reproducible project organization

---

## Project Objectives

The main objectives of the platform are to:

- Acquire microbial genome assemblies from NCBI RefSeq
- Parse genome sequence and annotation files
- Validate genomic coordinates and sequence information
- Extract genome and feature-level metadata
- Perform genome quality-control analysis
- Store genome information in a relational SQLite database
- Support ingestion of multiple microbial genome assemblies
- Provide structured query functionality
- Generate reproducible summary outputs
- Provide automated tests for core parsing and QC functionality
- Maintain a modular and reproducible bioinformatics software structure

---

# Platform Workflow

```text
                    NCBI RefSeq
                         │
                         ▼
              NCBI Datasets Download
                         │
                         ▼
              Microbial Genome Data
                         │
                ┌────────┴────────┐
                ▼                 ▼
             FASTA              GFF3
                │                 │
                ▼                 ▼
        Sequence Parsing    Feature Parsing
                │                 │
                └────────┬────────┘
                         ▼
                  Validation / QC
                         │
                         ▼
                Metadata Extraction
                         │
                         ▼
                 Relational Model
                         │
                         ▼
                  SQLite Database
                         │
                         ▼
                  Query Interface
                         │
                         ▼
                Structured Outputs
```

---

# Data Source

The project uses publicly available microbial genome datasets obtained from:

**NCBI RefSeq**

Genome datasets were downloaded using the **NCBI Datasets command-line interface**.

The platform was validated using multiple RefSeq microbial genome assemblies rather than relying only on a single demonstration genome.

Downloaded raw NCBI datasets are intentionally excluded from Git version control and can be regenerated using the documented workflow.

---

# Validation Dataset

The multi-genome platform was validated using three NCBI RefSeq microbial genome assemblies.

| Assembly | Genome Size | Contigs / Replicons | Annotated Features |
|---|---:|---:|---:|
| GCF_000005845.2 | 4,641,652 bp | 1 | 9,523 |
| GCF_000008865.2 | 5,594,605 bp | 3 | 11,058 |
| GCF_000009045.1 | 4,215,606 bp | 1 | 9,288 |
| **Total** | **14,451,863 bp** | **5** | **29,869** |

These assemblies provide a multi-genome validation dataset for testing genome discovery, parsing, quality control, relational storage, querying, and summary generation.

---

# Analysis Stages

## 1. Genome Data Acquisition

The platform obtains microbial genome datasets from NCBI RefSeq using the NCBI Datasets command-line interface.

The downloaded datasets contain sequence and annotation information required for downstream processing.

The acquisition process is separated from the analysis and database layers so that source datasets can be regenerated independently.

---

## 2. Genome Discovery

The ingestion workflow automatically discovers available genome assemblies within the extracted NCBI dataset structure.

Assembly accessions are identified using the NCBI RefSeq accession pattern:

```text
GCF_*
```

This allows the build process to operate across multiple assemblies instead of relying on a single hard-coded genome.

---

## 3. FASTA Parsing

Genome sequence data are parsed from FASTA files.

The parser extracts sequence-level information required for downstream processing, including:

- Sequence identifiers
- Sequence lengths
- Genome sequence information
- Sequence counts
- Total genome size

Biological sequence processing is implemented in Python using Biopython.

---

## 4. GFF3 Parsing

Genome annotation information is parsed from GFF3 files.

The parser extracts structured genomic feature information including:

- Feature type
- Genomic coordinates
- Strand
- Sequence/replicon identifier
- Annotation attributes
- Feature identifiers where available

This converts the original annotation representation into structured records suitable for validation, storage, and querying.

---

## 5. Genome Validation

The platform performs validation checks during processing to identify potentially invalid genome or annotation records.

Validation includes:

- Sequence validity checks
- Coordinate validation
- Feature record validation
- Sequence-length consistency
- Feature counting
- Feature-type characterization

Invalid sequence and coordinate counts are recorded as part of the QC output.

---

# Quality Control

A dedicated QC layer evaluates genome and annotation information during processing.

The QC framework calculates:

- Number of sequences
- Total sequence length
- Invalid sequences
- Total feature count
- Number of feature types
- Invalid genomic coordinates
- Most common feature types

---

## Example QC Result

The QC framework was validated using the *Escherichia coli* K-12 MG1655 RefSeq assembly.

```text
Assembly: GCF_000005845.2
Organism: Escherichia coli K-12 MG1655

sequence_count: 1
total_sequence_bp: 4641652
invalid_sequences: 0
feature_count: 9523
feature_types: 11
invalid_coordinates: 0
```

The QC implementation provides a reusable framework that can be applied to additional microbial genome assemblies.

---

# Relational Database

Processed genome information is stored in a relational SQLite database.

The database separates genome-level, replicon-level, and feature-level information to provide a structured representation of microbial genome resources.

Conceptually, the platform organizes information as:

```text
Genome
   │
   ├── Replicons / Sequences
   │
   └── Genomic Features
           │
           ├── Genes
           ├── CDS
           ├── Exons
           ├── ncRNA
           ├── tRNA
           ├── rRNA
           ├── Pseudogenes
           ├── Mobile genetic elements
           └── Other annotated feature types
```

This structure allows genome information to be queried independently from individual genomic features.

---

# Database Validation

The completed multi-genome build successfully loaded:

```text
Genomes:              3
Replicons / Contigs:  5
Total genome bases:   14,451,863 bp
Annotated features:   29,869
```

Genome-level records validated in the database include:

```text
GCF_000005845.2
Genome size: 4,641,652 bp
Contigs: 1
Features: 9,523

GCF_000008865.2
Genome size: 5,594,605 bp
Contigs: 3
Features: 11,058

GCF_000009045.1
Genome size: 4,215,606 bp
Contigs: 1
Features: 9,288
```

---

# Feature-Level Data

The platform preserves detailed annotation information rather than storing only genome-level summaries.

For the *E. coli* K-12 MG1655 assembly, the ingested annotation contains **9,523 genomic features across 11 feature types**.

Representative feature categories include:

```text
gene
CDS
exon
pseudogene
ncRNA
tRNA
mobile_genetic_element
sequence_feature
rRNA
origin_of_replication
region
```

This enables feature-level inspection through the query layer.

---

# Query Interface

The project includes a command-line query interface for retrieving information from the platform database.

The CLI provides commands for:

- Genome-level records
- Replicon information
- Genomic feature records
- Feature-type filtering
- Structured JSON output

---

## Example: Query a Genome

```bash
python -m microbial_genome_platform.cli genome GCF_000005845.2
```

Example information returned includes:

```text
Assembly accession
Organism
Genome size
Contig count
Feature count
```

---

## Example: Query Replicons

```bash
python -m microbial_genome_platform.cli replicons GCF_000005845.2
```

Example result:

```text
NC_000913.3
Length: 4641652 bp
GC: 50.791%
```

---

## Example: Query Features

```bash
python -m microbial_genome_platform.cli features GCF_000005845.2
```

The command returns structured feature-level records derived from the GFF3 annotation.

Feature retrieval can also be filtered by feature type through the query layer.

---

# Multi-Genome Ingestion

A major component of the platform is the transition from single-genome processing to multi-genome ingestion.

Instead of hard-coding one genome, the build workflow:

1. Discovers available NCBI genome assemblies
2. Identifies assembly accessions
3. Locates sequence and annotation files
4. Parses each assembly
5. Performs validation
6. Loads genome metadata
7. Loads replicon information
8. Loads genomic features
9. Builds the relational database
10. Generates summary tables

This provides a foundation for extending the platform to larger microbial genome collections.

---

# Build Workflow

The main platform build script is:

```text
scripts/build_platform.py
```

The build process discovers available genome assemblies and rebuilds the SQLite database from the source datasets.

The workflow is:

```text
Discover assemblies
        ↓
Parse FASTA
        ↓
Parse GFF3
        ↓
Validate records
        ↓
Extract metadata
        ↓
Calculate QC information
        ↓
Load relational database
        ↓
Generate summary tables
```

---

# Generated Outputs

The platform produces structured outputs for downstream inspection.

Representative output organization:

```text
results/
├── qc/
│   └── GCF_000005845.2_qc.txt
│
└── queries/
    ├── genome_summary.tsv
    └── feature_summary.tsv
```

The generated SQLite database is created locally during the build process and is intentionally excluded from version control.

Downloaded raw datasets are also excluded from Git to keep the repository lightweight.

---

# Automated Testing

The project includes automated tests for core parsing and quality-control functionality.

Testing is implemented using:

```text
pytest
```

The current test suite successfully passes:

```text
3 passed
```

The tests provide regression protection for important data-processing components, particularly biological data parsing and QC functionality.

---

# Reproducibility

Reproducibility is a central design principle of the project.

The workflow separates:

- Raw input datasets
- Processing scripts
- Source code
- Generated databases
- Analysis outputs
- Tests
- Documentation

Raw NCBI datasets and generated SQLite database files are excluded from Git version control.

The database can be regenerated locally from the downloaded RefSeq datasets using the documented build workflow.

This separation keeps the repository manageable while preserving a reproducible computational workflow.

---

# Repository Structure

```text
microbial-genome-data-platform/
│
├── data/
│   ├── metadata/
│   │   └── accessions.txt
│   ├── raw/
│   │   └── NCBI genome datasets
│   └── processed/
│
├── docs/
│
├── reports/
│
├── results/
│   ├── qc/
│   └── queries/
│
├── scripts/
│   ├── build_platform.py
│   └── query_platform.py
│
├── src/
│   └── microbial_genome_platform/
│       ├── __init__.py
│       ├── cli.py
│       ├── database.py
│       ├── ingest.py
│       ├── parsers.py
│       ├── qc.py
│       ├── queries.py
│       └── schema.py
│
├── tests/
│   ├── test_parsers.py
│   └── test_qc.py
│
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

# Core Components

## `parsers.py`

Responsible for parsing biological sequence and annotation information from input datasets.

Key responsibilities include:

- FASTA parsing
- GFF3 parsing
- Sequence record extraction
- Feature record extraction
- Structured representation of biological data

---

## `ingest.py`

Handles integration of parsed genome information into the relational database.

The ingestion layer connects the biological parsing layer with the database representation.

---

## `schema.py`

Defines the relational database structure used to represent:

- Genomes
- Replicons
- Genomic features

---

## `database.py`

Provides database connectivity and database-level operations used by the platform.

---

## `qc.py`

Implements genome and annotation quality-control calculations.

The QC module evaluates:

- Sequence counts
- Genome size
- Invalid sequences
- Feature counts
- Feature types
- Coordinate validity

---

## `queries.py`

Provides structured access to stored genome information.

The query layer supports retrieval of:

- Genome records
- Replicon records
- Feature records

---

## `cli.py`

Provides a command-line interface for interacting with the platform.

This allows users to inspect stored genome information without directly writing SQL queries.

---

## `build_platform.py`

Provides the reproducible multi-genome build workflow.

It discovers available assemblies, processes the input data, rebuilds the database, and produces summary outputs.

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Platform development and biological data processing |
| Biopython | Biological sequence processing |
| Pandas | Structured data processing and summary analysis |
| SQLite | Relational genome data storage |
| GFF3 | Genome annotation input |
| FASTA | Genome sequence input |
| NCBI RefSeq | Source genome data |
| NCBI Datasets CLI | Genome dataset acquisition |
| Pytest | Automated testing |
| Bash | Command-line workflow execution |
| Linux / WSL | Bioinformatics development environment |
| Git | Version control |
| GitHub | Repository management and project sharing |

---

# Skills Demonstrated

This project demonstrates hands-on experience with:

- Microbial genome data processing
- Prokaryotic genome analysis
- FASTA sequence processing
- GFF3 annotation parsing
- Genome annotation data modelling
- Genome quality control
- Biological data validation
- Relational database design
- SQLite database development
- Multi-genome ingestion
- Python software development
- Command-line interface development
- Automated testing with pytest
- Linux / WSL environments
- NCBI RefSeq datasets
- NCBI Datasets CLI
- Structured biological data processing
- Reproducible computational workflows
- Git and GitHub
- Technical documentation

---

# Validation Results

The platform was validated through automated testing and real NCBI RefSeq microbial genome datasets.

## Dataset Validation

```text
Assemblies processed:       3
Total genome sequence:      14,451,863 bp
Total replicons / contigs:  5
Total genomic features:     29,869
```

## Software Validation

```text
Automated tests:             3 passed
```

## Example Genome QC

```text
Assembly:                    GCF_000005845.2
Sequence count:              1
Genome size:                 4,641,652 bp
Invalid sequences:           0
Feature count:               9,523
Feature types:               11
Invalid coordinates:         0
```

These results demonstrate that the platform can process real RefSeq microbial genome data and preserve genome- and feature-level information in a structured database.

---

# Design Principles

The project was designed around several practical bioinformatics software principles.

### Reproducibility

The same source datasets and build workflow can be used to regenerate the database.

### Modularity

Parsing, ingestion, QC, database management, querying, and CLI functionality are separated into distinct modules.

### Validation

Input sequence and annotation records are checked before being incorporated into the platform.

### Multi-Genome Support

The ingestion workflow discovers and processes multiple genome assemblies rather than relying on a single hard-coded genome.

### Testability

Core parsing and QC functionality is covered by automated tests.

### Maintainability

The repository uses structured Python modules, clear separation of responsibilities, Git version control, and technical documentation.

---

# Current Scope

The current implementation focuses on:

- Microbial genome ingestion
- NCBI RefSeq datasets
- FASTA/GFF3 processing
- Genome and annotation QC
- Relational SQLite storage
- Multi-genome integration
- Queryable genome data
- Automated testing
- Reproducible local data builds

The project intentionally focuses on the genome data ingestion and platform layer.

Workflow orchestration technologies and large-scale columnar data processing are treated as separate capabilities in subsequent portfolio work rather than being claimed as part of this project.

---

# Future Extensions

Potential future extensions include:

- Larger microbial genome collections
- PostgreSQL-based deployment
- Workflow orchestration with Nextflow or Snakemake
- Apache Parquet-based data storage
- Expanded genome QC reporting
- Additional annotation resources
- Genome comparison functionality
- Cloud-based deployment
- Containerized execution
- Larger-scale production data ingestion
- Integration with genome-browser resources

These are planned extensions and are **not part of the current implementation**.

---

# Project Status

**Completed portfolio project.**

The platform has been implemented, tested, validated using multiple real NCBI RefSeq microbial genome assemblies, and organized as a public GitHub repository.

The current implementation includes:

- Multi-genome ingestion
- FASTA/GFF3 parsing
- Genome QC
- Relational SQLite storage
- Query functionality
- Automated tests
- Reproducible build scripts
- Structured result outputs
- Technical documentation

---

# License

This project is licensed under the MIT License. See the `LICENSE` file for details.

See `LICENSE` for details.

---

## Author

**Shifa Anas**
