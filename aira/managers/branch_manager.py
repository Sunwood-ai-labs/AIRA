from loguru import logger
from ..utils import run_command

class BranchManager:
    def __init__(self, repo_dir="./"):
        self.repo_dir = repo_dir

    def get_current_branch(self):
        """現在のブランチ名を取得する"""
        return run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.repo_dir).strip()

    def branch_exists(self, branch_name):
        """指定したブランチが存在するかチェックする"""
        try:
            run_command(["git", "rev-parse", "--verify", branch_name], cwd=self.repo_dir)
            return True
        except Exception:
            return False

    def has_uncommitted_changes(self):
        """未コミットの変更があるかチェックする"""
        try:
            status = run_command(["git", "status", "--porcelain"], cwd=self.repo_dir)
            return bool(status.strip())
        except Exception:
            return False

    def stash_changes(self):
        """現在の変更を一時保存する"""
        if self.has_uncommitted_changes():
            logger.info("Stashing uncommitted changes...")
            run_command(["git", "stash", "save", "AIRA: Temporary stash"], cwd=self.repo_dir)

    def pop_stashed_changes(self):
        """一時保存した変更を復元する"""
        try:
            run_command(["git", "stash", "pop"], cwd=self.repo_dir)
            logger.info("Restored stashed changes")
        except Exception as e:
            logger.warning(f"No stashed changes to restore or conflict occurred: {e}")

    def checkout_branch(self, branch_name, create=False):
        """ブランチをチェックアウトする"""
        try:
            current = self.get_current_branch()
            if current == branch_name:
                logger.info(f"Already on branch {branch_name}")
                return

            # 未コミットの変更がある場合は一時保存
            had_changes = self.has_uncommitted_changes()
            if had_changes:
                self.stash_changes()

            try:
                if create and not self.branch_exists(branch_name):
                    run_command(["git", "checkout", "-b", branch_name], cwd=self.repo_dir)
                else:
                    if not self.branch_exists(branch_name):
                        run_command(["git", "checkout", "-b", branch_name], cwd=self.repo_dir)
                    else:
                        run_command(["git", "checkout", branch_name], cwd=self.repo_dir)
                logger.success(f"Checked out branch: {branch_name}")
            finally:
                # 一時保存した変更を復元
                if had_changes:
                    self.pop_stashed_changes()

        except Exception as e:
            logger.error(f"Error while checking out branch: {e}")
            raise

    def merge_to_develop(self, source_branch):
        """developブランチへのマージと元ブランチの削除を行う"""
        if not self.branch_exists(source_branch):
            logger.warning(f"Branch {source_branch} does not exist. Skipping merge.")
            return

        try:
            current_branch = self.get_current_branch()
            
            # 未コミットの変更がある場合は一時保存
            had_changes = self.has_uncommitted_changes()
            if had_changes:
                self.stash_changes()

            try:
                self.checkout_branch("develop")
                run_command(["git", "merge", "--no-ff", source_branch], cwd=self.repo_dir)
                logger.success(f"Successfully merged {source_branch} into develop")
                
                if source_branch != "main":
                    run_command(["git", "branch", "-d", source_branch], cwd=self.repo_dir)
                    logger.success(f"Deleted branch: {source_branch}")
                
            except Exception as merge_error:
                logger.error(f"Merge conflict occurred: {merge_error}")
                run_command(["git", "merge", "--abort"], cwd=self.repo_dir)
                raise
            finally:
                if current_branch != source_branch or source_branch == "main":
                    self.checkout_branch(current_branch)
                else:
                    self.checkout_branch("develop")
                
                # 一時保存した変更を復元
                if had_changes:
                    self.pop_stashed_changes()
                
        except Exception as e:
            logger.error(f"Error during merge to develop: {e}")
            raise
