import argparse
import mimetypes
import os
from pathlib import Path

from colorama import Fore, Style

from .create_video import main as create_video


def parse_directory() -> Path:
    parser = argparse.ArgumentParser()

    parser.add_argument("directory", nargs='?', default=os.getcwd())

    args = parser.parse_args()

    return Path(args.directory)


def infer_paths(directory: Path) -> dict:
    paths = {
        "source": "",
        "title": "",
        "disclaimer_start": "",
        "disclaimer_end": "",
        "bumper": "",
        "output": ""
    }

    for f in os.listdir(directory):
        mimetype = str(mimetypes.guess_type(f)[0])
        filename = Path(f).name.lower()
        if mimetype.startswith("video"):
            paths["source"] = f
        elif mimetype.startswith("image"):
            if "title" in filename:
                paths["title"] = f
            elif "start" in filename and "disclaimer" in filename:
                paths["disclaimer_start"] = f
            elif "end" in filename and "disclaimer" in filename:
                paths["disclaimer_end"] = f
            elif "bumper" in filename:
                paths["bumper"] = f

    paths["output"] = f"Joi_Delivers_Corp_Pres_{directory.name}.mp4"

    return paths


def enter_config(paths: dict) -> dict:
    config = dict(paths)
    config["slide_duration"] = 7.0

    try:
        print("Please enter the following information (press enter for default)...")

        config["source"] = input(
            f"Enter the path of the source video [{config['source']}]: ").strip() or config['source']
        config["title"] = input(
            f"Enter the path of the title screen [{config['title']}]: ").strip() or config['title']
        config["disclaimer_start"] = input(
            f"Enter the path of the initial disclaimer screen [{config['disclaimer_start']}]: ").strip() or config['disclaimer_start']
        config["disclaimer_end"] = input(
            f"Enter the path of the final disclaimer screen [{config['disclaimer_end']}]: ").strip() or config['disclaimer_end']
        config["bumper"] = input(
            f"Enter the path of the bumper screen [{config['bumper']}]: ").strip() or config['bumper']
        config["output"] = input(
            f"Enter the path of the output video [{config['output']}]: ").strip() or config['output']

        config["slide_duration"] = float(input(
            f"Enter the slide screen duration: [{config['slide_duration']}]").strip() or config['slide_duration'])
    except KeyboardInterrupt:
        print("Cancelled.")
        exit(1)

    return config


def main() -> int:

    directory = parse_directory()

    config = enter_config(infer_paths(directory))

    create_video(
        config["source"],
        config["title"],
        config["disclaimer_start"],
        config["disclaimer_end"],
        config["bumper"],
        config["output"],
        config["slide_duration"]
    )

    return 0


if __name__ == '__main__':
    exit(main())
