from loguru import logger
from .repository_manager import RepositoryManager
from .commit_manager import CommitManager

from litellm import completion
import os

# SourceSageのモジュールをインポート
from sourcesage.core import SourceSage
from sourcesage.modules.ReleaseDiffReportGenerator import GitDiffGenerator, MarkdownReportGenerator
from sourcesage.modules.CommitCraft import CommitCraft
from sourcesage.modules.DocuMind import DocuMind
from sourcesage.modules.IssueWize import IssueWize

from dotenv import load_dotenv
dotenv_path=os.path.join(os.getcwd(), '.env')
logger.debug(f"dotenv_path : {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path, verbose=True, override=True)

class Aira:
    """AIRAメインクラス"""
    def __init__(self, args):
        """初期化"""
        self.args = args
        self.model = args.model
        
        # リポジトリとコミットマネージャーを初期化
        self.repo_manager = RepositoryManager()
        self.commit_manager = CommitManager({"commit_msg_path": os.getenv('COMMIT_MSG_PATH', '.SourceSageAssets/COMMIT_CRAFT/llm_output.md')})

    def run_sourcesage(self):
        """SourceSageの各モジュールを実行する"""
        args = self.args 

        # -----------------------------------------------
        # SourceSageの実行
        if 'all' in args.ss_mode or 'Sage' in args.ss_mode:
            logger.info("SourceSageを起動します...")
            sourcesage = SourceSage(args.ss_output, args.repo, args.owner, args.repository, 
                                    args.ignore_file, args.language_map, args.changelog_start_tag, 
                                    args.changelog_end_tag)
            sourcesage.run()

        # -----------------------------------------------  
        # IssueWizeを使用してIssueを作成
        if 'all' in args.ss_mode or 'IssueWize' in args.ss_mode:
            issuewize = IssueWize(model=args.issuewize_model)
            if args.issue_summary and args.project_name and args.repo_overview_file:
                logger.info("IssueWizeを使用してIssueを作成します...")
                issuewize.create_optimized_issue(args.issue_summary, args.project_name, 
                                                args.milestone_name, args.repo_overview_file)
            else:
                logger.warning("IssueWizeの実行に必要なパラメータが不足しています。")

        # -----------------------------------------------
        # レポートの生成
        if 'all' in args.ss_mode or 'GenerateReport' in args.ss_mode:
            logger.info("git diff レポートの生成を開始します...")
            git_diff_generator = GitDiffGenerator(args.repo_path, args.git_fetch_tags, args.git_tag_sort, args.git_diff_command)
            diff, latest_tag, previous_tag = git_diff_generator.get_git_diff()

            if diff is not None:
                report_file_name = args.report_file_name.format(latest_tag=latest_tag)
                os.makedirs(args.ss_output_path, exist_ok=True)
                output_path = os.path.join(args.ss_output_path, report_file_name)

                markdown_report_generator = MarkdownReportGenerator(diff, latest_tag, previous_tag, 
                                                                    args.report_title, args.report_sections, 
                                                                    output_path)
                markdown_report_generator.generate_markdown_report()

        # -----------------------------------------------
        # CommitCraftを使用してLLMにステージ情報を送信し、コミットメッセージを生成
        if 'all' in args.ss_mode or 'CommitCraft' in args.ss_mode:
            stage_info_file = args.stage_info_file
            llm_output_file = os.path.join(args.commit_craft_output, args.llm_output)
            os.makedirs(args.commit_craft_output, exist_ok=True)
            commit_craft = CommitCraft(args.ss_model_name, stage_info_file, llm_output_file)
            commit_craft.generate_commit_messages()
            
            # コミットメッセージが生成されたら自動コミットを実行
            logger.info("自動コミットを実行します...")
            self.commit_manager.process_commits()

