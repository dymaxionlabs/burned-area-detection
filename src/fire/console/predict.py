# -*- coding: utf-8 -*-
"""
This script performs model prediction over a set of image chips using an already
trained U-Netq model.
"""

import argparse
import logging
import sys

from fire import __version__
from fire.unet.predict import PredictConfig, predict

__author__ = "Damián Silvani"
__copyright__ = "Dymaxion Labs"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Predict over a directory of image tiles",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--version",
                        action="version",
                        version="meduy {ver}".format(ver=__version__))
    parser.add_argument("-v",
                        "--verbose",
                        dest="loglevel",
                        help="set loglevel to INFO",
                        action="store_const",
                        const=logging.INFO)
    parser.add_argument("-vv",
                        "--very-verbose",
                        dest="loglevel",
                        help="set loglevel to DEBUG",
                        action="store_const",
                        const=logging.DEBUG)

    parser.add_argument("dir", help="Path to image tiles to predict")
    parser.add_argument("-o",
                        "--output-dir",
                        help="path to results output directory",
                        default="./results")
    parser.add_argument("--model",
                        "-m",
                        help="path to trained model (.h5)",
                        default="./unet.h5")
    parser.add_argument("-W", "--width", type=int, help="Image tile width")
    parser.add_argument("-H", "--height", type=int, help="Image tile height")
    parser.add_argument("-N",
                        "--num-channels",
                        default=3,
                        type=int,
                        help="Number of channels")
    parser.add_argument("-C",
                        "--num-classes",
                        default=1,
                        type=int,
                        help="Number of classes")
    parser.add_argument("--batch-size",
                        default=32,
                        type=int,
                        help="Batch size for prediction")

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel,
                        stream=sys.stdout,
                        format=logformat,
                        datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    config = PredictConfig(batch_size=args.batch_size,
                           model_path=args.model,
                           images_path=args.dir,
                           results_path=args.output_dir,
                           height=args.height,
                           width=args.width,
                           n_channels=args.num_channels,
                           n_classes=args.num_classes)

    predict(config)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
