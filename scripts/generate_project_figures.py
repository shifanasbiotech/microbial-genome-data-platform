from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BASE = Path(__file__).resolve().parents[1]
DB = BASE / "results" / "microbial_genomes.sqlite"
OUT = BASE / "reports" / "figures"

OUT.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)

# =========================================================
# ACTUAL P3 DATABASE SCHEMA
# =========================================================

genomes = conn.execute("""
    SELECT
        genome_id,
        assembly_accession,
        organism_name,
        genome_size_bp,
        contig_count,
        total_features
    FROM genomes
    ORDER BY assembly_accession
""").fetchall()

if not genomes:
    raise RuntimeError("No genome records found.")

print("\n=== VERIFIED GENOME DATA ===")

for row in genomes:
    print(
        f"{row[1]} | {row[2]} | "
        f"{row[3]:,} bp | "
        f"{row[4]} contigs | "
        f"{row[5]:,} features"
    )

# =========================================================
# FIGURE 1 — GENOME SIZE COMPARISON
# Uses genomes.genome_size_bp directly
# =========================================================

accessions = [r[1] for r in genomes]
sizes_mb = [r[3] / 1_000_000 for r in genomes]
feature_counts = [r[5] for r in genomes]
contigs = [r[4] for r in genomes]

fig, ax = plt.subplots(figsize=(11, 6))

bars = ax.bar(accessions, sizes_mb)

ax.set_title(
    "Microbial Genome Data Platform\nGenome Size Comparison",
    fontsize=17,
    fontweight="bold"
)

ax.set_xlabel("NCBI RefSeq Assembly")
ax.set_ylabel("Genome Size (Mb)")
ax.grid(axis="y", alpha=0.2)

for bar, size, features, contig_count in zip(
    bars,
    sizes_mb,
    feature_counts,
    contigs
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        f"{size:.2f} Mb\n"
        f"{features:,} features • "
        f"{contig_count} contig{'s' if contig_count != 1 else ''}",
        ha="center",
        va="bottom",
        fontsize=9
    )

fig.tight_layout()

fig1 = OUT / "01_genome_size_comparison.png"
fig.savefig(fig1, dpi=220, bbox_inches="tight")
plt.close(fig)

# =========================================================
# FIGURE 2 — E. COLI FEATURE DISTRIBUTION
# Join features -> genomes using genome_id
# =========================================================

ecoli_genome_id = next(
    r[0]
    for r in genomes
    if r[1] == "GCF_000005845.2"
)

feature_rows = conn.execute("""
    SELECT
        feature_type,
        COUNT(*)
    FROM features
    WHERE genome_id = ?
    GROUP BY feature_type
    ORDER BY COUNT(*) ASC
""", (ecoli_genome_id,)).fetchall()

if not feature_rows:
    raise RuntimeError("No E. coli feature records found.")

feature_labels = [str(r[0]) for r in feature_rows]
feature_values = [int(r[1]) for r in feature_rows]

fig, ax = plt.subplots(figsize=(11, 7))

bars = ax.barh(
    feature_labels,
    feature_values
)

ax.set_title(
    "E. coli K-12 MG1655\nGenomic Feature Distribution",
    fontsize=17,
    fontweight="bold"
)

ax.set_xlabel("Feature Count")
ax.set_ylabel("Feature Type")
ax.grid(axis="x", alpha=0.2)

for bar, value in zip(bars, feature_values):
    ax.text(
        value + max(feature_values) * 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"{value:,}",
        va="center",
        fontsize=9
    )

ax.text(
    0,
    -0.12,
    "Assembly: GCF_000005845.2  |  "
    f"Total features: {sum(feature_values):,}  |  "
    f"Feature types: {len(feature_values)}",
    transform=ax.transAxes,
    fontsize=9
)

fig.tight_layout()

fig2 = OUT / "02_ecoli_feature_distribution.png"
fig.savefig(fig2, dpi=220, bbox_inches="tight")
plt.close(fig)

# =========================================================
# FIGURE 3 — PLATFORM DATASET SUMMARY
# Calculated from actual genomes table
# =========================================================

total_bp = sum(r[3] for r in genomes)
total_features = sum(r[5] for r in genomes)
total_contigs = sum(r[4] for r in genomes)

fig, ax = plt.subplots(figsize=(11, 6))
ax.axis("off")

ax.text(
    0.5,
    0.88,
    "Microbial Genome Data Platform",
    ha="center",
    fontsize=22,
    fontweight="bold"
)

