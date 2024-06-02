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
    parser = argparse.ArgumentParser(description='Gaiah - シンプルなGitリポジトリ管理ツール')
    
    parser.add_argument('--config', default='.aira/config.yml', help='設定ファイルのパス')

    return parser.parse_args()

def main():
    tprint("!  Welcome  to  AIRA  !")

    # .aira/config.ymlが存在するかチェック
    args = parse_arguments()
    aira_config_path = args.config
    if not os.path.exists(aira_config_path):
        # aira\template\config.ymlをコピー
        template_config_path = "aira/template/config.yml"
        os.makedirs(os.path.dirname(aira_config_path), exist_ok=True)
        shutil.copy(template_config_path, aira_config_path)
        logger.info(f"{aira_config_path}が見つかりませんでした。{template_config_path}からコピーしました。")
    else:
        logger.info(f"{aira_config_path}が見つかりました。")

    # .aira/config.ymlからconfig_pathを取得
    with open(aira_config_path, "r") as f:
        aira_config = yaml.safe_load(f)


    # ------------------
    # make abst
    #
    
    # ------------------
    # gaiah init
    #
    if(aira_config["aira"]["gaiah"]["run"]):
        
        gaiah_config_path = aira_config["aira"]["gaiah"]["develop"]["config_path"]
        gaiah_config = load_config(gaiah_config_path)
        logger.info(f"Gaiah config path : {gaiah_config_path}")
        if not os.path.exists(os.path.join(gaiah_config["gaiah"]["local"]["repo_dir"], ".git")):
            logger.info("初期化を行います...")
            gaiah_config_path = aira_config["aira"]["gaiah"]["init"]["config_path"]
            gaiah_config = load_config(gaiah_config_path)
        else:
            logger.info(".gitが発見されました...")

        tprint("-- Gaiah --")
        logger.info("Gaiahの処理を開始します...")
        gaiah = Gaiah(gaiah_config)
        gaiah.run()
    
    # ------------------
    # Harmon AI
    #
    if(aira_config["aira"]["harmon_ai"]["run"]):
        logger.info("Harmon AIの処理を開始します...")
        harmon_ai = HarmonAI()
        harmon_ai.run()

    # ------------------
    # gaiah init
    #
    gaiah_config_path = aira_config["aira"]["gaiah"]["develop"]["config_path"]
    gaiah_config = load_config(gaiah_config_path)
    gaiah = Gaiah(gaiah_config)
    gaiah.run()
    
if __name__ == "__main__":
    main()