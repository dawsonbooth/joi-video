import argparse
import configparser

from concat_directory import main as concat_directory

# TODO: config module, convert pdf

def main(directory: str, config: str, outfile: str):
    cp = configparser.ConfigParser()
    cp.read(config)
    cp.sections()

    concat_directory(
        directory,
        float(cp['OUTPUT']['IMAGE_DURATION']),
        outfile,
        **cp['SOURCE']
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str,
                        help="Path to directory containing media files")
    parser.add_argument('--config', type=str, required=True,
                        help="The config file")
    parser.add_argument('--outfile', type=str, required=True,
                        help="Output file path")
    args = parser.parse_args()

    exit(main(args.directory, args.config, args.outfile))
