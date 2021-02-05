import ffmpeg

from .file import load_file


def get_video_stream(filename: str):
    probe = ffmpeg.probe(filename)
    return next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)


def main(
    source: str,
    title: str,
    disclaimer_start: str,
    disclaimer_end: str,
    bumper: str,
    output: str,
    slide_duration: float,
):
    video_stream = get_video_stream(source)

    height = int(video_stream["height"])
    width = int(video_stream["width"])
    raw_duration = float(video_stream["duration"])

    title_media = load_file(title, slide_duration, width, height)
    dis_start_media = load_file(disclaimer_start, slide_duration, width, height)
    raw_media = load_file(source, raw_duration)
    dis_end_media = load_file(disclaimer_end, slide_duration, width, height)
    bumper_media = load_file(bumper, slide_duration, width, height)

    (
        ffmpeg.concat(*title_media, *dis_start_media, *raw_media, *dis_end_media, *bumper_media, v=1, a=1)
        .output(str(output), s=f"{width}x{height}", r=24, preset="ultrafast")
        .overwrite_output()
        .run()
    )
