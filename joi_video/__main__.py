import argparse
import os
from pathlib import Path
from typing import Any, Dict, Union

from colorama import Fore

from .create_video import main as create_video
from .file import is_image, is_pdf, is_video

from itertools import chain


def parse_directory() -> Path:
    parser = argparse.ArgumentParser()

    parser.add_argument("directory", nargs="?", default=os.getcwd())

    args = parser.parse_args()

    return Path(args.directory)


def infer_paths(directory: Path) -> Dict[str, Union[str, os.PathLike]]:
    paths: Dict[str, Union[str, os.PathLike]] = dict()

    files = chain(directory.glob("*.*"), directory.parent.glob("*.*"))

    for path in files:
        filename = path.name.lower()
        if is_video(path):
            paths["source"] = path
        elif is_image(path):
            if "title" in filename:
                paths["title"] = path
            elif "start" in filename and "disclaimer" in filename:
                paths["disclaimer_start"] = path
            elif "end" in filename and "disclaimer" in filename:
                paths["disclaimer_end"] = path
            elif "bumper" in filename:
                paths["bumper"] = path
        elif is_pdf(path):
            paths["title"] = path

    paths["output"] = directory.joinpath(f"Joi_Delivers_Corp_Pres_{directory.resolve().name}.mp4")

    return paths


def prompt(message: str, default: Any):
    return (
        input(f"{Fore.LIGHTBLUE_EX}{message} [{Fore.CYAN}{default}{Fore.LIGHTBLUE_EX}]: {Fore.RESET}").strip()
        or default
    )


def enter_config(paths: Dict[str, Union[str, os.PathLike]]) -> Dict[str, Any]:
    config: Dict[str, Any] = dict(paths)
    config["slide_duration"] = 7.0

    try:
        print("Please enter the following information (press enter for default)...")

        config["source"] = prompt("Enter the path of the source video", config["source"])
        config["title"] = prompt("Enter the path of the title screen", config["title"])
        config["disclaimer_start"] = prompt(
            "Enter the path of the initial disclaimer screen", config["disclaimer_start"]
        )
        config["disclaimer_end"] = prompt("Enter the path of the final disclaimer screen", config["disclaimer_end"])
        config["bumper"] = prompt("Enter the path of the bumper screen", config["bumper"])
        config["output"] = prompt("Enter the path of the output video", config["output"])
        config["slide_duration"] = float(prompt("Enter the slide screen duration", config["slide_duration"]))

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
        config["slide_duration"],
    )

    return 0


if __name__ == "__main__":
    exit(main())
