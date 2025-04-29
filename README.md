# 育休プラン作成フォーム

このプロジェクトは、育児休業取得計画に必要な情報をフォーム形式で入力し、  
ChatGPT用のプロンプト（指示文）を自動生成する**Flaskアプリケーション**です。

## 概要

- 育休取得を検討中の家族を想定した育休計画プロンプト作成ツール
- 回答した内容をもとに、ChatGPTに貼り付けて育休プラン提案を得ることができます
- データはサーバーに保存されず、**生成されたプロンプトのみを自分でコピー＆活用**します

## 使用技術

- Python 3.x
- Flask
- HTML/CSS (Jinja2テンプレート)


## セットアップ手順

1. リポジトリをクローン
    ```bash
    git clone https://github.com/kbobshida/ikukkyu_webapp.git
    cd ikukkyu_webapp
    ```

2. 仮想環境を作成（推奨）
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windowsなら venv\Scripts\activate
    ```

3. 必要なパッケージをインストール
    ```bash
    pip install -r requirements.txt
    ```

4. アプリを起動
    ```bash
    python app.py
    ```

5. ブラウザでアクセス
    ```
    http://127.0.0.1:5000/
    ```

## 使い方

1. すべての質問項目に回答する
2. 「プロンプトを生成する」ボタンを押す
3. 表示されたプロンプトをコピーする
4. ChatGPTに貼り付けて実行する

※サーバーに個人情報は保存されません。安心してご利用ください。

## ライセンス

このリポジトリは MIT ライセンスのもとで公開されています。  
自由にご利用・改変・配布可能です。

---

# 📢 メモ
- Flask公式サイト：[Flask Documentation](https://flask.palletsprojects.com/)
- ChatGPT公式サイト：[ChatGPT](https://chat.openai.com/)
