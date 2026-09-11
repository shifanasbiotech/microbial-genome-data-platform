from src.microbial_genome_platform.parsers import (
    parse_fasta,
    parse_gff3,
)


def test_parse_fasta(tmp_path):
    path = tmp_path / "test.fna"

    path.write_text(
        ">contig1\n"
        "ATGCGC\n"
    )

    records = parse_fasta(path)

    assert len(records) == 1
    assert records[0]["length_bp"] == 6
    assert records[0]["gc_percent"] == 66.667


def test_parse_gff3(tmp_path):
    path = tmp_path / "test.gff3"

    path.write_text(
        "##gff-version 3\n"
        "contig1\tRefSeq\tgene\t1\t100\t.\t+\t.\tID=gene1\n"
    )

    records = parse_gff3(path)

    assert len(records) == 1
    assert records[0]["feature_type"] == "gene"
    assert records[0]["start"] == 1
    assert records[0]["end"] == 100
