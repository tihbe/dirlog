import argparse
from . import createdir


def main():
    parser = argparse.ArgumentParser(description="Directory logging utility library.")
    parser.add_argument(
        "--create",
        "-c",
        metavar="name",
        type=str,
        help="Create a logging directory for the experiment.",
        required=False,
    )

    args = parser.parse_args()
    if args.create:
        print(createdir(exp_name=args.create))
        exit(0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
