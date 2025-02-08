import argparse
from art import tprint
from loguru import logger
import sys
import os
import shutil
from dotenv import load_dotenv
from .aira import Aira
from sourcesage.cli import add_arguments as sourcesage_add_arguments

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
    """コマンドライン引数を解析する"""
    load_dotenv()
    default_model = os.getenv('LLM_MODEL', 'gemini/gemini-1.5-pro-latest')
    parser = argparse.ArgumentParser(description='AIRA - Automated Source Code Analysis Tool')
    parser.add_argument('--mode', nargs='+', default=['commit'], 
                      help='処理モード（commit: 自動コミット, sourcesage: SourceSage実行）')
    parser.add_argument('--model', default=default_model, help='使用するLLMモデル名')
    sourcesage_add_arguments(parser)
    return parser.parse_args()

def main():
    """メイン処理"""
    tprint("!  Welcome  to  AIRA  !")
    args = parse_arguments()
    aira = Aira(args=args)

    for mode in args.mode:
        if mode == "commit":
            logger.info("mode is << commit >>")
            aira.commit_manager.process_commits()
        elif mode == "sourcesage":
            logger.info("mode is << sourcesage >>")
            aira.run_sourcesage()
        else:
            logger.warning(f"Unknown mode: {mode}")
if __name__ == "__main__":
    main()
