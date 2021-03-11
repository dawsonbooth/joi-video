import os
from typing import Union

import ffmpeg

from file import load_file
from settings import Settings


def get_video_stream(path: Union[str, os.PathLike]):
    probe = ffmpeg.probe(path)
    return next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)


def main(settings: Settings):
    video_stream = get_video_stream(settings.source)

    height = int(video_stream["height"])
    width = int(video_stream["width"])
    raw_duration = float(video_stream["duration"])

    title_media = load_file(settings.title, settings.slide_duration, width, height)
    dis_start_media = load_file(settings.disclaimer_start, settings.slide_duration, width, height)
    raw_media = load_file(settings.source, raw_duration)
    dis_end_media = load_file(settings.disclaimer_end, settings.slide_duration, width, height)
    bumper_media = load_file(settings.bumper, settings.slide_duration, width, height)

    (
        ffmpeg.concat(*title_media, *dis_start_media, *raw_media, *dis_end_media, *bumper_media, v=1, a=1)
        .output(str(settings.output), s=f"{width}x{height}", r=24, preset="ultrafast")
        .overwrite_output()
        .run()
    )
