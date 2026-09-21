from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
DB = BASE / "results" / "microbial_genomes.sqlite"
OUT = BASE / "reports" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

if not DB.exists():
    raise FileNotFoundError(f"Database not found: {DB}")

conn = sqlite3.connect(DB)

def columns(table):
    return [row[1] for row in conn.execute(f"PRAGMA table_info({table})")]

def pick(table, candidates):
    cols = columns(table)
    lowered = {c.lower(): c for c in cols}
    for candidate in candidates:
        if candidate.lower() in lowered:
            return lowered[candidate.lower()]
    return None

# -----------------------------
# 1. Genome size comparison
# -----------------------------
genome_table = "genomes"
feature_table = "features"
replicon_table = "replicons"

accession_col = pick(genome_table, [
    "assembly_accession", "accession", "assembly"
])

organism_col = pick(genome_table, [
    "organism", "organism_name", "species"
])

size_col = pick(genome_table, [
    "genome_size", "genome_length", "sequence_length",
    "total_sequence_bp", "total_length", "length"
])

feature_accession_col = pick(feature_table, [
    "assembly_accession", "accession", "genome_accession"
])

feature_type_col = pick(feature_table, [
    "feature_type", "type"
])

rep_accession_col = pick(replicon_table, [
    "assembly_accession", "accession", "genome_accession"
])

rep_length_col = pick(replicon_table, [
    "length", "length_bp", "sequence_length"
])

if accession_col is None:
    raise RuntimeError("Could not identify the genome accession column.")

# Get genome accessions
accessions = [
    row[0]
    for row in conn.execute(
        f"SELECT {accession_col} FROM {genome_table} ORDER BY {accession_col}"
    )
]

genome_sizes = {}

# Prefer genome-level stored size; otherwise calculate from replicons
if size_col:
    rows = conn.execute(
        f"SELECT {accession_col}, {size_col} "
        f"FROM {genome_table} ORDER BY {accession_col}"
    ).fetchall()
    for accession, size in rows:
        genome_sizes[accession] = int(size)
elif rep_accession_col and rep_length_col:
    rows = conn.execute(
        f"SELECT {rep_accession_col}, SUM({rep_length_col}) "
        f"FROM {replicon_table} GROUP BY {rep_accession_col} "
        f"ORDER BY {rep_accession_col}"
    ).fetchall()
    for accession, size in rows:
        genome_sizes[accession] = int(size)

# Feature counts per assembly
feature_counts = {}
if feature_accession_col:
    rows = conn.execute(
        f"SELECT {feature_accession_col}, COUNT(*) "
        f"FROM {feature_table} "
        f"GROUP BY {feature_accession_col} "
        f"ORDER BY {feature_accession_col}"
    ).fetchall()
    feature_counts = {a: int(c) for a, c in rows}

# Figure 1
labels = list(genome_sizes.keys())
sizes_mb = [genome_sizes[a] / 1_000_000 for a in labels]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels, sizes_mb)
ax.set_title("Microbial Genome Data Platform — Genome Sizes")
ax.set_xlabel("NCBI RefSeq assembly")
ax.set_ylabel("Genome size (Mb)")
ax.grid(axis="y", alpha=0.2)

for bar, accession in zip(bars, labels):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():.2f} Mb\n{feature_counts.get(accession, 0):,} features",
        ha="center",
        va="bottom",
        fontsize=9
    )

fig.tight_layout()
fig.savefig(OUT / "genome_size_comparison.png", dpi=220, bbox_inches="tight")
plt.close(fig)

# -----------------------------
# 2. E. coli feature landscape
# -----------------------------
if feature_type_col:
    # Use the first / smallest accession as the E. coli assembly used in P3
    ecoli_accession = "GCF_000005845.2"

    rows = conn.execute(
        f"SELECT {feature_type_col}, COUNT(*) "
        f"FROM {feature_table} "
        f"WHERE {feature_accession_col} = ? "
        f"GROUP BY {feature_type_col} "
        f"ORDER BY COUNT(*) DESC",
        (ecoli_accession,)
    ).fetchall()

    feature_labels = [r[0] for r in rows]
    feature_values = [int(r[1]) for r in rows]

    fig, ax = plt.subplots(figsize=(10, 7))

    # Horizontal bar chart keeps all feature labels readable
    order = list(range(len(feature_labels)))[::-1]
    ax.barh(
        [feature_labels[i] for i in order],
        [feature_values[i] for i in order]
    )

    ax.set_title(
        "E. coli K-12 MG1655 — Genomic Feature Distribution"
    )
    ax.set_xlabel("Feature count")
    ax.set_ylabel("Feature type")
    ax.grid(axis="x", alpha=0.2)

    for y, value in enumerate([feature_values[i] for i in order]):
        ax.text(
            value + max(feature_values) * 0.01,
            y,
            f"{value:,}",
            va="center",
            fontsize=9
        )

    ax.text(
        0,
        -0.13,
        f"Assembly: {ecoli_accession}  •  Total annotated features: {sum(feature_values):,}",
        transform=ax.transAxes,
        fontsize=9
    )

    fig.tight_layout()
    fig.savefig(
        OUT / "ecoli_feature_distribution.png",
        dpi=220,
        bbox_inches="tight"
    )
    plt.close(fig)

# -----------------------------
# 3. Platform dataset summary
# -----------------------------
total_bp = sum(genome_sizes.values())
total_features = sum(feature_counts.values())

fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")

ax.text(
    0.5, 0.88,
    "Microbial Genome Data Platform — Validation Dataset",
    ha="center",
    fontsize=20,
    fontweight="bold"
)

metrics = [
    ("3", "RefSeq genomes"),
    ("5", "replicons / contigs"),
    (f"{total_bp:,}", "total sequence bp"),
    (f"{total_features:,}", "annotated features"),
]

positions = [0.12, 0.37, 0.62, 0.87]

for x, (value, label) in zip(positions, metrics):
    ax.text(
        x, 0.55, value,
        ha="center",
        fontsize=22,
        fontweight="bold"
    )
    ax.text(
        x, 0.43, label,
        ha="center",
        fontsize=10
    )

ax.text(
    0.5, 0.17,
    "Python • Biopython • Pandas • SQLite • FASTA/GFF3 • NCBI Datasets CLI • pytest • Linux/WSL",
    ha="center",
    fontsize=10
)

fig.tight_layout()
fig.savefig(
    OUT / "platform_dataset_summary.png",
    dpi=220,
    bbox_inches="tight"
)
plt.close(fig)

conn.close()

print()
print("========================================")
print("PROJECT FIGURES GENERATED")
print("========================================")
for file in sorted(OUT.glob("*.png")):
    print(f"✓ {file.relative_to(BASE)}")
print()
