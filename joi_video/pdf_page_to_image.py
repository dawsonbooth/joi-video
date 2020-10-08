import argparse

import fitz
from PIL import Image


def pdf_page_to_image(filename, page: int = 0):
    pdf = fitz.open(filename)
    pix = pdf.loadPage(page).getPixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img


def main(filename: str, page: int, outfile: str):
    img = pdf_page_to_image(filename, page=page)
    img.save(outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str,
                        help="Path to PDF file")
    parser.add_argument('--page', type=int, default=0,
                        help="Page to convert")
    parser.add_argument('--outfile', type=str, required=True,
                        help="Output file path")
    args = parser.parse_args()

    exit(main(args.filename, args.page, args.outfile))
