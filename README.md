# Genome Analysis & Visualization Pipeline

A reproducible bioinformatics pipeline for processing, validating,
annotating, and preparing genome-scale datasets for downstream
genomic analysis and genome-browser visualization.

## Project objectives

- Process genome sequence and annotation files
- Validate FASTA and GFF3 genomic data
- Extract genome-level and feature-level statistics
- Integrate genomic metadata
- Generate analysis-ready BED/TSV outputs
- Produce quality-control reports
- Prepare datasets for genome-browser inspection
- Demonstrate reproducible Linux/Python bioinformatics workflows

## Technologies

Python • Linux/WSL • Biopython • pandas • GFF3 • FASTA • BED
• genomic QC • data validation • reproducible pipelines
• genome visualization workflows

## Planned workflow

Raw genomic data
        ↓
Input validation
        ↓
FASTA/GFF3 parsing
        ↓
Genome statistics
        ↓
Feature extraction
        ↓
QC and validation
        ↓
Browser-ready genomic tracks
        ↓
Automated report

## Status

Project under active development.

## Multi-genome ingestion

The platform supports batch ingestion of multiple NCBI RefSeq microbial
assemblies from an accession list. The current validation dataset contains
three assemblies and stores genome metadata, replicons, and GFF3-derived
features in SQLite.

### Reproducible build

```bash
PYTHONPATH=. python scripts/build_platform.py


