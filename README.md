<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/AIRA.png" width="100%">
<br>
<h1 align="center">AIRA</h1>
<h2 align="center">
  ～AI-Integrated Repository for Accelerated Development～
<br>
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/AIRA">
<img alt="PyPI - Format" src="https://img.shields.io/pypi/format/AIRA">
<img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/AIRA">
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/AIRA">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dd/AIRA">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/AIRA">
<a href="https://github.com/Sunwood-ai-labs/AIRA" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=AIRA&message=Sunwood-ai-labs&color=blue&logo=github"></a>
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/AIRA">
<a href="https://github.com/Sunwood-ai-labs/AIRA"><img alt="forks - Sunwood-ai-labs" src="https://img.shields.io/github/forks/AIRA/Sunwood-ai-labs?style=social"></a>
<a href="https://github.com/Sunwood-ai-labs/AIRA"><img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/AIRA"></a>
<a href="https://github.com/Sunwood-ai-labs/AIRA"><img alt="GitHub Top Language" src="https://img.shields.io/github/languages/top/Sunwood-ai-labs/AIRA"></a>
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AIRA?color=red">
<img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/Sunwood-ai-labs/AIRA?sort=semver&color=orange">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Sunwood-ai-labs/AIRA/publish-to-pypi.yml">
<br>
<p align="center">
  <a href="https://hamaruki.com/"><b>[🌐 Website]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[🐱 GitHub]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[🐦 Twitter]</b></a> •
  <a href="https://hamaruki.com/"><b>[🍀 Official Blog]</b></a>
</p>

</h2>

</p>

>[!IMPORTANT]
>このリポジトリのリリースノートやREADME、コミットメッセージの9割近くは[claude.ai](https://claude.ai/)や[ChatGPT4](https://chatgpt.com/)を活用した[AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II)で生成しています。

## 🌟 はじめに

AIRAは、リポジトリの管理や開発を加速するためのAIインテグレーション開発ツールです。   
Githubリポジトリの作成、ローカルリポジトリの初期化、コミットメッセージの自動生成、READMEの自動生成などを行うことができます。

開発者の皆さんは、AIRAを使うことで以下のようなメリットを得ることができます。

- リポジトリ管理の自動化による開発の加速  
- コミットメッセージやREADMEの自動生成による手間の削減
- 開発者同士のコミュニケーションの円滑化

AIRAは、開発者の皆さんの開発効率を高め、よりクリエイティブな活動に集中できるようサポートします。

## 🚀 インストール方法

AIRAは、以下の手順でインストールすることができます。

1. Python 3.7以上がインストールされていることを確認してください。
2. ターミナルまたはコマンドプロンプトを開きます。
3. 以下のコマンドを実行して、AIRAをインストールします。

   ```bash
   pip install aira
   ```

これで、AIRAのインストールは完了です。   
`aira --help`コマンドを実行して、使い方を確認してみましょう。

## 📝 使い方

### 環境設定

`.env`ファイルを作成し、必要な設定を記述します。
`.env.example`をコピーして使用することができます。

```bash
cp .env.example .env
```

主な設定項目：
```plaintext
# AIRAの基本設定
GAIAH_RUN=true
COMMIT_MSG_PATH=.Gaiah.md

# LLMの設定
LLM_MODEL=gemini/gemini-1.5-pro-latest
GEMINI_API_KEY=your-api-key-here

# GitHubの設定（必要な場合のみ）
GITHUB_ACCESS_TOKEN=your-github-token-here
```

### コミットメッセージの自動生成

AIRAには2つのコミット生成モードがあります：

1. 基本的なコミットモード：
```bash
aira --mode commit
```

2. SourceSageを使用した高度なコミットモード：
```bash
aira --mode sourcesage commit --ss-model-name="gemini/gemini-1.5-flash-002"
```

このコマンドを実行すると、以下の処理が行われます：

1. 変更内容の取得と解析
2. AIによるコミットメッセージの自動生成
3. ファイルのステージング
4. コミットの実行

#### コミットモードの違い

- **基本モード（--mode commit）**
  - シンプルな変更に適しています
  - 高速な処理が可能
  - 基本的なコミットメッセージを生成

- **SourceSageモード（--mode sourcesage commit）**
  - 複雑な変更に適しています
  - より詳細なコード解析を実行
  - 高品質なコミットメッセージを生成
  - カスタムモデルの指定が可能（--ss-model-name）

## 🤝 コントリビューション

AIRAは、オープンソースプロジェクトです。   
皆さんのコントリビューションを歓迎します！  

バグ報告や機能リクエストがある場合は、[Issueページ](https://github.com/Sunwood-ai-labs/AIRA/issues)からお願いします。   
また、プルリクエストも大歓迎です。 

コントリビューションガイドラインについては、[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## 開発者用

### SourceSageリリースノートを作成コマンド

```shell
sourcesage --mode DocuMind --docuMind-model "gemini/gemini-1.5-pro-latest" --docuMind-db ".SourceSageAssets\DOCUMIND\Repository_summary.md" --docuMind-release-report ".SourceSageAssets\RELEASE_REPORT\Report_v0.2.2.md"  --docuMind-changelog ".SourceSageAssets\Changelog\CHANGELOG_release_0.2.2.md"  --docuMind-output ".SourceSageAssets/DOCUMIND/RELEASE_NOTES_v0.2.2.md"  --docuMind-prompt-output ".SourceSageAssets/DOCUMIND/_PROMPT_v0.2.2.md"  --repo-name "SourceSage" --repo-version "v0.2.2"
```

## 📄 ライセンス

AIRAは、[MITライセンス](https://opensource.org/licenses/MIT)の下で公開されています。   
詳細は、[LICENSE](LICENSE)ファイルを参照してください。

## 🙏 謝辞

AIRAの開発にあたり、以下のオープンソースプロジェクトを活用させていただきました。  
この場を借りて、お礼申し上げます。

- [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)
- [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah)  
- [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II)

また、AIRAの開発には、以下のAIモデルを活用させていただきました。

- [claude.ai](https://claude.ai/)
- [ChatGPT4](https://chat.openai.com/)

最後に、AIRAを使ってくださる開発者の皆さんに感謝いたします。   
皆さんのフィードバックを元に、より良いツールを目指して開発を続けていきます。

これからもAIRAをよろしくお願いします！
