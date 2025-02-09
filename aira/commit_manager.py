import os
import re
from loguru import logger
from .utils import run_command, tqdm_sleep
from .managers.staging_manager import StagingManager
from .managers.branch_manager import BranchManager

class CommitManager:
    FILENAME_REGEX = r'(?m)^###\s(.+)'
    COMMIT_MESSAGE_REGEX = r'```commit-msg\n(.*?)\n```'

    def __init__(self, config):
        self.config = config
        self.repo_dir = "./"
        self.commit_msg_path = config.get('commit_msg_path', '.Gaiah.md')
        self.staging_manager = StagingManager(self.repo_dir)
        self.branch_manager = BranchManager(self.repo_dir)

    def commit_changes(self, commit_message, branch_name=None):
        """変更をコミットする"""
        try:
            if branch_name:
                self.branch_manager.checkout_branch(branch_name, create=True)

            # Gitの設定を確認
            try:
                user_name = run_command(["git", "config", "user.name"], cwd=self.repo_dir)
                user_email = run_command(["git", "config", "user.email"], cwd=self.repo_dir)
                
                if not user_name or not user_email:
                    logger.warning("Git user configuration is missing")
                    run_command(["git", "config", "user.name", "AIRA Bot"], cwd=self.repo_dir)
                    run_command(["git", "config", "user.email", "aira@example.com"], cwd=self.repo_dir)
                    logger.info("Set default Git configuration")
            except Exception as e:
                logger.warning(f"Error checking Git configuration: {e}")
                run_command(["git", "config", "user.name", "AIRA Bot"], cwd=self.repo_dir)
                run_command(["git", "config", "user.email", "aira@example.com"], cwd=self.repo_dir)

            # ステージングされたファイルがあるか確認
            staged_files = run_command(["git", "diff", "--staged", "--name-only"], cwd=self.repo_dir)
            if not staged_files.strip():
                logger.warning("No staged changes to commit")
                return False

            # コミットメッセージファイルを作成
            commit_message_file = os.path.join(self.repo_dir, ".aira_commit_message.txt")
            try:
                with open(commit_message_file, "w", encoding="utf-8") as f:
                    f.write(commit_message)
            except Exception as e:
                logger.error(f"Error writing commit message file: {e}")
                return False

            try:
                # コミットを実行
                output = run_command(["git", "commit", "-F", commit_message_file], cwd=self.repo_dir, check=False)
                if "nothing to commit" in output.lower():
                    logger.warning("Nothing to commit")
                    return False
                
                logger.success("Committed changes.")
                return True
            except Exception as commit_error:
                logger.error(f"Error during commit operation: {commit_error}")
                return False
            finally:
                # コミットメッセージファイルを削除
                try:
                    if os.path.exists(commit_message_file):
                        os.remove(commit_message_file)
                except Exception as e:
                    logger.warning(f"Error removing commit message file: {e}")

        except Exception as e:
            logger.error(f"Error while committing changes: {e}")
            return False

    def process_commits(self, branch_name=None):
        """コミットメッセージファイルからコミットを処理する"""
        content = self._read_commit_messages()
        if not content:
            return

        # ブランチごとのコミット内容を整理
        branch_commits = {}
        branch_sections = re.split(r'(?m)^##\s(.+)', content)[1:]
        self.staging_manager.unstage_files()
        tqdm_sleep(5)

        # 各セクションをブランチごとにグループ化
        for i in range(0, len(branch_sections), 2):
            branch = branch_sections[i].strip()
            content = branch_sections[i + 1]
            if branch not in branch_commits:
                branch_commits[branch] = []
            branch_commits[branch].append(content)

        # ブランチごとにまとめて処理
        for branch, contents in branch_commits.items():
            try:
                # ブランチ名とコンテンツを直接渡す
                current_branch = branch_name or branch
                branch_content = "\n".join(contents)
                if current_branch != "develop":
                    self.branch_manager.checkout_branch(current_branch, create=True)
                self._process_commits_for_branch(branch_content, current_branch)
            except Exception as e:
                logger.error(f"Error processing branch {branch}: {e}")

    def _read_commit_messages(self):
        try:
            with open(self.commit_msg_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            logger.warning(f"Commit messages file not found: {self.commit_msg_path}")
            logger.info(f"Creating an empty commit messages file: {self.commit_msg_path}")
            with open(self.commit_msg_path, "w", encoding="utf-8") as file:
                file.write("")
            return None

    def _process_commits_for_branch(self, branch_content, branch_name):
        """ブランチ内の全コミットを処理する"""
        try:
            commits = re.split(self.FILENAME_REGEX, branch_content)
            if commits and not commits[0].strip():
                commits = commits[1:]

            for j in range(0, len(commits), 2):
                filename = commits[j].strip()
                commit_message_section = commits[j + 1]
                self.process_commit_section(filename, commit_message_section, branch_name)
            
            # developブランチ以外の場合、コミットが成功したらマージを試みる
            if branch_name != "develop":
                try:
                    self.branch_manager.merge_to_develop(branch_name)
                except Exception as merge_error:
                    logger.error(f"Failed to merge branch {branch_name} to develop: {merge_error}")
        except Exception as e:
            logger.error(f"Error processing commits for branch {branch_name}: {e}")
            raise
    def process_commit_section(self, filename, commit_message_section, branch_name):
        """
        コミットセクションを処理する
        """
        commit_message_match = re.search(self.COMMIT_MESSAGE_REGEX, commit_message_section, re.DOTALL)
        if commit_message_match:
            commit_message = commit_message_match.group(1)
            msg = f"{'-'*10} Commit message: [{branch_name}][{filename}]{'-'*10} "
            logger.info(f"{msg}")
            for commit_msg in commit_message.split("\n"):
                logger.info(f"{commit_msg}")
            commit_message = commit_message.strip()
            logger.info(f"{'-'*len(msg)}")
        else:
            logger.warning("No commit message found in the commit section. Skipping...")
            return

        self.process_file(filename, commit_message, branch_name)

    def process_file(self, filename, commit_message, branch_name=None):
        """
        ファイルを処理する
        """
        try:
            # ファイルの存在チェックとステージング
            if os.path.exists(os.path.join(self.repo_dir, filename)):
                logger.info("file is modified")
                self.staging_manager.stage_file(filename, "modified")
            else:
                logger.info("file is deleted")
                self.staging_manager.stage_file(filename, "deleted")

            # ステージされたファイルの確認
            changed_files = run_command(["git", "diff", "--staged", "--name-only"], cwd=self.repo_dir).splitlines()
            
            logger.info(f"changed_files is {changed_files}")
            if filename in changed_files:
                self.commit_changes(commit_message, branch_name)
            else:
                logger.info(f"No changes detected in file: {filename}")

        except Exception as e:
            logger.error(f"Error while processing file: {filename} - {e}")
            raise
