import logging
import math
import multiprocessing as mp
import os
import shutil
import subprocess
import tempfile
from functools import partial
from glob import glob

from fire.utils import grouper, map_with_threads, run_command
from tqdm import tqdm


def gdal_polygonize(src, dst):
    run_command(f'gdal_polygonize.py {src} {dst}')


def apply_threshold(src, dst, *, threshold):
    """
    Output source values (probabilities) instead of simply a binary mask

    Make sure nodata=0, so that gdal_polygonize step ignores pixels under
    threshold.

    """
    # Rescale to 255
    threshold = threshold * 255

    run_command('gdal_calc.py '
                f'--calc "(A >= {threshold}) * A" '
                f'-A {src} '
                '--NoDataValue 0 '
                f'--outfile {dst}')


def process_image(image, *, tmpdir, threshold):
    src = image
    if threshold:
        src = os.path.join(tmpdir, os.path.basename(image))
        apply_threshold(src=image, dst=src, threshold=threshold)
    name, _ = os.path.splitext(os.path.basename(image))
    dst = os.path.join(tmpdir, f'{name}.gpkg')
    gdal_polygonize(src, dst)


def merge_vector_files(*, input_dir, output, tmpdir):
    srcs = list(glob(os.path.join(input_dir, '*.gpkg')))
    src_groups = list(enumerate(grouper(srcs, n=1000)))
    groups_dir = os.path.join(tmpdir, 'groups')
    os.makedirs(groups_dir, exist_ok=True)

    def merge_chip_vector_files(enumerated_srcs, *, output_dir):
        i, srcs = enumerated_srcs
        srcs = [f for f in srcs if f]
        output = os.path.join(groups_dir, f'{i}.gpkg')
        run_command(
            f'ogrmerge.py -overwrite_ds -single -a_srs epsg:5382 '
            f'-f GPKG -o {output} {" ".join(srcs)}',
            quiet=False)
        return output

    # First, merge groups of vector files using ogrmerge.py in parallel
    output_dir = os.path.join(tmpdir, 'temp')
    worker = partial(merge_chip_vector_files, output_dir=output_dir)
    map_with_threads(src_groups, worker)

    # Second, merge ogrmerge results using ogr2ogr into a single file
    group_paths = glob(os.path.join(groups_dir, '*.gpkg'))
    for src in tqdm(group_paths):
        run_command(f'ogr2ogr -f GPKG -update -append {output} {src}',
                    quiet=False)


def polygonize(threshold=None, temp_dir=None, *, input_dir, output):
    images = list(glob(os.path.join(input_dir, '*.tif')))

    must_remove_temp_dir = False
    if temp_dir:
        # Make sure directory exists
        os.makedirs(temp_dir, exist_ok=True)
    else:
        # Create a temporary directory if user did not provide one
        must_remove_temp_dir = True
        tmpdir = tempfile.TemporaryDirectory()
        temp_dir = tmpdir.name

    # Process all chip images
    worker = partial(process_image, tmpdir=temp_dir, threshold=threshold)
    map_with_threads(images, worker)

    # Merge all vector files into a single one
    merge_vector_files(input_dir=temp_dir, output=output, tmpdir=temp_dir)

    if must_remove_temp_dir:
        tmpdir.cleanup()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=
        "Apply threshold and polygonize results into a single vector file")
    parser.add_argument("input_dir", help="results directory")
    parser.add_argument("-t",
                        "--threshold",
                        type=float,
                        help="apply threshold (0-1)",
                        default=None)
    parser.add_argument("-o", "--output", help="output in GPKG format")
    parser.add_argument("--temp-dir", help="temporary directory")

    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    polygonize(input_dir=args.input_dir,
               output=args.output,
               threshold=args.threshold,
               temp_dir=args.temp_dir)
