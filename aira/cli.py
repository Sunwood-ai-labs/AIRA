import argparse
from art import tprint
from loguru import logger
from gaiah.gaiah import Gaiah
from gaiah.cli import load_config

from harmon_ai.harmon_ai import HarmonAI

import sys
import os
import shutil
import yaml
from .aira import Aira
logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | <cyan>{name:<45}:{line:<5}</cyan> | <level>{message}</level>",
            "colorize": True,
        }
    ]
)

def parse_arguments():
    """
    コマンドライン引数を解析する
    """
    parser = argparse.ArgumentParser(description='AIRA - AI-Integrated Repository for Accelerated Development')
    parser.add_argument('--config', default='.aira/config.yml', help='設定ファイルのパス')
    return parser.parse_args()

def main():
    tprint("!  Welcome  to  AIRA  !")

    args = parse_arguments()
    aira = Aira(args.config)
    aira.run()

if __name__ == "__main__":
    main()