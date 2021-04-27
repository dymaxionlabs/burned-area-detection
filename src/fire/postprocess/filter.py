import numpy as np
import os
import rasterio
import shutil
from functools import partial
from glob import glob

from basurales.utils import map_with_processes


def get_max_prob(p):
    with rasterio.open(p) as src:
        img = src.read()
        return np.max(img)


def filter_chip(src, *, threshold, output_dir):
    print("threshold-> ",threshold)
    if get_max_prob(src) >= threshold:
        dst = os.path.join(output_dir, os.path.basename(src))
        os.makedirs(output_dir, exist_ok=True)
        os.symlink(os.path.abspath(src), os.path.abspath(dst))



def filter_by_max_prob(input_dir, output_dir, threshold):
    shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    threshold = round(threshold * 255)
    print("threshold: ",threshold)
    files = glob(os.path.join(input_dir, '*'))
    worker = partial(filter_chip, output_dir=output_dir, threshold=threshold)
    map_with_processes(files, worker)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Filter directory of result chips by max. prob threshold")
    parser.add_argument("input_dir", help="results directory")
    parser.add_argument("-t",
                        "--threshold",
                        type=float,
                        help="apply threshold (between 0 and 1)",
                        default=0.5)
    parser.add_argument("-o", "--output-dir", help="output results directory")

    args = parser.parse_args()

    filter_by_max_prob(input_dir=args.input_dir,
                       output_dir=args.output_dir,
                       threshold=args.threshold)
