import argparse
from pathlib import Path

from create_video import main as create_video
from settings import Settings


def parse_directory() -> Path:
    parser = argparse.ArgumentParser()

    parser.add_argument("directory", type=Path, default=Path.cwd())

    args = parser.parse_args()

    return args.directory


def main() -> int:
    try:
        create_video(Settings(parse_directory()))
    except KeyboardInterrupt:
        print("\nCancelled.")
    return 0


if __name__ == "__main__":
    exit(main())