ax.text(
    0.5,
    0.77,
    "Completed Multi-Genome Validation Dataset",
    ha="center",
    fontsize=13
)

metrics = [
    (str(len(genomes)), "RefSeq Genomes"),
    (f"{total_contigs:,}", "Replicons / Contigs"),
    (f"{total_bp:,}", "Total Sequence (bp)"),
    (f"{total_features:,}", "Annotated Features"),
]

positions = [0.12, 0.37, 0.62, 0.87]

for x, (value, label) in zip(positions, metrics):
    ax.text(
        x,
        0.53,
        value,
        ha="center",
        fontsize=22,
        fontweight="bold"
    )

    ax.text(
        x,
        0.42,
        label,
        ha="center",
        fontsize=10
    )

ax.text(
    0.5,
    0.17,
    "Python • Biopython • Pandas • SQLite • "
    "FASTA/GFF3 • NCBI Datasets CLI • pytest • Linux/WSL",
    ha="center",
    fontsize=10
)

fig.tight_layout()

fig3 = OUT / "03_platform_dataset_summary.png"
fig.savefig(fig3, dpi=220, bbox_inches="tight")
plt.close(fig)

# =========================================================
# FIGURE 4 — ACTUAL PLATFORM WORKFLOW
# Programmatically generated with Matplotlib
# =========================================================

fig, ax = plt.subplots(figsize=(14, 6))

ax.set_xlim(0, 14)
ax.set_ylim(0, 6)
ax.axis("off")

ax.text(
    7,
    5.45,
    "Microbial Genome Data Platform — Workflow",
    ha="center",
    fontsize=21,
    fontweight="bold"
)

steps = [
    ("1", "NCBI RefSeq", "Genome datasets"),
    ("2", "FASTA / GFF3", "Parsing"),
    ("3", "Validation & QC", "Sequence + features"),
    ("4", "SQLite", "Relational storage"),
    ("5", "CLI Queries", "Genome exploration"),
    ("6", "Analysis", "Reports + figures"),
]

x_positions = [0.3, 2.65, 5.0, 7.35, 9.7, 12.05]

for i, (number, title, description) in enumerate(steps):

    box = FancyBboxPatch(
        (x_positions[i], 2.35),
        1.65,
        1.45,
        boxstyle="round,pad=0.04",
        linewidth=1.5,
        fill=False
    )

    ax.add_patch(box)

    ax.text(
        x_positions[i] + 0.825,
        3.45,
        number,
        ha="center",
        fontsize=11,
        fontweight="bold"
    )

    ax.text(
        x_positions[i] + 0.825,
        3.05,
        title,
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

    ax.text(
        x_positions[i] + 0.825,
        2.65,
        description,
        ha="center",
        fontsize=8
    )

    if i < len(steps) - 1:

        arrow = FancyArrowPatch(
            (x_positions[i] + 1.68, 3.08),
            (x_positions[i + 1] - 0.05, 3.08),
            arrowstyle="->",
            mutation_scale=14,
            linewidth=1.4
        )

        ax.add_patch(arrow)

ax.text(
    7,
    1.45,
    f"{len(genomes)} genomes  •  "
    f"{total_contigs} replicons/contigs  •  "
    f"{total_bp:,} bp  •  "
    f"{total_features:,} annotated features",
    ha="center",
    fontsize=12,
    fontweight="bold"
)

ax.text(
    7,
    0.75,
    "Python • Biopython • Pandas • SQLite • "
    "NCBI Datasets CLI • pytest • Linux/WSL • Git/GitHub",
    ha="center",
    fontsize=10
)

fig.tight_layout()

fig4 = OUT / "04_platform_workflow.png"
fig.savefig(fig4, dpi=220, bbox_inches="tight")
plt.close(fig)

conn.close()

# =========================================================
# VALIDATION
# =========================================================

figures = [fig1, fig2, fig3, fig4]

print("\n========================================")
print("P3 FIGURES GENERATED SUCCESSFULLY")
print("========================================")

for figure in figures:

    if not figure.exists():
        raise RuntimeError(f"Missing: {figure}")

    size = figure.stat().st_size

    if size < 10000:
        raise RuntimeError(
            f"Figure appears invalid: {figure} ({size} bytes)"
        )

    print(
        f"✓ {figure.name} — "
        f"{size:,} bytes"
    )

print("\n========================================")
print("ALL 4 REAL PROJECT VISUALS READY")
print("========================================")
