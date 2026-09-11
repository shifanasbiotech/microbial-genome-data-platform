import argparse
import json

from .queries import GenomeQueries


def main():
    parser = argparse.ArgumentParser(
        description="Microbial Genome Data Platform"
    )

    parser.add_argument(
        "--database",
        default="results/microbial_genomes.sqlite",
        help="Path to SQLite database",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # genome command
    genome_parser = subparsers.add_parser(
        "genome",
        help="Show genome information",
    )

    genome_parser.add_argument(
        "accession",
        help="Genome assembly accession",
    )

    # replicons command
    replicons_parser = subparsers.add_parser(
        "replicons",
        help="Show replicons for a genome",
    )

    replicons_parser.add_argument(
        "accession",
        help="Genome assembly accession",
    )

    # features command
    features_parser = subparsers.add_parser(
        "features",
        help="Show genomic features",
    )

    features_parser.add_argument(
        "accession",
        help="Genome assembly accession",
    )

    args = parser.parse_args()

    queries = GenomeQueries(args.database)

    try:
        if args.command == "genome":
            result = queries.get_genome(args.accession)

        elif args.command == "replicons":
            result = queries.get_replicons(args.accession)

        elif args.command == "features":
            result = queries.get_features(args.accession)

        print(json.dumps(result, indent=2, default=str))

    finally:
        queries.close()
if __name__ == "__main__":
    main()