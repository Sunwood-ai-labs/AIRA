import os
import re
from loguru import logger
from .utils import run_command, tqdm_sleep

class CommitManager:
    FILENAME_REGEX = r'(?m)^###\s(.+)'
    COMMIT_MESSAGE_REGEX = r'```commit-msg\n(.*?)\n```'

    def __init__(self, config):
        self.config = config
        self.repo_dir = "./"
        self.commit_msg_path = config.get('commit_msg_path', '.Gaiah.md')

    def unstage_files(self):
        """
        ステージにある全てのファイルをアンステージする
        """
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
        """
        ファイルをステージする
        """
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

    def commit_changes(self, commit_message, branch_name=None):
        """
        変更をコミットする
        """
        try:
            if branch_name:
                try:
                    run_command(["git", "checkout", "-b", branch_name], cwd=self.repo_dir)
                except:
                    pass

            # 複数行のコミットメッセージに対応
            commit_message_lines = commit_message.split("\n")
            commit_message_file = os.path.join(self.repo_dir, ".aira_commit_message.txt")
            with open(commit_message_file, "w", encoding="utf-8") as f:
                f.write(commit_message)
            
            run_command(["git", "commit", "-F", commit_message_file], cwd=self.repo_dir)
            os.remove(commit_message_file)
            logger.success("Committed changes.")

        except Exception as e:
            logger.error(f"Error while committing changes: {e}")
            raise

    def process_commits(self, branch_name=None):
        """
        コミットメッセージファイルからコミットを処理する
        """
        try:
            with open(self.commit_msg_path, "r", encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            logger.warning(f"Commit messages file not found: {self.commit_msg_path}")
            logger.info(f"Creating an empty commit messages file: {self.commit_msg_path}")
            with open(self.commit_msg_path, "w", encoding="utf-8") as file:
                file.write("")
            return

        branch_sections = re.split(r'(?m)^##\s(.+)', content)[1:]
        self.unstage_files()
        tqdm_sleep(5)

        original_branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.repo_dir).strip()
        
        try:
            for i in range(0, len(branch_sections), 2):
                file_branch_name = branch_sections[i].strip()
                branch_content = branch_sections[i + 1]

                current_branch = branch_name or file_branch_name
                commits = re.split(self.FILENAME_REGEX, branch_content)
                if commits and not commits[0].strip():
                    commits = commits[1:]

                try:
                    for j in range(0, len(commits), 2):
                        filename = commits[j].strip()
                        commit_message_section = commits[j + 1]
                        self.process_commit_section(filename, commit_message_section, current_branch)
                    
                    # 各ブランチでの作業が完了したらdevelopにマージ
                    if current_branch != "develop":
                        self.merge_to_develop(current_branch)
                
                except Exception as e:
                    logger.error(f"Error processing branch {current_branch}: {e}")
                    # エラーが発生してもdevelopへのマージを試行
                    if current_branch != "develop":
                        try:
                            self.merge_to_develop(current_branch)
                        except Exception as merge_error:
                            logger.error(f"Failed to merge after error: {merge_error}")
        
        finally:
            # 必ず元のブランチに戻る
            try:
                run_command(["git", "checkout", original_branch], cwd=self.repo_dir)
            except Exception as checkout_error:
                logger.error(f"Failed to return to original branch: {checkout_error}")

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
            if os.path.exists(os.path.join(self.repo_dir, filename)):
                logger.info("file is modified")
                self.stage_file(filename, "modified")
            else:
                logger.info("file is deleted")
                self.stage_file(filename, "deleted")

            changed_files = run_command(["git", "diff", "--staged", "--name-only"], cwd=self.repo_dir).splitlines()
            
            logger.info(f"changed_files is {changed_files}")
            if filename in changed_files:
                self.commit_changes(commit_message, branch_name)
            else:
                logger.info(f"No changes detected in file: {filename}")

        except Exception as e:
            logger.error(f"Error while processing file: {filename} - {e}")
            raise

    def merge_to_develop(self, source_branch):
        """
        指定されたブランチをdevelopブランチにマージし、マージ後にブランチを削除する
        """
        try:
            current_branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.repo_dir).strip()
            
            # developブランチに切り替え
            run_command(["git", "checkout", "develop"], cwd=self.repo_dir)
            
            # マージを試行
            try:
                run_command(["git", "merge", "--no-ff", source_branch], cwd=self.repo_dir)
                logger.success(f"Successfully merged {source_branch} into develop")
                
                # マージが成功したらソースブランチを削除
                if source_branch != "main":  # mainブランチは削除しない
                    run_command(["git", "branch", "-d", source_branch], cwd=self.repo_dir)
                    logger.success(f"Deleted branch: {source_branch}")
                
            except Exception as merge_error:
                logger.error(f"Merge conflict occurred: {merge_error}")
                # マージを中止
                run_command(["git", "merge", "--abort"], cwd=self.repo_dir)
                raise
            finally:
                # 元のブランチに戻る（削除されていない場合のみ）
                if current_branch != source_branch or source_branch == "main":
                    run_command(["git", "checkout", current_branch], cwd=self.repo_dir)
                else:
                    run_command(["git", "checkout", "develop"], cwd=self.repo_dir)
                
        except Exception as e:
            logger.error(f"Error during merge to develop: {e}")
            raise
