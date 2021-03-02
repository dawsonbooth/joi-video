import mimetypes
import os
import tempfile
from pathlib import Path
from typing import Union

import ffmpeg
import fitz
from PIL import Image

SILENCE = Path(__file__).parent.resolve() / "silence.mp3"
TEMP = Path(tempfile.gettempdir())


def mimetype(path: Union[str, os.PathLike]):
    return mimetypes.guess_type(path)


def is_image(path: Union[str, os.PathLike]) -> bool:
    return str(mimetype(path)[0]).startswith("image")


def is_video(path: Union[str, os.PathLike]) -> bool:
    return str(mimetype(path)[0]).startswith("video")


def is_pdf(path: Union[str, os.PathLike]) -> bool:
    return str(mimetype(path)[0]).endswith("pdf")


def is_audio(path: Union[str, os.PathLike]) -> bool:
    return str(mimetype(path)[0]).startswith("image")


def pdf_page_to_image(path: Union[str, os.PathLike], page: int = 0):
    pdf = fitz.open(path)
    pix = pdf.loadPage(page).getPixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img


def load_video(path: Union[str, os.PathLike], duration: float):
    clip = ffmpeg.input(path)
    video = clip.video.filter("fade", type="in", start_time=0, duration=0.5).filter(
        "fade", type="out", start_time=duration - 0.5, duration=0.5
    )
    return video, clip.audio


def load_audio(path: Union[str, os.PathLike], duration: float):
    clip = ffmpeg.input(path, t=duration)
    return clip.audio


def load_image(path: Union[str, os.PathLike], duration: float, width: int, height: int):
    clip = ffmpeg.input(path, t=duration, loop=1)
    video = (
        clip.filter("scale", size=f"{width}x{height}", force_original_aspect_ratio="decrease")
        .filter("setsar", "1/1")
        .filter("pad", str(width), str(height), "(ow-iw)/2", "(oh-ih)/2")
        .filter("fade", type="in", start_time=0, duration=0.5)
        .filter("fade", type="out", start_time=duration - 0.5, duration=0.5)
    )
    return video, load_audio(SILENCE, duration=duration)


def load_pdf_page(path: Union[str, os.PathLike], *args):
    img = pdf_page_to_image(path)
    img_path = TEMP / "slide.png"
    img.save(img_path)
    return load_image(img_path, *args)


def load_file(path: Union[str, os.PathLike], *args):
    if is_video(path):
        return load_video(path, *args)
    elif is_image(path):
        return load_image(path, *args)
    elif is_pdf(path):
        return load_pdf_page(path, *args)
    elif is_audio(path):
        return load_audio(path, *args)
