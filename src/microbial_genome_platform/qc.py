def genome_qc(sequence_records, feature_records):
    """Generate reproducible sequence and annotation QC metrics."""

    invalid_sequences = [
        r for r in sequence_records
        if r["length_bp"] <= 0
    ]

    invalid_features = [
        r for r in feature_records
        if r["start"] <= 0
        or r["end"] < r["start"]
    ]

    feature_types = {}

    for record in feature_records:
        feature_types[record["feature_type"]] = (
            feature_types.get(record["feature_type"], 0) + 1
        )

    return {
        "sequence_count": len(sequence_records),
        "total_sequence_bp": sum(
            r["length_bp"] for r in sequence_records
        ),
        "invalid_sequences": len(invalid_sequences),
        "feature_count": len(feature_records),
        "feature_types": len(feature_types),
        "invalid_coordinates": len(invalid_features),
        "top_feature_types": sorted(
            feature_types.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:10],
    }
