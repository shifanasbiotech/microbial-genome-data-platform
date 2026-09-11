# P3 — Microbial Genome Data Platform

## Overview

A Python-based microbial genome data platform for ingesting, validating,
storing, querying, and summarising RefSeq microbial genome assemblies.

## Implemented

- NCBI RefSeq genome ingestion
- Genomic FASTA parsing
- GFF3 annotation parsing
- Genome and annotation quality-control checks
- SQLite relational data storage
- Batch ingestion of multiple microbial assemblies
- Indexed/queryable genome metadata
- Replicon and feature retrieval
- Command-line query interface
- TSV analysis outputs
- Automated tests with pytest
- Reproducible Linux/WSL workflow
- Real NCBI RefSeq datasets

## Multi-genome validation dataset

Three RefSeq assemblies are currently used for development validation:

- GCF_000005845.2
- GCF_000008865.2
- GCF_000009045.1

The platform successfully ingests all three assemblies into a single
SQLite database.

## Software stack

Python, Biopython, pandas, SQLite, pytest, Bash, Linux/WSL, Git.

## Data flow

NCBI RefSeq
→ FASTA/GFF3
→ parsing
→ validation/QC
→ relational SQLite storage
→ SQL/query interface
→ analysis summaries

## Reproducibility

The genome accession list is stored in:

`data/metadata/accessions.txt`

The multi-genome build is reproducible using:

`python scripts/build_platform.py`

Tests are executed with:

`pytest -q`

## Scope

This project focuses on microbial genome resource ingestion and analysis.
Production workflow orchestration and columnar data storage are addressed
separately in the subsequent Nextflow/Parquet project.
