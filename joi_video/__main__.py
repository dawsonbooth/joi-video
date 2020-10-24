import argparse
import os
from pathlib import Path

from colorama import Fore

from .create_video import main as create_video
from .file import mimetype


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
        f = directory.joinpath(f)
        filetype = str(mimetype(f)[0])
        filename = f.name.lower()
        if filetype.startswith("video"):
            paths["source"] = f
        elif filetype.startswith("image"):
            if "title" in filename:
                paths["title"] = f
            elif "start" in filename and "disclaimer" in filename:
                paths["disclaimer_start"] = f
            elif "end" in filename and "disclaimer" in filename:
                paths["disclaimer_end"] = f
            elif "bumper" in filename:
                paths["bumper"] = f
        elif filetype.endswith("pdf"):
            paths["title"] = f

    paths["output"] = directory.joinpath(
        f"Joi_Delivers_Corp_Pres_{directory.resolve().name}.mp4")

    return paths


def prompt(message: str, default: str):
    return input(
        f"{Fore.LIGHTBLUE_EX}{message} [{Fore.CYAN}{default}{Fore.LIGHTBLUE_EX}]: {Fore.RESET}"
    ).strip() or default


def enter_config(paths: dict) -> dict:
    config = dict(paths)
    config["slide_duration"] = 7.0

    try:
        print("Please enter the following information (press enter for default)...")

        config["source"] = prompt(
            "Enter the path of the source video", config['source'])
        config["title"] = prompt(
            "Enter the path of the title screen", config['title'])
        config["disclaimer_start"] = prompt(
            "Enter the path of the initial disclaimer screen", config['disclaimer_start'])
        config["disclaimer_end"] = prompt(
            "Enter the path of the final disclaimer screen", config['disclaimer_end'])
        config["bumper"] = prompt(
            "Enter the path of the bumper screen", config['bumper'])
        config["output"] = prompt(
            "Enter the path of the output video", config['output'])
        config["slide_duration"] = prompt(
            "Enter the slide screen duration", config['slide_duration'])

    except KeyboardInterrupt:
        print("\nCancelled.")
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
