from loguru import logger
from .utils import run_command

class RepositoryManager:
    def __init__(self):
        self.repo_dir = "./"

    def get_staged_files(self):
        """ステージングされているファイルの一覧を取得する"""
        staged_files = run_command(["git", "diff", "--name-only", "--cached"], cwd=self.repo_dir)
        return staged_files.splitlines() if staged_files else []

    def get_current_branch(self):
        """現在のブランチ名を取得する"""
        return run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.repo_dir).strip()

    def checkout_branch(self, branch_name, create=False):
        """指定したブランチをチェックアウトする"""
        if create:
            run_command(["git", "checkout", "-b", branch_name], cwd=self.repo_dir)
        else:
            run_command(["git", "checkout", branch_name], cwd=self.repo_dir)
        logger.success(f"Checked out branch: {branch_name}")
        return True
