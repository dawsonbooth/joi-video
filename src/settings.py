from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import Callable, DefaultDict, Optional, TypeVar

from colorama import Fore

from file import is_image, is_pdf, is_video

D = TypeVar("D")


def prompt(
    message: str,
    default: Optional[D],
    transform: Callable[[str], D],
    default_display: Callable[[D], str] = str,
) -> D:
    PREFIX = f"{Fore.LIGHTBLUE_EX}{message}"
    RESET = Fore.RESET

    if default is not None:
        BOX = f"{Fore.CYAN}{default_display(default)}{Fore.LIGHTBLUE_EX}"
        response = input(f"{PREFIX} [{BOX}]: {RESET}")
        if response == "":
            return default
    else:
        response = input(f"{PREFIX}: {RESET}")
        while response == "":
            print("This path cannot be blank!")
            response = input(f"{PREFIX}: {RESET}")

    return transform(response.strip())


def prompt_path(message: str, path: Optional[Path]) -> Path:
    if path is None:
        return prompt(message, path, Path, lambda _: "")
    return prompt(message, path, Path, lambda p: str(p.relative_to(Path.cwd().resolve())))


class Settings:
    source: Path
    title: Path
    disclaimer_start: Path
    disclaimer_end: Path
    bumper: Path
    output: Path

    slide_duration: float

    def __init__(self, directory: Path) -> None:
        directory = directory.resolve()
        files = list(chain(directory.glob("*.*"), directory.parent.glob("*.*")))

        paths: DefaultDict[str, Optional[Path]] = defaultdict(lambda: None)

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

        paths["output"] = directory / f"Joi_Delivers_Corp_Pres_{directory.name}.mp4"

        print("Please enter the following information (press enter for default)...")

        self.source = prompt_path("Enter the path of the source video", paths["source"])
        self.title = prompt_path("Enter the path of the title screen", paths["title"])
        self.disclaimer_start = prompt_path(
            "Enter the path of the initial disclaimer screen", paths["disclaimer_start"]
        )
        self.disclaimer_end = prompt_path("Enter the path of the final disclaimer screen", paths["disclaimer_end"])
        self.bumper = prompt_path("Enter the path of the bumper screen", paths["bumper"])
        self.output = prompt_path("Enter the path of the output video", paths["output"])
        self.slide_duration = prompt("Enter the slide screen duration", 7.0, float)
