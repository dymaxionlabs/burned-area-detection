import logging
import multiprocessing as mp
import os
from functools import partial
from glob import glob
from multiprocessing.pool import ThreadPool

import cv2
import numpy as np
import rasterio
import rasterio.mask
from fire.utils import map_with_threads, resize
from shapely.geometry import box
from tqdm import tqdm


def add_extra_band_to_image(img_path, *, input_dir, output_dir, band_path, n_bands):
    with rasterio.open(os.path.join(input_dir, img_path)) as src:
        profile_ = src.profile.copy()
        profile_.update(count=src.count + n_bands, dtype=np.uint8)
        img_ = src.read()
        window = box(*src.bounds)  # get a window
        h, w = src.height, src.width

    with rasterio.open(band_path) as extra_dim:
        try:
            img_shape, _ = rasterio.mask.mask(
                extra_dim, [window],
                crop=True)  ## cut original extra dim with that size
        except ValueError as err:
            logging.error(err)
            return

    img_shape = resize(img_shape[0], (h, w)).astype(np.uint8)

    with rasterio.open(os.path.join(output_dir, img_path), 'w',
                       **profile_) as dst:
        for b in range(img_.shape[0]):
            dst.write(img_[b, :, :], b + n_bands)
        dst.write(img_shape, img_.shape[0] + n_bands)


def concatenate(*, input_dir, output_dir, band_path, n_bands):
    os.makedirs(output_dir, exist_ok=True)

    images = [
        os.path.basename(f)
        for f in (glob(os.path.join(input_dir, '*.tif')))
    ]
    logging.info("Total images: %d", len(images))

    worker = partial(add_extra_band_to_image,
                     input_dir=input_dir,
                     output_dir=output_dir,
                     band_path=band_path,
                     n_bands =n_bands)
    map_with_threads(images, worker)

    total_new_img = len(glob(os.path.join(output_dir, '*.tif')))
    logging.info("Images generated: %d", total_new_img)
    logging.info("Images skipped (no overlap): %d",
                 len(images) - total_new_img)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Concatenate extra band to image chips")
    parser.add_argument("-i", "--input-dir", required=True, help="images path")
    parser.add_argument("-o",
                        "--output-dir",
                        required=True,
                        help="output images path")
    parser.add_argument("-b", "--band-path", required=True, help="band path")
    parser.add_argument("-n", "--N-bands", required=True, help="number of bands to add")
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    concatenate(input_dir=args.input_dir,
                output_dir=args.output_dir,
                band_path=args.band_path,
                n_bands=args.n_bands
               )
