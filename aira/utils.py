import subprocess
from loguru import logger
import time
from tqdm import tqdm

def run_command(command, cwd=None, check=True):
    """
    コマンドを実行し、結果を返す

    Args:
        command (list): 実行するコマンドとその引数のリスト
        cwd (str, optional): コマンドを実行するディレクトリ
        check (bool, optional): エラー時に例外を発生させるかどうか

    Returns:
        str: コマンドの実行結果
    """
    try:
        logger.info(f"実行コマンド： {' '.join(command)}")
        result = subprocess.run(command, cwd=cwd, check=check, capture_output=True, text=True, encoding='utf-8')
        time.sleep(1)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        logger.warning(f"Error while running command: {' '.join(command)}")
        logger.warning(f"Error message: {error_message}")
        raise

def tqdm_sleep(n):
    """
    進捗バーを表示しながらスリープする

    Args:
        n (int): スリープする秒数
    """
    for _ in tqdm(range(n)):
        time.sleep(1)

def create_config_template():
    """
    デフォルトの設定テンプレートを生成する

    Returns:
        dict: デフォルトの設定
    """
    return {
        "gaiah": {
            "run": True,
            "repo": {
                "repo_name": "AIRA",
                "description": "AI-Integrated Repository for Accelerated Development",
                "private": False
            },
            "local": {
                "repo_dir": "./",
                "no_initial_commit": False
            },
            "commit": {
                "process_commits": True,
                "commit_msg_path": ".Gaiah.md"
            }
        }
    }
