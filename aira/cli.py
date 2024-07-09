import argparse
from art import tprint
from loguru import logger
from gaiah.gaiah import Gaiah
from gaiah.cli import load_config

from harmon_ai.harmon_ai import HarmonAI
from sourcesage.cli import add_arguments as sourcesage_add_arguments
import sourcesage

import sys
import os
import shutil
import yaml
from .aira import Aira

logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | <cyan>{name:<35}:{function:<35}:{line:<5}</cyan> | <level>{message}</level>",
            "colorize": True,
        }
    ]
)

def parse_arguments():
    """
    コマンドライン引数を解析する
    """
    parser = argparse.ArgumentParser(description='AIRA - AI-Integrated Repository for Accelerated Development')
    parser.add_argument('--config', default='.aira/config.dev.yml', help='設定ファイルのパス')
    parser.add_argument('--mode', nargs='+', default=['commit'], help='処理モード（複数指定可）')
    sourcesage_add_arguments(parser)
    return parser.parse_args()

def main():
    tprint("!  Welcome  to  AIRA  !")

    args = parse_arguments()
    aira = Aira(args=args, config_path=args.config)

    for mode in args.mode:
        if mode == "make":
            logger.info("mode is << make >>")
            aira.make_repo()
            aira.run()
            aira.co_and_merge_branches()
        
        elif mode == "commit":
            logger.info("mode is << commit >>")
            aira.run()

        elif mode == "sourcesage":
            logger.info("mode is << sourcesage >>")
            aira.run_sourcesage()  # Airaクラスのrun_sourcesageメソッドを実行
        
        else:
            logger.warning(f"Unknown mode: {mode}")

if __name__ == "__main__":
    main()
