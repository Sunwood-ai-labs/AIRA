import os
from loguru import logger
from ..utils import run_command

class StagingManager:
    def __init__(self, repo_dir="./"):
        self.repo_dir = repo_dir

    def unstage_files(self):
        """ステージにある全てのファイルをアンステージする"""
        logger.info("Unstaging all files...")
        try:
            staged_files = run_command(["git", "diff", "--name-only", "--cached"], cwd=self.repo_dir).splitlines()
            if staged_files:
                run_command(["git", "reset", "HEAD", "--"] + staged_files, cwd=self.repo_dir)
                logger.success(f"Unstaged files: {', '.join(staged_files)}")
            else:
                logger.info("No staged files found.")
        except Exception as e:
            logger.error(f"Error while unstaging files: {e}")
            raise

    def stage_file(self, filename, action):
        """ファイルをステージする"""
        try:
            if action == "deleted":
                logger.info(f"Deleted file: {filename}")
                run_command(["git", "rm", filename], cwd=self.repo_dir)
            else:
                logger.info(f"Staged file: {filename}")
                run_command(["git", "add", filename], cwd=self.repo_dir)
        except Exception as e:
            logger.error(f"Error while staging file: {filename} - {e}")
            raise
