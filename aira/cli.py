import argparse
from art import tprint
from loguru import logger
from gaiah.gaiah import Gaiah
from gaiah.cli import parse_arguments
import sys

logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | <cyan>{name:<45}:{line:<5}</cyan> | <level>{message}</level>",
            "colorize": True,
        }
    ]
)


def parse():
    parser = argparse.ArgumentParser(description="GitHubリポジトリ用のREADMEテンプレートとバッジを生成します。")
    parser.add_argument("--repo_name", help="GitHubリポジトリの名前", default="Repo Name")
    parser.add_argument("--owner_name", help="リポジトリオーナーのGitHubユーザー名", default="Owner name")
    parser.add_argument("--package_name", help="パッケージの名前", default="Package Name")

    return parser

def parse_arguments3():
    # parser = argparse.ArgumentParser(description="Description for all arguments", add_help=True)
    # パッケージ3の引数パーサー
    parser3 = argparse.ArgumentParser(description='Package 3 description')
    parser3.add_argument('--arg5', type=str, choices=['option1', 'option2'], help='Argument 5 help')
    parser3.add_argument('--arg6', type=int, nargs='+', help='Argument 6 help')
    return parser3

def main():
    args = parse_arguments3()
    print("Package 1 argument help:")
    args.print_help()
    
    args = parse()
    print("Package 2 argument help:")
    args.print_help()
    # args2 = parse_arguments2()
    tprint("!  Welcome  to  AIRA  !")
    raise
    gaiah = Gaiah(args)
    gaiah.run()

if __name__ == "__main__":
    main()