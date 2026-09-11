from src.microbial_genome_platform.qc import genome_qc


def test_genome_qc():
    sequences = [
        {
            "sequence_id": "chr1",
            "length_bp": 1000,
            "gc_percent": 50.0,
        }
    ]

    features = [
        {
            "sequence_id": "chr1",
            "feature_type": "gene",
            "start": 1,
            "end": 100,
        }
    ]

    result = genome_qc(sequences, features)

    assert result["sequence_count"] == 1
    assert result["total_sequence_bp"] == 1000
    assert result["feature_count"] == 1
    assert result["invalid_coordinates"] == 0
