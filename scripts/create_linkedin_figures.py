from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------------------------------------------------------
# Microbial Genome Data Platform
# LinkedIn / GitHub project visualisation script
# ---------------------------------------------------------

OUTPUT = Path("reports/figures")
OUTPUT.mkdir(parents=True, exist_ok=True)

# Verified results from the completed P3 analysis
assemblies = [
    "GCF_000005845.2",
    "GCF_000008865.2",
    "GCF_000009045.1",
]

genome_bp = [
    4_641_652,
    5_594_605,
    4_215_606,
]

contigs = [1, 3, 1]

feature_counts = [
    9_523,
    11_058,
    9_288,
]

# E. coli K-12 MG1655 feature distribution
feature_types = [
    "gene",
    "CDS",
    "exon",
    "pseudogene",
    "ncRNA",
    "tRNA",
    "mobile_genetic_element",
    "sequence_feature",
    "rRNA",
    "origin_of_replication",
    "region",
]

feature_values = [
    4506,
    4340,
    216,
    145,
    108,
    86,
    50,
    48,
    22,
    1,
    1,
]

# =========================================================
# 1. Genome Dataset Comparison
# =========================================================

fig, ax = plt.subplots(figsize=(11, 6.5))

bars = ax.bar(
    assemblies,
    [x / 1_000_000 for x in genome_bp]
)

ax.set_title(
    "Microbial Genome Dataset Comparison",
    fontsize=18,
    fontweight="bold"
)

ax.set_ylabel("Genome size (Mb)")
ax.set_xlabel("NCBI RefSeq assembly")

ax.grid(
    axis="y",
    alpha=0.2
)

for i, bar in enumerate(bars):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.08,
        f"{genome_bp[i] / 1_000_000:.2f} Mb\n"
        f"{feature_counts[i]:,} features",
        ha="center",
        va="bottom",
        fontsize=10
    )

ax.text(
    0.5,
    -0.18,
    "3 microbial genomes • 5 replicons/contigs • 14,451,863 bp • 29,869 annotated features",
    transform=ax.transAxes,
    ha="center",
    fontsize=10
)

fig.tight_layout()

fig.savefig(
    OUTPUT / "genome_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# =========================================================
# 2. Genomic Feature Landscape
# =========================================================

order = sorted(
    zip(feature_types, feature_values),
    key=lambda x: x[1]
)

labels = [x[0] for x in order]
values = [x[1] for x in order]

fig, ax = plt.subplots(figsize=(11, 7))

bars = ax.barh(
    labels,
    values
)

ax.set_title(
    "E. coli K-12 MG1655 — Genomic Feature Landscape",
    fontsize=18,
    fontweight="bold"
)

ax.set_xlabel("Feature count")

ax.grid(
    axis="x",
    alpha=0.2
)

for bar, value in zip(bars, values):
    ax.text(
        value + 40,
        bar.get_y() + bar.get_height() / 2,
        f"{value:,}",
        va="center",
        fontsize=9
    )

ax.text(
    0,
    -0.14,
    "Assembly: GCF_000005845.2 • 9,523 features • 11 feature types",
    transform=ax.transAxes,
    fontsize=10
)

fig.tight_layout()

fig.savefig(
    OUTPUT / "feature_landscape.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# =========================================================
# 3. Quality Control Summary
# =========================================================

qc_labels = [
    "Sequences",
    "Invalid sequences",
    "Features",
    "Invalid coordinates",
    "Feature types",
]

qc_values = [
    1,
    0,
    9523,
    0,
    11,
]

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(
    qc_labels,
    qc_values
)

ax.set_title(
    "Genome Quality-Control Summary",
    fontsize=18,
    fontweight="bold"
)

ax.set_ylabel("Count")

ax.grid(
    axis="y",
    alpha=0.2
)

for bar, value in zip(bars, qc_values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + max(qc_values) * 0.015,
        f"{value:,}",
        ha="center",
        fontsize=10
    )

ax.text(
    0.5,
    -0.17,
    "E. coli K-12 MG1655 • GCF_000005845.2 • 4,641,652 bp • 0 invalid sequences • 0 invalid coordinates",
    transform=ax.transAxes,
    ha="center",
    fontsize=9
)

fig.tight_layout()

fig.savefig(
    OUTPUT / "qc_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# =========================================================
# 4. Platform Architecture
# =========================================================

fig, ax = plt.subplots(figsize=(13, 7))

ax.set_xlim(0, 13)
ax.set_ylim(0, 8)
ax.axis("off")

ax.set_title(
    "Microbial Genome Data Platform — Workflow",
    fontsize=20,
    fontweight="bold",
    pad=20
)

nodes = [
    (0.5, 5.5, 2.0, 1.0, "NCBI RefSeq\nData"),
    (3.0, 5.5, 2.0, 1.0, "Genome\nIngestion"),
    (5.5, 5.5, 2.0, 1.0, "FASTA / GFF3\nParsing"),
    (8.0, 5.5, 2.0, 1.0, "Validation\n& QC"),
    (10.5, 5.5, 2.0, 1.0, "SQLite\nDatabase"),
    (3.0, 2.8, 2.3, 1.0, "Genome / Replicon /\nFeature Queries"),
    (6.0, 2.8, 2.3, 1.0, "Analysis\nOutputs"),
    (9.0, 2.8, 2.3, 1.0, "QC Reports /\nSummary Tables"),
]

for x, y, w, h, label in nodes:
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.03",
        linewidth=1.5,
        fill=False
    )

    ax.add_patch(box)

    ax.text(
        x + w / 2,
        y + h / 2,
        label,
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold"
    )

arrows = [
    ((2.5, 6.0), (3.0, 6.0)),
    ((5.0, 6.0), (5.5, 6.0)),
    ((7.5, 6.0), (8.0, 6.0)),
    ((10.0, 6.0), (10.5, 6.0)),
    ((11.5, 5.5), (4.2, 3.8)),
    ((5.3, 3.3), (6.0, 3.3)),
    ((8.3, 3.3), (9.0, 3.3)),
]

for start, end in arrows:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="->",
            mutation_scale=15,
            linewidth=1.5
        )
    )

ax.text(
    6.5,
    1.25,
    "Python • Biopython • Pandas • SQLite • NCBI Datasets CLI • pytest • Linux/WSL • Git/GitHub",
    ha="center",
    fontsize=11
)

ax.text(
    6.5,
    0.75,
    "Reproducible multi-genome bioinformatics data workflow",
    ha="center",
    fontsize=12,
    fontweight="bold"
)

fig.tight_layout()

fig.savefig(
    OUTPUT / "platform_workflow.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

print()
print("==============================================")
print("LINKEDIN FIGURES CREATED SUCCESSFULLY")
print("==============================================")
print()
print("Created:")
print("  reports/figures/genome_comparison.png")
print("  reports/figures/feature_landscape.png")
print("  reports/figures/qc_summary.png")
print("  reports/figures/platform_workflow.png")
print()
print("All figures are generated programmatically with")
print("Python + Matplotlib from verified P3 project results.")
