import mimetypes
import tempfile
from pathlib import Path

import ffmpeg
import fitz
from PIL import Image

SILENCE = Path(__file__).parent.joinpath("silence.mp3")
TEMP = Path(tempfile.gettempdir())


def mimetype(filename: str):
    return mimetypes.guess_type(filename)


def pdf_page_to_image(filename, page: int = 0):
    pdf = fitz.open(filename)
    pix = pdf.loadPage(page).getPixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img


def load_video(filename: str, duration: float):
    clip = ffmpeg.input(filename)
    video = clip.video.filter("fade", type="in", start_time=0, duration=0.5).filter(
        "fade", type="out", start_time=duration - 0.5, duration=0.5
    )
    return video, clip.audio


def load_audio(filename: str, duration: float):
    clip = ffmpeg.input(filename, t=duration)
    return clip.audio


def load_image(filename: str, duration: float, width: int, height: int):
    clip = ffmpeg.input(filename, t=duration, loop=1)
    video = (
        clip.filter("scale", size=f"{width}x{height}", force_original_aspect_ratio="decrease")
        .filter("setsar", "1/1")
        .filter("pad", str(width), str(height), "(ow-iw)/2", "(oh-ih)/2")
        .filter("fade", type="in", start_time=0, duration=0.5)
        .filter("fade", type="out", start_time=duration - 0.5, duration=0.5)
    )
    return video, load_audio(SILENCE, duration=duration)


def load_pdf_page(filename: str, *args):
    img = pdf_page_to_image(filename)
    img_path = TEMP.joinpath("slide.png")
    img.save(img_path)
    return load_image(img_path, *args)


def load_file(filename: str, *args):
    filetype = str(mimetype(filename)[0])
    if filetype.startswith("video"):
        return load_video(filename, *args)
    elif filetype.startswith("image"):
        return load_image(filename, *args)
    elif filetype.endswith("pdf"):
        return load_pdf_page(filename, *args)
    elif filetype.startswith("audio"):
        return load_audio(filename, *args)
