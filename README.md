# Microbial Genome Data Platform

A reproducible Python-based platform for ingesting, validating, storing, querying, and performing quality control on microbial genome resources from NCBI RefSeq.

## Project Overview

This project demonstrates a production-oriented approach to handling structured microbial genome resources at scale.

The platform currently ingests multiple NCBI RefSeq microbial assemblies, parses genomic FASTA and GFF3 data, validates genome and annotation records, stores structured information in SQLite, and exposes query functionality through both Python APIs and a command-line interface.

## Architecture

```text
NCBI RefSeq
    │
    ▼
Genome accession list
    │
    ▼
NCBI Datasets
    │
    ├── FASTA
    ├── GFF3
    └── Metadata
    │
    ▼
Python ingestion layer
    │
    ├── FASTA parsing
    ├── GFF3 parsing
    └── metadata extraction
    │
    ▼
Validation & QC
    │
    ├── sequence validation
    ├── coordinate validation
    ├── feature statistics
    └── genome-level QC
    │
    ▼
SQLite relational database
    │
    ├── genomes
    ├── replicons
    └── features
    │
    ▼
Query layer + CLI
    │
    ├── genome queries
    ├── replicon queries
    └── feature queries
    │
    ▼
QC reports & analysis outputs
