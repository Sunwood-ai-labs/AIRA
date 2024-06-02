# aira/repository_manager.py
import subprocess
from loguru import logger
import os
from gaiah.utils import run_command, tqdm_sleep

class RepositoryManager:
    def __init__(self, config):
        self.config = config

    def is_initialized(self):
        repo_dir = self.config["gaiah"]["local"]["repo_dir"]
        logger.info(f"repo_dir is {repo_dir}")

        # ディレクトリが存在するか確認
        if not os.path.exists(repo_dir):
            return False

        return ".git" in os.listdir(repo_dir)

    def init(self):
        repo_dir = self.config["gaiah"]["local"]["repo_dir"]
        os.makedirs(repo_dir, exist_ok=True)
        run_command(command=["git", "init"], cwd=repo_dir)
        logger.info(f"Initialized repository at {repo_dir}")