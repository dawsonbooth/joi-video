import argparse

import ffmpeg


def get_video_stream(filename: str):
    probe = ffmpeg.probe(filename)
    return next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)


def load_video(filename: str, duration: float):
    clip = (
        ffmpeg.input(filename)
    )
    video = (
        clip.video
        .filter('fade', type='in', start_time=0, duration=.5)
        .filter('fade', type='out', start_time=duration - .5, duration=.5)
    )
    return video, clip.audio


def load_image(filename: str, duration: float, width: int, height: int):
    clip = (
        ffmpeg
        .input(filename, t=duration, loop=1)
    )
    video = (
        clip
        .filter('scale', size=f"{width}x{height}")
        .filter('fade', type='in', start_time=0, duration=.5)
        .filter('fade', type='out', start_time=duration - .5, duration=.5)
    )
    return video


def load_audio(filename: str, duration: float):
    clip = ffmpeg.input(filename, t=duration)
    return clip.audio


def main(directory: str, image_duration: float, outfile: str) -> int:
    video_stream = get_video_stream(f"{directory}/raw.mp4")

    height = int(video_stream['height'])
    width = int(video_stream['width'])
    raw_duration = float(video_stream['duration'])

    title_video = load_image(
        f"{directory}/Title.png", image_duration, width, height)
    dis_start_video = load_image(
        f"{directory}/DisclaimerStart.png", image_duration, width, height)
    raw_video, raw_audio = load_video(f"{directory}/raw.mp4", raw_duration)
    dis_end_video = load_image(
        f"{directory}/DisclaimerEnd.png", image_duration, width, height)
    bumper_video = load_image(
        f"{directory}/Bumper.png", image_duration, width, height)
    silence_audio = load_audio(
        f"{directory}/silence.mp3", duration=image_duration)

    (
        ffmpeg
        .concat(
            title_video, silence_audio,
            dis_start_video, silence_audio,
            raw_video, raw_audio,
            dis_end_video, silence_audio,
            bumper_video, silence_audio,
            v=1, a=1
        )
        .output(outfile, pix_fmt='yuv420p', s=f"{width}x{height}", r=24, preset='ultrafast')
        .overwrite_output()
        .run()
    )

    # Finish with no errors
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str,
                        help="Path to directory containing media files")
    parser.add_argument('--duration', type=float, default=7.0,
                        help="Image duration")
    parser.add_argument('--outfile', type=str, required=True,
                        help="Output file path")
    args = parser.parse_args()

    exit(main(args.directory, args.duration, args.outfile))
