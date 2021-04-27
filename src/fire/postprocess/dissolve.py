import logging
import math
import multiprocessing as mp

import fiona
from fire.utils import grouper, map_with_processes
from shapely.geometry import mapping, shape
from shapely.ops import unary_union
from tqdm import tqdm

GROUP_SIZE = 10000


def dissolve_group(geom_group):
    geoms = [shape(f["geometry"]) for f in geom_group if f]
    # logging.info("[%d] Total shapes: %d", i, len(geoms))

    # logging.info("[%d] Try to fix geometry by applying buffer 0", i)
    geoms = [s.buffer(0) for s in geoms]

    # logging.info("[%d] Filter invalid shapes", i)
    geoms = [s.buffer(0) for s in geoms if s.is_valid]
    # logging.info("[%d] Valid shapes: %d", i, len(geoms))

    # logging.info("[%d] Perform unary union to dissolve shapes", i)
    dissolved = unary_union(geoms)
    return dissolved


def dissolve(src, dst):
    block_geoms = []
    with fiona.open(src, 'r') as ds_in:
        crs = ds_in.crs
        drv = ds_in.driver

        # This is needed because calling iter() over ds_in again
        # somehow resets the iterator...
        gen = (g for g in ds_in)

        groups = grouper(gen, GROUP_SIZE)
        total_groups = math.ceil(len(ds_in) / GROUP_SIZE)
        logging.info("Total features: %d, total groups (of size %d): %d",
                     len(ds_in), GROUP_SIZE, total_groups)

        block_geoms = map_with_processes(groups,
                                         dissolve_group,
                                         total=total_groups)

    logging.info("Dissolve blocks")
    dissolved = unary_union(block_geoms)

    schema = {"geometry": "Polygon", "properties": {"id": "int"}}

    logging.info("Write output file")
    with fiona.open(dst, 'w', driver=drv, schema=schema, crs=crs) as ds_dst:
        for i, g in enumerate(tqdm(dissolved)):
            ds_dst.write({"geometry": mapping(g), "properties": {"id": i}})


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Dissolve polygons in polygonized results vector file")
    parser.add_argument("src", help="path to input vector file")
    parser.add_argument("dst",
                        help="path to output vector file (in GPKG format)")

    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    dissolve(src=args.src, dst=args.dst)
