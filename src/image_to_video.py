import argparse

import ffmpeg


def main(filename: str, duration: float, outfile: str) -> int:

    (
        ffmpeg
        .input(filename, t=duration, loop=1)
        .output(outfile)
        .overwrite_output()
        .run()
    )

    # Finish with no errors
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str,
                        help="Path to image")
    parser.add_argument('--duration', type=float, default=5.0,
                        help="Image duration")
    parser.add_argument('--outfile', type=str, required=True,
                        help="Output file path")
    args = parser.parse_args()

    exit(main(args.filename, args.duration, args.outfile))
