from loguru import logger
from .gaiah_repo import GaiahRepo
from .gaiah_commit import GaiahCommit

class Gaiah:
    def __init__(self, args):
        self.args = args
        self.repo_dir = args.repo_dir if args.init_repo or args.process_commits else None
        self.commit_msg_path = args.commit_msg_path if args.process_commits else None
        self.repo = GaiahRepo(self.repo_dir, self.commit_msg_path)
        self.commit = GaiahCommit(self.repo)

    def run(self):
        if self.args.init_repo:
            self.init_local_repo(self.args.repo_dir, not self.args.no_initial_commit)

        if self.args.create_repo:
            repo_params = {
                'description': self.args.description,
                'private': self.args.private
            }
            self.create_remote_repo(self.args.repo_name, repo_params)

        if self.args.process_commits:
            self.commit.process_commits(branch_name=self.args.branch_name)

        logger.success("successfully!")

    def init_local_repo(self, repo_dir, initial_commit=True):
        self.repo.init_local_repo(repo_dir, initial_commit)

    def create_remote_repo(self, repo_name, repo_params):
        logger.info(">>> リモートリポジトリを作成しています...")
        self.repo.create_remote_repo(repo_name, repo_params)
        
        logger.info(">>> ブランチを作成しています...")
        self.repo.create_branches()
        
        logger.info(">>> 初期ファイルを追加しています...")
        self.repo.add_initial_files()
        
        logger.info(">>> 初期ファイルをコミットしています...")
        self.repo.commit_initial_files()
        
        logger.info(">>> ブランチをマージしています...")
        self.repo.merge_branches()
        
        logger.info(">>> マージしたブランチをプッシュしています...")
        self.repo.push_merged_branches()